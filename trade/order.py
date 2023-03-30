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