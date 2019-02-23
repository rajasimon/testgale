import json

import aiohttp

from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from bs4 import BeautifulSoup

from testgale.core.models import Crawler, Image


class CrawlerProcess(AsyncConsumer):

    @database_sync_to_async
    def update_database_crawler(self, url, depth):
        crawler, created = Crawler.objects.get_or_create(url=url)
        if created:
            crawler.depth = depth
            crawler.save()

        result = crawler.link.filter(depth=depth+1).all()
        if not result:
            result = [crawler]
        return result

    @database_sync_to_async
    def update_database_link(self, crawler, depth, links):
        for link in links:
            url = link.get('href')

            if url:
                obj = Crawler.objects.create(url=url)
                obj.depth = depth
                obj.save()
                crawler.link.add(obj)

    @database_sync_to_async
    def update_database_image(self, crawler, depth, images):
        for image in images:
            url = image.get('href')

            if url:
                obj = Image.objects.create(url=image.get('src'))
                crawler.image_set.add(obj)
        
    async def start_crawler(self, url, depth):
        # Update the database once done
        crawlers = await self.update_database_crawler(url, depth)

        for crawler in crawlers:
            async with aiohttp.ClientSession() as session:
                async with session.get(crawler.url) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    links = soup.find_all('a')
                    images = soup.find_all('img')
                    
                    await self.update_database_link(crawler, depth, links)
                    await self.update_database_image(crawler, depth, images)

    async def process(self, url, depth):
        start = int(depth)
        end = 0
        
        while start >= end:
            # Start the process
            await self.start_crawler(url, start)

            start -= 1

        return True

    async def generate(self, message):
        url = message['url']
        depth = message['depth']

        status = await self.process(url, depth)
        if status:
        
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                "chat_stream", 
                {
                    "type": "stream_message", 
                    "message": {'isCompleted': True},
                }
            )

class CrawlerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # To accept the connection call
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)


    # Receive message from room group
    async def stream_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))