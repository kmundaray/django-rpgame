from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/RpGameConsumer/(?P<game_id>\d+)/$', consumers.RpGameConsumer.as_asgi()),
    re_path(r'^ws/RpGameConsumer/$', consumers.RpGameConsumer.as_asgi()),
]