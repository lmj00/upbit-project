from channels.generic.websocket import AsyncWebsocketConsumer
from .coin import get_top_trade_price_coin

import time
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["coin"]
        self.room_group_name = "coin_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        try:
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
                
                await self.send(text_data=json.dumps({"coin_dic": coin_dic}))
                
                time.sleep(1)
        except:
            print("재연결")
            await self.connect()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )