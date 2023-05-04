from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from coin.coin import get_krw_market_list
from coin.models import Ticker

import json

class smlTradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["sml_trade"]
        self.room_group_name = "sml_trade_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        while True:
            length = len(get_krw_market_list()) 
            ticker_qs = Ticker.objects.order_by('-id')[:length]
            ticker_ls = []

            for ts in ticker_qs:
                ticker_ls.append(model_to_dict(ts))


            await self.channel_layer.group_send(
                self.room_group_name, { 
                    "type": "ticker", 
                    "ticker_ls": ticker_ls
                }
            )

            ticker_ls.sort(key=lambda x:x['acc_trade_price_24h'], reverse=True)
            
            await self.send(text_data=json.dumps(ticker_ls))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )