from django.urls import path

from exchange_rate.views import DollarRateView, ExchangeRateListView

urlpatterns = [
    # path('/get-current-usd/', DollarRateView.as_view(), name='exchange_rate_usd'),
    # path('/history/', ExchangeRateListView.as_view(), name='history'),
    ]
