from urllib.parse import urlencode, unquote
from api_key import access_key, secret_key, server_url
from coin.coin import get_krw_codes_list

import jwt
import hashlib
import os
import requests
import uuid
import time


params = {}

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorization = 'Bearer {}'.format(jwt_token)
headers = {
    'Authorization': authorization,
}

res = requests.get(server_url + '/v1/accounts', params=params, headers=headers).json()


def get_krw():
    return float(res[0]['balance'])


def get_coins():
    market = get_krw_codes_list()
    coins = res[1:]
    coin_list = []

    # 거래 미지원 코인 제외
    for coin in coins:  
        currency = coin['unit_currency'] + '-' + coin['currency']

        if currency in market:
            coin_list.append(currency)
    
    return coin_list