from coin.models import Ticker
from django.db import transaction

import websockets
import json 
import requests
import json 
import time


url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)


def get_krw_codes_list():
    krw_codes = []

    for res in response.json():
        market = res['market']
        
        if market[:3] == 'KRW':
            krw_codes.append(market)

    return krw_codes


def get_kr_name_dic():
    kr_name_dic = {}

    for res in response.json():
        market = res['market']
        
        if market[:3] == 'KRW':
            kr_name_dic[market] = res['korean_name']

    return kr_name_dic


async def get_ticker():
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

        for _ in range(len(get_krw_codes_list())):
            recv = await websocket.recv()
            recv_obj = json.loads(recv)

            code = recv_obj['code']
            name = kr_name_dic.get(code)

            with transaction.atomic():
                Ticker.objects.create(
                    type = recv_obj['type'],
                    code = code,
                    name = name,
                    opening_price = recv_obj['opening_price'],
                    high_price = recv_obj['high_price'],
                    low_price = recv_obj['low_price'],
                    trade_price = recv_obj['trade_price'],
                    prev_closing_price = recv_obj['prev_closing_price'],
                    change = recv_obj['change'],
                    change_price =  recv_obj['change_price'],
                    signed_change_price = recv_obj['signed_change_price'],
                    change_rate = recv_obj['change_rate'],
                    signed_change_rate = recv_obj['signed_change_rate'],
                    trade_volume = recv_obj['trade_volume'],
                    acc_trade_volume = recv_obj['acc_trade_volume'],
                    acc_trade_volume_24h = recv_obj['acc_trade_volume_24h'],
                    acc_trade_price = recv_obj['acc_trade_price'],
                    acc_trade_price_24h	= recv_obj['acc_trade_price_24h'],
                    trade_date = recv_obj['trade_date'],
                    trade_time = recv_obj['trade_time'],
                    trade_timestamp = recv_obj['trade_timestamp'],
                    ask_bid = recv_obj['ask_bid'],
                    acc_ask_volume = recv_obj['acc_ask_volume'],
                    acc_bid_volume = recv_obj['acc_bid_volume'], 
                    highest_52_week_price = recv_obj['highest_52_week_price'],
                    highest_52_week_date = recv_obj['highest_52_week_date'],
                    lowest_52_week_price = recv_obj['lowest_52_week_price'],
                    lowest_52_week_date = recv_obj['lowest_52_week_date'],
                    market_state = recv_obj['market_state'],
                    timestamp = recv_obj['timestamp']
                )



def get_top_trade_price_coin():
    length = len(get_krw_codes_list()) 
    ticker_list = Ticker.objects.order_by('-id')[:length]
    coin_list = []

    for ticker in ticker_list:
        if ticker.acc_trade_price_24h >= 100_000_000_000:
            coin_list.append(ticker)
    
    coin_list.sort(key=lambda x: x.acc_trade_price_24h, reverse=True)
    
    return coin_list


def get_top_trade_volume_coin():
    dic = {}

    for coin in get_top_trade_price_coin():
        dic[coin] = coin.trade_volume

    top_trade_volume_coin = max(dic, key=dic.get)

    return top_trade_volume_coin


def get_coin_snapshot(code):
    url = "https://api.upbit.com/v1/ticker?markets=" + code

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()[0]