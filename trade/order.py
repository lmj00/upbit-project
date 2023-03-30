from urllib.parse import urlencode, unquote
from coin.price import get_top_trade_volume_coin
import jwt
import hashlib
import os
import requests
import uuid

access_key = ''
secret_key = ''
server_url = 'https://api.upbit.com'


def get_krw():
    params = {
        
    }

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

    return float(res[0]['balance'])


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

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
    res.json()