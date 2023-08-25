from coin.models import Ticker
from django.db import transaction
from typing import List, Dict, Any

import websockets
import json 
import requests
import json 
import time


url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)


def get_krw_codes_list() -> List[str]:
    krw_codes = [] 

    for res in response.json():
        market = res['market']
        
        if market[:3] == 'KRW':
            krw_codes.append(market)

    return krw_codes


def get_kr_name_dic() -> Dict[str, str]:
    kr_name_dic = {}

    for res in response.json():
        market = res['market']
        
        if market[:3] == 'KRW':
            kr_name_dic[market] = res['korean_name']

    return kr_name_dic


@transaction.atomic
async def get_ticker() -> None:
    async with websockets.connect('wss://api.upbit.com/websocket/v1') as websocket:
        request_ticker = [
            {"ticket":"ticket"},
            {
                "type":"ticker",
                "codes": get_krw_codes_list()
            }
        ]

        await websocket.send(json.dumps(request_ticker))

        kr_name_dic = get_kr_name_dic()
        tickers = []

        for _ in range(len(get_krw_codes_list())):
            recv = await websocket.recv()
            recv_obj = json.loads(recv)

            code = recv_obj['code']
            name = kr_name_dic.get(code)

            tickers.append(Ticker(name=name, **recv_obj))

        Ticker.objects.bulk_create(tickers)


def get_top_trade_price_coin() -> List[Ticker]:
    length = len(get_krw_codes_list()) 
    ticker_list = Ticker.objects.order_by('-id')[:length]
    coin_list = []

    for ticker in ticker_list:
        if ticker.acc_trade_price_24h >= 100_000_000_000:
            coin_list.append(ticker)
    
    coin_list.sort(key=lambda x: x.acc_trade_price_24h, reverse=True)
    
    return coin_list


def get_top_trade_volume_coin() -> Ticker:
    dic = {}

    for coin in get_top_trade_price_coin():
        dic[coin] = coin.trade_volume

    top_trade_volume_coin = max(dic, key=dic.get)

    return top_trade_volume_coin


def get_coin_snapshot(code: str) -> Dict[str, Any]:
    url = "https://api.upbit.com/v1/ticker?markets=" + code

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()[0]