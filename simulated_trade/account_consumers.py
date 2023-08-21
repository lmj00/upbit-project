from channels.generic.websocket import AsyncWebsocketConsumer

from coin.models import Ticker
from .models import Account

from coin.coin import get_krw_codes_list

import asyncio
import json

class AccountConsumer(AsyncWebsocketConsumer):
    length = len(get_krw_codes_list()) 

    async def receive(self, text_data):
        data = json.loads(text_data)
        signal = data.get('signal')
        
        if signal:
            await asyncio.gather(
                self.send_account_coin(),
                self.send_account_balance()
            )
            
            
    async def send_account_coin(self):
        ac_obj = Account.objects.all()
        sml_account_ls = []
        gcs = None

        for coin in ac_obj:
            code = coin.unit_currency + "-" + coin.currency
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
                dic['avg_buy_price'] = int(coin.avg_buy_price)
                dic['amount_money'] = int(amount_money)
                dic['valuation_amount'] = int(valuation_amount)
                dic['rate_of_return'] = rate_of_return

                sml_account_ls.append(dic)

        await self.send(text_data=json.dumps({
            "type": "sml_account",
            "value": sml_account_ls
        }))


    async def send_account_balance(self):
        ac_obj = Account.objects.all()
        gcs = None
        
        holding_krw = ac_obj.get(currency='KRW').balance
        total_purchase = total_evaluation = total_assets = 0

        for coin in ac_obj:
            code = coin.unit_currency + "-" + coin.currency

            if code != 'KRW-KRW':
                ticker_qs = Ticker.objects.order_by('-id')[:self.length]

                for tqs in ticker_qs:
                    if code == tqs.code:
                        gcs = tqs

                total_purchase += coin.avg_buy_price * coin.balance
                total_evaluation += (coin.avg_buy_price * coin.balance) + (gcs.trade_price - coin.avg_buy_price) * coin.balance

        profit_or_loss = total_evaluation - total_purchase
        total_assets += holding_krw + total_evaluation
        rate_of_return = round((total_evaluation - total_purchase) / total_purchase * 100, 2)

        ac_dic = {
            'holding_krw': int(holding_krw),
            'total_assets': int(total_assets),
            'total_purchase': int(total_purchase),
            'total_evaluation': int(total_evaluation),
            'profit_or_loss': int(profit_or_loss),
            'rate_of_return': rate_of_return
        }

        await self.send(text_data=json.dumps({
            "type": "sml_account_balance",
            "value": ac_dic
        }))