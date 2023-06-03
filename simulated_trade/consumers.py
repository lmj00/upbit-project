from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from coin.coin import get_krw_codes_list

from coin.models import Ticker
from .models import smlAccount

import asyncio
import json

class smlTradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_group_name = 'coin_group'

        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await asyncio.gather(
            self.send_ticker(),
            self.send_account_coin()
        )


    async def send_ticker(self):
        length = len(get_krw_codes_list()) 

        while True:
            ticker_qs = Ticker.objects.order_by('-id')[:length]
            ticker_ls = [model_to_dict(ts) for ts in ticker_qs]

            # await self.channel_layer.group_send(
            #     self.room_group_name, { 
            #         "data": ticker_ls
            #     }
            # )

            ticker_ls.sort(key=lambda x:x['acc_trade_price_24h'], reverse=True)

            await self.send(text_data=json.dumps({
                "type": "ticker",
                "value": ticker_ls
            }))

            await asyncio.sleep(1)


    async def send_account_coin(self):
        length = len(get_krw_codes_list()) 

        while True:
            sm_ac_objects = smlAccount.objects.all()
            sml_account_ls = []
            gcs = None

            for coin in sm_ac_objects:
                code = coin.currency + "-" + coin.unit_currency
                dic = {}

                if code != 'KRW-KRW':
                    ticker_qs = Ticker.objects.order_by('-id')[:length]

                    for tqs in ticker_qs:
                        if code == tqs.code:
                            gcs = tqs

                    rate_of_return = round((gcs.trade_price - coin.avg_buy_price) / coin.avg_buy_price * 100, 2)
                    amount_money = coin.balance * coin.avg_buy_price
                    valuation_amount = amount_money + (amount_money * rate_of_return / 100) 

                    dic['name'] = gcs.name
                    dic['balance'] = coin.balance
                    dic['avg_buy_price'] = coin.avg_buy_price
                    dic['amount_money'] = amount_money
                    dic['rate_of_return'] = rate_of_return
                    dic['valuation_amount'] = valuation_amount

                    sml_account_ls.append(dic)

            await self.send(text_data=json.dumps({
                "type": "sml_account",
                "value": sml_account_ls
            }))

            await asyncio.sleep(1)