from rest_framework import serializers
from .models import DepositProduct, SavingProduct, DepositOption, SavingOption, Exchange

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('registered_user',)

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'  # 명시적으로 모든 필드를 포함
        read_only_fields = ('registered_user',)  # ForeignKey는 읽기 전용으로 설정

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

class RegisteredSerializer(serializers.Serializer):
    option_pk = serializers.IntegerField(required=True)
    f = serializers.BooleanField(required=True)  # True: 예금, False: 적금
