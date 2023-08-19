from django.urls import re_path

from . import account_consumers, ticker_consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<sml_trade>\w+)/ticker/$", ticker_consumers.TickerConsumer.as_asgi()),
    re_path(r"ws/(?P<sml_trade>\w+)/account/$", account_consumers.AccountConsumer.as_asgi())
]