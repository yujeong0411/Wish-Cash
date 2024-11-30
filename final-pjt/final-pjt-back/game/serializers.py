from rest_framework import serializers
from .models import Stock, Transaction, Portfolio

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'current_price', 'price_change', 'percent_change']

class TransactionSerializer(serializers.ModelSerializer):
    stock = serializers.CharField(source='stock.name', read_only=True)  # ForeignKey를 symbol로 변환

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'stock', 'quantity', 'price', 'transaction_type', 'timestamp']
        read_only_fields = ['user', 'price', 'timestamp']

class TradeRequestSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField(max_length=10)
    quantity = serializers.IntegerField(min_value=1)
    transaction_type = serializers.ChoiceField(choices=["BUY", "SELL"])

class PortfolioSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="stock.symbol", read_only=True)
    stock_name = serializers.CharField(source="stock.name", read_only=True)
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'stock_symbol', 'stock_name', 'quantity', 'purchase_price']
        read_only_fields = ['user']