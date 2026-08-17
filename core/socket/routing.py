from django.urls import re_path
from core.socket import FeedRoom

websocket_urlpatterns = [
    re_path(r"ws/feed/(?P<feed_uuid>[0-9a-f-]+)/$", FeedRoom.as_asgi()),
]