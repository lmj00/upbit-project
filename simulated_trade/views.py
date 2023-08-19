from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from .models import Account, History
from coin.coin import get_kr_name_dic

from decimal import Decimal
import json


# Create your views here.
def index(request):
    return render(request, 'simulated_trade/index.html')


def check_tick_size(price):
    if price >= 2_000_000:
        return 1000
    
    if price >= 1_000_000:
        return 500
    
    if price >= 500_000:
        return 100

    if price >= 100_000:
        return 50

    if price >= 10_000:
        return 10

    if price >= 1_000:
        return 5
    
    if price < 0.1:
        return 0.0001
    
    if price < 1:
        return 0.001
    
    if price < 10:
        return 0.01
    
    if price < 100:
        return 0.1
    
    if price < 1_000:
        return 1


@transaction.atomic
def order_bid(request):  
    json_obj = json.loads(request.body)    
    reversed_dic = {v: k for k, v in get_kr_name_dic().items()}

    krw_balance_obj = Account.objects.get(currency='KRW')
    krw_balance = krw_balance_obj.balance

    kr_name = json_obj['in_name']
    code = reversed_dic[kr_name].split('-')

    buy_quantity = float(json_obj['in_quantity'])
    buy_price = float(json_obj['in_price'])
    buy_total = buy_quantity * buy_price
    
    cts = check_tick_size(buy_price)

    message = ''
    
    if Decimal(str(buy_price)) % Decimal(str(cts)) != 0:
        message = f'주문가격은 {cts}KRW 단위로 입력 부탁드립니다.'
    elif krw_balance < buy_total + (buy_total * 0.0005):
        message = '주문가능 금액이 부족합니다.' 
    elif buy_total < 5000:
        message = '최소 주문금액은 5000KRW입니다.'
    else:
        obj, created = Account.objects.get_or_create(
            currency = code[1],
            unit_currency = code[0],
            defaults = {
                'balance': buy_quantity,
                'avg_buy_price' : buy_price
            }
        )   
        
        krw_balance_obj.balance -= buy_total + (buy_total * 0.0005) 
        krw_balance_obj.save()

        if created == False:
            Account.objects.filter(id=obj.id).update(
                balance = obj.balance + buy_quantity,
                avg_buy_price = (obj.avg_buy_price * obj.balance + buy_price * buy_quantity) / (obj.balance + buy_quantity)
            )

        History.objects.create(
            side = 'bid',
            market = code[0] + '-' + code[1],
            price = buy_price,
            volume = buy_quantity,
            paid_fee = buy_total * 0.0005
        )

        message = '매수주문이 완료되었습니다.'



    reponse_data = {
        'message': message
    }

    return JsonResponse(reponse_data)


@transaction.atomic
def order_ask(request):
    json_obj = json.loads(request.body)    
    reversed_dic = {v: k for k, v in get_kr_name_dic().items()}

    kr_name = json_obj['in_name']
    code = reversed_dic[kr_name].split('-')

    currency = code[1]
    unit_currency = code[0]
    sell_balance = float(json_obj['in_quantity'])
    sell_price = float(json_obj['in_price'])
    sell_total = sell_balance * sell_price

    qs = Account.objects.filter(
        currency=currency, 
        unit_currency=unit_currency
    )

    ac_coin = qs.first()
    cts = check_tick_size(sell_price)
    message = ''

    try:
        if Decimal(str(sell_price)) % Decimal(str(cts)) != 0:
            message = f'주문가격은 {cts}KRW 단위로 입력 부탁드립니다.'
        elif ac_coin is None:
            message = '주문가능 수량이 부족합니다.'
        elif sell_balance > ac_coin.balance:
            message = "보유수량이 부족합니다."
        elif sell_total < 5000:
            message = '최소 주문금액은 5000KRW입니다.'
        else:
            krw = (sell_price / ac_coin.avg_buy_price) * ac_coin.avg_buy_price * sell_balance
            total_krw = krw - (krw * 0.0005)

            if sell_balance < ac_coin.balance:
                Account.objects.filter(id=ac_coin.id).update(
                    balance = ac_coin.balance - sell_balance
                )
            else:
                Account.objects.get(id=ac_coin.id).delete()

            krw_account = Account.objects.get(currency='KRW')
            Account.objects.filter(id=krw_account.id).update(balance=krw_account.balance + total_krw)

            History.objects.create(
                side = 'ask',
                market = code[0] + '-' + code[1],
                price = sell_price,
                volume = sell_balance,
                paid_fee = sell_total * 0.0005
            )

            message = '매도주문이 완료되었습니다.'

    except Exception as e:
        message = e

    reponse_data = {
        'message': message
    }

    return JsonResponse(reponse_data)


def get_history(request, code):
    history = History.objects.filter(market=code)
    response_data = []
    
    for hs in history:
        if hs.side == 'bid':
            side = '매수'
        else:
            side = '매도'

        cts_price = check_tick_size(hs.price)

        if cts_price < 1:
            point = str(cts_price).split()[-1]    
            price = f'{hs.price:.{len(point)}f}'
        else:
            price = int(hs.price)

        volume = f'{hs.volume:.8f}'

        obj = {
            'side': side,
            'market': hs.market,           
            'created_at': hs.created_at,
            'price': price,
            'total': Decimal(price) * Decimal(volume),
            'volume': volume,
        }

        response_data.append(obj)

    return JsonResponse({'history': response_data})