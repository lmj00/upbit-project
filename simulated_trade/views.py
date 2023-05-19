from django.shortcuts import render
from django.http import JsonResponse
from .models import smlAccount
from coin.coin import get_kr_name_dic

import json


# Create your views here.
def index(request):
    return render(request, 'simulated_trade/index.html')


def order_bid(request):  
    json_obj = json.loads(request.body)    
    reversed_dic = {v: k for k, v in get_kr_name_dic().items()}

    kr_name = json_obj['in_name']
    code = reversed_dic[kr_name].split('-')

    smlAccount.objects.create(
        currency = code[0],
        balance = json_obj['in_quantity'], 
        avg_buy_price = json_obj['in_price'],
        unit_currency = code[1]
    )

    reponse_data = {
        'message': '매수 주문이 완료되었습니다.'
    }

    return JsonResponse(reponse_data)