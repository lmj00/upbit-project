from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.db.models.query import QuerySet

from .models import Account, History, Bookmark
from coin.coin import get_kr_name_dic

from typing import Optional, Union, Tuple, Dict, List, Any
from decimal import Decimal

import json


def index(request: HttpRequest):
    bookmarks: List[Dict[str, Union[int, str]]] = list(Bookmark.objects.all().values())
    context = {'bookmarks': bookmarks}
    
    return render(request, 'simulated_trade/index.html', context=context)


def check_tick_size(price: float) -> Union[int, float]:
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
def order_bid(request: HttpRequest) -> JsonResponse:  
    json_obj: Dict[str, str] = json.loads(request.body)
    reversed_dic: Dict[str, str] = {v: k for k, v in get_kr_name_dic().items()}

    krw_account: Account = Account.objects.get(currency='KRW')
    krw_balance: Decimal = krw_account.balance

    kr_name: str = json_obj['in_name']
    code: List[str] = reversed_dic[kr_name].split('-')

    currency: str = code[1]
    unit_currency: str = code[0]

    buy_quantity: Decimal = Decimal(json_obj['in_quantity'])
    buy_price: Decimal = Decimal(json_obj['in_price'])
    buy_total: Decimal = buy_quantity * buy_price
    buy_fee: Decimal = buy_total * Decimal(0.0005)

    cts: Union[int, float] = check_tick_size(buy_price)

    message: str = ''
    
    if Decimal(str(buy_price)) % Decimal(str(cts)) != 0:
        message = f'주문가격은 {cts}KRW 단위로 입력 부탁드립니다.'
    elif krw_balance < buy_total + buy_fee:
        message = '주문가능 금액이 부족합니다.' 
    elif buy_total < 5000:
        message = '최소 주문금액은 5000KRW입니다.'
    else:
        obj: Account
        created: bool

        obj, created = Account.objects.get_or_create(
            currency = currency,
            unit_currency = unit_currency,
            defaults = {
                'balance': buy_quantity,
                'avg_buy_price' : buy_price
            }
        )   

        krw_account.balance -= buy_total + buy_fee
        krw_account.save()

        if created == False:
            Account.objects.filter(id=obj.id).update(
                balance = obj.balance + buy_quantity,
                avg_buy_price = (obj.avg_buy_price * obj.balance + buy_price * buy_quantity) / (obj.balance + buy_quantity)
            )

        History.objects.create(
            side = 'bid',
            market = unit_currency + '-' + currency,
            price = buy_price,
            volume = buy_quantity,
            paid_fee = buy_fee
        )

        message = '매수주문이 완료되었습니다.'



    reponse_data = {
        'message': message
    }

    return JsonResponse(reponse_data)


@transaction.atomic
def order_ask(request: HttpRequest) -> JsonResponse:
    json_obj: Dict[str, str] = json.loads(request.body)    
    reversed_dic: Dict[str, str] = {v: k for k, v in get_kr_name_dic().items()}

    kr_name: str = json_obj['in_name']
    code: List[str] = reversed_dic[kr_name].split('-')

    currency: str = code[1]
    unit_currency: str = code[0]

    sell_balance: Decimal = Decimal(json_obj['in_quantity'])
    sell_price: Decimal = Decimal(json_obj['in_price'])
    sell_total: Decimal = sell_balance * sell_price

    qs: QuerySet[Account] = Account.objects.filter(
        currency=currency, 
        unit_currency=unit_currency
    )

    ac_coin: Optional[Account] = qs.first()
    cts: Union[int, float] = check_tick_size(sell_price)
    message: str = ''

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
            sell_krw: Decimal = (sell_price / ac_coin.avg_buy_price) * ac_coin.avg_buy_price * sell_balance
            sell_fee: Decimal = sell_krw * Decimal(0.0005)

            if sell_balance < ac_coin.balance:
                Account.objects.filter(id=ac_coin.id).update(
                    balance = ac_coin.balance - sell_balance
                )
            else:
                Account.objects.get(id=ac_coin.id).delete()

            krw_account: Account = Account.objects.get(currency='KRW')
            Account.objects.filter(id=krw_account.id).update(balance=krw_account.balance + sell_krw - sell_fee)

            History.objects.create(
                side = 'ask',
                market = unit_currency + '-' + currency,
                price = sell_price,
                volume = sell_balance,
                paid_fee = sell_fee
            )

            message = '매도주문이 완료되었습니다.'

    except Exception as e:
        message = e

    reponse_data = {
        'message': message
    }

    return JsonResponse(reponse_data)


def get_history(request: HttpRequest, code: str) -> JsonResponse:
    history: History = History.objects.filter(market=code)
    response_data = []
    price: Union[str, int]

    for hs in history:
        if hs.side == 'bid':
            side = '매수'
        else:
            side = '매도'

        cts_price: Union[int, float] = check_tick_size(hs.price)

        if cts_price < 1:
            point: str = str(cts_price).split()[-1]    
            price = f'{hs.price:.{len(point)}f}'
        else:
            price = int(hs.price)

        volume: str = f'{hs.volume:.8f}'

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


def check_bookmark(request: HttpRequest, code: str) -> JsonResponse:
    has_bookmark: bool = Bookmark.objects.filter(market=code).exists()

    if not has_bookmark:
        Bookmark.objects.create(market=code)
    else:
        Bookmark.objects.filter(market=code).delete()

    return JsonResponse({'status': 200})