from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/sml_trade/(?P<sml_trade>\w+)/$", consumers.smlTradeConsumer.as_asgi()),
]