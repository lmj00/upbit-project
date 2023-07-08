from django.test import TestCase, Client
from django.urls import reverse

from .models import Account

import json


class TestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create(
            currency='KRW',
            balance=100_000_000,
            avg_buy_price=0.0,
            unit_currency='KRW'
        )

        Account.objects.create(
            currency='BTC',
            balance=1,
            avg_buy_price=30_000_000,
            unit_currency='KRW'
        )


    def test_order_bid(self):
        c = Client()
        url = reverse('order-bid')

        data = {
            'in_name': '비트코인',
            'in_price': 30_000_000,
            'in_quantity': 1,
            'in_total': 30_000_000
        }

        json_data = json.dumps(data)

        response = c.post(
            url,
            data=json_data,
            content_type='application/json',
        )

        response_data = json.loads(response.content)
        message = response_data['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, '매수주문이 완료되었습니다.')


    def test_order_ask(self):
        c = Client()
        url = reverse('order-ask')

        data = {
            'in_name': '비트코인',
            'in_price': 30_000_000,
            'in_quantity': 1,
            'in_total': 30_000_000
        }

        json_data = json.dumps(data)

        response = c.post(
            url,
            data=json_data,
            content_type='application/json',
        )

        response_data = json.loads(response.content)
        message = response_data['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, '매도주문이 완료되었습니다.')