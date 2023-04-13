from urllib.parse import urlencode, unquote
from api_key import access_key, secret_key, server_url
from coin.coin import get_top_trade_volume_coin
from order.order_list import get_wait_order_value
from trade.accounts import get_krw

import jwt
import hashlib
import os
import requests
import uuid


def order_bid():
    coin = get_top_trade_volume_coin()

    params = {
        'market': coin.code,
        'side': 'bid',
        'ord_type': 'limit',
        'price': coin.trade_price,
        'volume': (get_krw() - get_krw() * 0.0005) / coin.trade_price
    }

    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization, 
    }

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers).json()

    if len(get_wait_order_value()) > 0 and res['uuid'] == get_wait_order_value()[0]['uuid']:
        order_cancel(res['uuid'])
    else:
        order_ask()

'''
수정 중
'''
def order_ask(coin):
    params = {
        'market': coin['market'],
        'side': 'ask',
        'ord_type': 'limit',    
        'price': coin['trade_price'],
        'volume': coin['executed_volume'] - coin['executed_volume'] * 0.0005  
    }

    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers).json()

    return res


def order_cancel(order_uuid):
    params = {
    'uuid': order_uuid
    }

    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.delete(server_url + '/v1/order', params=params, headers=headers)