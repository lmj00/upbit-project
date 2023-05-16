from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/coin/(?P<coin>\w+)/$", consumers.CoinConsumer.as_asgi()),
]