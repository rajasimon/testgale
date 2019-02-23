from django.urls import path

from testgale.core import consumers

websocket_patterns = [
    path('ws/chat/<room_name>/', consumers.CrawlerConsumer)
]

channel_patterns = {
    "crawler-process": consumers.CrawlerProcess,
}