from channels.routing import ProtocolTypeRouter, ChannelNameRouter

from testgale.core import consumers

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "channel": ChannelNameRouter({
        "crawler-process": consumers.CrawlerProcess,
    }),
})