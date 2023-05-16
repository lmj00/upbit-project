from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from coin.coin import get_krw_market_list
from coin.models import Ticker

import asyncio
import json


class smlTradeConsumer(AsyncWebsocketConsumer):
    room_group_name = 'coin_group'

    async def connect(self):
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_ticker()
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )


    async def send_ticker(self):
        length = len(get_krw_market_list()) 

        while True:
            ticker_qs = Ticker.objects.order_by('-id')[:length]
            ticker_ls = [model_to_dict(ts) for ts in ticker_qs]

            await self.channel_layer.group_send(
                self.room_group_name, { 
                    "ticker_ls": ticker_ls
                }
            )

            ticker_ls.sort(key=lambda x:x['acc_trade_price_24h'], reverse=True)

            await self.send(text_data=json.dumps(ticker_ls))

            await asyncio.sleep(1)