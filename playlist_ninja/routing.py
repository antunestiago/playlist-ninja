from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from django.core.asgi import get_asgi_application
from playlist import consumer

websocket_urlpatterns = [
    re_path(r"ws/music_complete/$", consumer.MusicConsumer),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # (http->django views is added by default)
        "websocket": URLRouter([
            path('song', consumer.MusicConsumer.as_asgi())
        ]),
    }
)
