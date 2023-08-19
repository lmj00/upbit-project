from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from coin.models import Ticker

from coin.coin import get_krw_codes_list

import json

class TickerConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        signal = data.get('signal')

        if signal:
            await self.send_ticker()
        
        
    async def send_ticker(self):
        length = len(get_krw_codes_list()) 

        ticker_qs = Ticker.objects.order_by('-id')[:length]
        ticker_ls = []

        for ts in ticker_qs:
            ticker_dict = model_to_dict(ts)
            ticker_dict['change_rate'] = str(round(ticker_dict['change_rate'] * 100, 2))
            ticker_dict['signed_change_rate'] = str(round(ticker_dict['signed_change_rate'] * 100, 2))
            ticker_ls.append(ticker_dict)

        ticker_ls.sort(key=lambda x:x['acc_trade_price_24h'], reverse=True)

        await self.send(text_data=json.dumps({
            "type": "ticker",
            "value": ticker_ls
        }))