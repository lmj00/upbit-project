from django.urls import path
from . import views

urlpatterns =  [
    path('', views.index, name='sml-index'),
    path('order/bid', views.order_bid, name='order-bid'),
    path('order/ask', views.order_ask, name='order-ask'),
    path('code/<str:code>', views.code, name='code')
]