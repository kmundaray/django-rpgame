

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/RpGameConsumer/$', consumers.RpGameConsumer.as_asgi()),
    # add more paths and consumers as needed
]

