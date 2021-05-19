from channels.routing import URLRouter
from django.urls import re_path
from . import consumers


websocket_routes = [
    re_path(r"ws/chat/(?P<room_uuid>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
