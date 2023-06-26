from django.urls import re_path

from web_player.src.apps import consumers

websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
