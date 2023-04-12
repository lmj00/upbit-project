from django.contrib import messages
from django.shortcuts import render
from coin.price import get_top_trade_volume_coin
from trade.order import AccountCheck, order_bid


def trade(request):
    try: 
        if request.method == 'POST':
            if AccountCheck().get_krw() >= 5002.5:
                order_bid()
            else:
                messages.add_message(
                    request, 
                    messages.INFO, 
                    '주문가능 금액이 부족합니다.'
                )                                
    except:
        messages.add_message(
            request, 
            messages.INFO, 
            'Open API Key 관리에서 허용 IP주소를 확인해주세요.'
        )

    context = {
        'max_volume_coin': get_top_trade_volume_coin()
    }

    return render(request, 'trade/trade.html', context=context)