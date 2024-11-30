from django.db import models
from django.conf import settings

from django.db import models
from decimal import Decimal

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # 주식 코드
    name = models.CharField(max_length=100)  # 주식 이름
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # 현재 가격
    
    # 추가 필드
    price_change = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 대비 (전일 대비 가격 차이)
    percent_change = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 등락률 (대비에 대한 백분율)

    def __str__(self):
        return self.symbol


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("BUY", "매수"),
        ("SELL", "매도"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)  # 주식
    quantity = models.PositiveIntegerField()  # 거래 수량
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 거래 당시 가격
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)  # 거래 유형
    timestamp = models.DateTimeField(auto_now_add=True)  # 거래 시간

    def __str__(self):
        return f"{self.user.nickname} {self.transaction_type} {self.quantity} {self.stock.symbol}"

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio")
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name="portfolios")
    quantity = models.PositiveIntegerField(default=0)  # 보유 수량
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('user', 'stock')  # 같은 사용자와 주식의 중복 방지

    def __str__(self):
        return f"{self.user.nickname} owns {self.quantity} of {self.stock.symbol}"