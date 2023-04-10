from urllib.parse import urlencode, unquote
from coin.price import get_top_trade_volume_coin, get_coin_snapshot

import jwt
import hashlib
import os
import requests
import uuid
import time

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

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers).json()

    if len(get_wait_order_value()) > 0 and res['uuid'] == get_wait_order_value()[0]['uuid']:
        order_cancel(res['uuid'])
    else:
        order_ask()


def order_ask():
    while True:
        gcov = get_complete_order_value()
        gcov_price = float(gcov['price'])

        gcs = get_coin_snapshot(gcov['market'])
        rate_of_return = (gcs['trade_price'] - gcov_price) / gcov_price * 100
        
        if rate_of_return >= 1:
            params = {
                'market': gcs['market'],
                'side': 'ask',
                'ord_type': 'limit',
                'price': gcs['trade_price'],
                'volume': gcs['executed_volume'] - gcs['executed_volume'] * 0.0005  
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

        time.sleep(0.01)


def get_wait_order_value():
    params = {
    'states[]': ['wait']
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

    res = requests.get(server_url + '/v1/orders', params=params, headers=headers).json()

    return res


def get_complete_order_value():
    params = {
    'states[]': ['done']
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

    res = requests.get(server_url + '/v1/orders', params=params, headers=headers).json()

    return res[0]


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