from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from testgale.core import routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    "websocket": URLRouter(routing.websocket_patterns),
    "channel": ChannelNameRouter(routing.channel_patterns),
})