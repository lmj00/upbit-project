from django.shortcuts import render
from coin.price import get_top_trade_volume_coin
from trade.order import get_krw, order_bid


def trade(request):
    if request.method == 'POST':
        if get_krw() >= 5002.5:
            order_bid()
        else:
            print("최소 주문 금액이 부족합니다.")

                
    context = {
        'max_volume_coin': get_top_trade_volume_coin()
    }

    return render(request, 'trade/test.html', context=context)