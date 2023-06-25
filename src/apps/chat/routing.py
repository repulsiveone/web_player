from django.urls import re_path

from web_player.src.apps import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.websocket_receive),
]
