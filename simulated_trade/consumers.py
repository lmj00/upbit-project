from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms.models import model_to_dict

from coin.coin import get_krw_codes_list

from coin.models import Ticker
from .models import Account

import asyncio
import json

class smlTradeConsumer(AsyncWebsocketConsumer):
    length = len(get_krw_codes_list()) 

    async def connect(self):
        await self.accept()


    async def receive(self, text_data):
        data = json.loads(text_data)
        signal = data.get('signal')
        
        if signal == True:
            await asyncio.gather(
                self.send_ticker(),
                self.send_account_coin(),
                self.send_account_balance()
            )


    async def send_ticker(self):
        ticker_qs = Ticker.objects.order_by('-id')[:self.length]
        ticker_ls = [model_to_dict(ts) for ts in ticker_qs]
        ticker_ls.sort(key=lambda x:x['acc_trade_price_24h'], reverse=True)

        await self.send(text_data=json.dumps({
            "type": "ticker",
            "value": ticker_ls
        }))


    async def send_account_coin(self):
        ac_obj = Account.objects.all()
        sml_account_ls = []
        gcs = None

        for coin in ac_obj:
            code = coin.currency + "-" + coin.unit_currency
            dic = {}

            if code != 'KRW-KRW':
                ticker_qs = Ticker.objects.order_by('-id')[:self.length]

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


    async def send_account_balance(self):
        ac_obj = Account.objects.all()
        gcs = None

        ac_dic = {
            'holding_krw':ac_obj.get(unit_currency='KRW').balance,
            'total_assets': 0,
            'total_purchase': 0,
            'total_evaluation': 0,
            'profit_or_loss': 0,
            'rate_of_return': 0
        }
        
        for coin in ac_obj:
            code = coin.currency + "-" + coin.unit_currency

            if code != 'KRW-KRW':
                ticker_qs = Ticker.objects.order_by('-id')[:self.length]

                for tqs in ticker_qs:
                    if code == tqs.code:
                        gcs = tqs

                ac_dic['total_purchase'] += coin.avg_buy_price * coin.balance
                ac_dic['total_evaluation'] += (coin.avg_buy_price * coin.balance) + (gcs.trade_price - coin.avg_buy_price) * coin.balance

        ac_dic['profit_or_loss'] = ac_dic['total_evaluation'] - ac_dic['total_purchase']
        ac_dic['total_assets'] += ac_dic['holding_krw'] + ac_dic['total_evaluation']
        ac_dic['rate_of_return'] = round((ac_dic['total_evaluation'] - ac_dic['total_purchase']) / ac_dic['total_purchase'] * 100, 2)
                

        await self.send(text_data=json.dumps({
            "type": "sml_account_balance",
            "value": ac_dic
        }))