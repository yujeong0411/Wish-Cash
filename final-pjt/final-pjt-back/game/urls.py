from django.urls import path
from .views import stock_list, trade, portfolio_view, transaction_history, fetch_and_save_stock_data

urlpatterns = [
    path('stocks/', stock_list),
    path('trade/', trade),
    path('portfolio/', portfolio_view,),
    path('fetch-and-save-stock-data/', fetch_and_save_stock_data),
    path('transactions/', transaction_history),
]