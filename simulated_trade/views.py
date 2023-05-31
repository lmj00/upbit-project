from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from .models import smlAccount
from coin.coin import get_kr_name_dic

import json


# Create your views here.
def index(request):
    return render(request, 'simulated_trade/index.html')


def order_bid(request):  
    json_obj = json.loads(request.body)    
    reversed_dic = {v: k for k, v in get_kr_name_dic().items()}

    krw_balance_obj = smlAccount.objects.get(unit_currency='KRW')
    krw_balance = krw_balance_obj.balance

    kr_name = json_obj['in_name']
    code = reversed_dic[kr_name].split('-')

    in_quantity = float(json_obj['in_quantity'])
    in_price = float(json_obj['in_price'])
    in_total = in_quantity * in_price
    
    message = ''

    if krw_balance < in_total + (in_total * 0.0005):
        message = '주문가능 금액이 부족합니다.' 
    else:
        obj, created = smlAccount.objects.get_or_create(
            unit_currency = code[1],
            currency = code[0],
            defaults = {
                'balance': in_quantity,
                'avg_buy_price' : in_price
            }
        )   
        
        krw_balance_obj.balance -= in_total + (in_total * 0.0005) 
        krw_balance_obj.save()

        if created == False:
            smlAccount.objects.filter(id=obj.id).update(
                balance = obj.balance + in_quantity,
                avg_buy_price = (obj.avg_buy_price * obj.balance + in_price * in_quantity) / (obj.balance + in_quantity)
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

    unit_currency = code[1]
    currency = code[0]
    sell_balance = float(json_obj['in_quantity'])
    sell_price = float(json_obj['in_price'])
    
    qs = smlAccount.objects.filter(
        currency=currency, 
        unit_currency=unit_currency
    )

    ac_coin = qs.first()
    message = ''

    try:
        if sell_balance == ac_coin.balance:
            krw = (sell_price / ac_coin.avg_buy_price) * ac_coin.avg_buy_price * ac_coin.balance
            krw_account = smlAccount.objects.get(unit_currency='KRW')
            
            smlAccount.objects.get(id=ac_coin.id).delete()
            smlAccount.objects.filter(id=krw_account.id).update(balance=krw_account.balance + krw)
            message = '매도 주문이 완료되었습니다.'
            
    except Exception as e:
        message = e

    reponse_data = {
        'message': message
    }

    return JsonResponse(reponse_data)