from channels.generic.websocket import AsyncWebsocketConsumer
from .coin import get_top_trade_price_coin

import json
import asyncio

class CoinConsumer(AsyncWebsocketConsumer):
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
        while True:
            coin_dic = {}
    
            for ttpc in get_top_trade_price_coin():
                coin_dic[ttpc.code] = ttpc.trade_price

            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "ticker", 
                    "coin": coin_dic
                }
            )
            
            await self.send(text_data=json.dumps(coin_dic))

            await asyncio.sleep(1)  