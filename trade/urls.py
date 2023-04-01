from django.urls import path
from .views import trade

urlpatterns = [
    path('', trade, name='trade'),
]
