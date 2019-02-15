import aiohttp

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from bs4 import BeautifulSoup

from testgale.core.models import Crawler, Link, Image


class CrawlerProcess(AsyncConsumer):

    @database_sync_to_async
    def update_database_crawler(self, message):
        crawler = Crawler()
        crawler.url = message['url']
        crawler.depth = message['depth']
        crawler.save()
        return crawler

    @database_sync_to_async
    def update_database_link(self, crawler, links):
        for link in links:
            obj = Link.objects.create(url=link.get('href'))
            crawler.link_set.add(obj)


    @database_sync_to_async
    def update_database_image(self, crawler, images):
        for image in images:
            obj = Image.objects.create(url=image.get('src'))
            crawler.image_set.add(obj)
        
    async def start_crawler(self, crawler):

        async with aiohttp.ClientSession() as session:
            async with session.get(crawler.url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                links = soup.find_all('a')
                images = soup.find_all('img')
                
                await self.update_database_link(crawler, links)
                await self.update_database_image(crawler, images)
    

    async def generate(self, message):
        # Update the database once done
        crawler = await self.update_database_crawler(message)

        # Start the process
        await self.start_crawler(crawler)