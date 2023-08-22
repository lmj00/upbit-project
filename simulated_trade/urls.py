from django.urls import path
from . import views

urlpatterns =  [
    path('', views.index, name='sml-index'),
    path('order/bid', views.order_bid, name='order-bid'),
    path('order/ask', views.order_ask, name='order-ask'),
    path('history/<str:code>', views.get_history, name='get-history'),
    path('bookmark/<str:code>', views.check_bookmark, name='check-bookmark'),
]