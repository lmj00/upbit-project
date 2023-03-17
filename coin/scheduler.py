from apscheduler.schedulers.background import BackgroundScheduler
import requests
from .models import Ticker


def getTicker():
    url = "https://api.upbit.com/v1/market/all?isDetails=false"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    for res in response.json():
        market = res['market']
        
        if market[:3] == 'KRW':
            url = 'https://api.upbit.com/v1/ticker?markets=' + market
            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)
            data = response.json()[0]

            Ticker.objects.create(
                    market = data['market'],
                    trade_date = data['trade_date'],
                    trade_time = data['trade_time'],
                    trade_date_kst = data['trade_date_kst'],
                    trade_time_kst = data['trade_time_kst'],
                    trade_timestamp = data['trade_timestamp'],
                    opening_price = data['opening_price'],
                    high_price = data['high_price'],
                    low_price = data['low_price'],
                    trade_price = data['trade_price'],
                    prev_closing_price = data['prev_closing_price'],
                    change = data['change'],
                    change_price = data['change_price'],
                    change_rate = data['change_rate'],
                    signed_change_price = data['signed_change_price'],
                    signed_change_rate = data['signed_change_rate'],
                    trade_volume = data['trade_volume'],
                    acc_trade_price = data['acc_trade_price'],
                    acc_trade_price_24h = data['acc_trade_price_24h'],
                    acc_trade_volume = data['acc_trade_volume'],
                    acc_trade_volume_24h = data['acc_trade_volume_24h'],
                    highest_52_week_price = data['highest_52_week_price'],
                    highest_52_week_date = data['highest_52_week_date'],
                    lowest_52_week_price = data['lowest_52_week_price'],
                    lowest_52_week_date = data['lowest_52_week_date'],
                    timestamp = data['timestamp']
            )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getTicker, 'interval', minutes=1)
    scheduler.start()