from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Stock, Transaction, Portfolio
from .serializers import StockSerializer, TradeRequestSerializer, TransactionSerializer, PortfolioSerializer
import requests

from django.http import JsonResponse
import logging
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)

from django.http import JsonResponse
import requests
from .models import Stock

def fetch_and_save_stock_data(request):
    BASE_URL = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService"
    ENDPOINT = "/getStockPriceInfo"
    SERVICE_KEY = "m4OMRSHGKm4DzT8pIrepzpENGfcBixkUgqyUH0uduG97i8UknpVpfArTUGGSMrqUjdHVtEP0Zy7Gjd5q1Hd69Q=="

    params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 10,
        "pageNo": 1,
        "resultType": "json",
        "basDt": "20241122",
    }

    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", params=params)
        response.raise_for_status()  # HTTP 오류 확인

        data = response.json()
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

        if not items:
            return JsonResponse({"error": "응답 데이터에 항목이 없습니다."}, status=400)

        save_results = {"updated": [], "created": []}

        for item in items:
            stock_data = {
                "symbol": item.get("srtnCd"),
                "name": item.get("itmsNm"),
                "current_price": item.get("clpr"),
                "price_change": item.get("vs"),  # 전일 대비 변화값
                "percent_change": item.get("fltRt"),  # 등락률
            }

            # `update_or_create`를 사용하여 데이터 업데이트 또는 생성
            obj, created = Stock.objects.update_or_create(
                symbol=stock_data["symbol"],  # 고유한 기준
                defaults={
                    "name": stock_data["name"],  # 종목명 업데이트
                    "current_price": stock_data["current_price"],  # 가격 업데이트
                    "price_change": stock_data["price_change"],  # 전일 대비 변화값 업데이트
                    "percent_change": stock_data["percent_change"],  # 등락률 업데이트
                },
            )

            if created:
                save_results["created"].append(stock_data)
            else:
                save_results["updated"].append(stock_data)

        return JsonResponse({
            "message": "데이터 처리 완료",
            "updated_count": len(save_results["updated"]),
            "created_count": len(save_results["created"]),
            "updated": save_results["updated"],
            "created": save_results["created"],
        }, status=200)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def stock_list(request):
    """
    모든 주식 정보를 반환합니다.
    """
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def trade(request):
    """
    매수/매도 거래를 처리합니다.
    """
    serializer = TradeRequestSerializer(data=request.data)
    if serializer.is_valid():
        stock_symbol = serializer.validated_data['stock_symbol']
        quantity = serializer.validated_data['quantity']
        transaction_type = serializer.validated_data['transaction_type']

        # 주식 정보 확인
        stock = get_object_or_404(Stock, symbol=stock_symbol)

        user = request.user

        if transaction_type == "BUY":
            total_cost = stock.current_price * quantity
            if user.balance < total_cost:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.balance -= total_cost  # 사용자 잔액 차감

            # Portfolio 업데이트 (구매 가격을 고려한 거래 처리)
            portfolio, created = Portfolio.objects.get_or_create(user=user, stock=stock)

            if created:
                portfolio.purchase_price = stock.current_price  # 처음 구매 시 가격 기록
            else:
                # 기존 포트폴리오가 있는 경우, 평균 구매 가격 업데이트
                total_quantity = portfolio.quantity + quantity
                new_purchase_price = ((portfolio.purchase_price * portfolio.quantity) + (stock.current_price * quantity)) / total_quantity
                portfolio.purchase_price = new_purchase_price

            portfolio.quantity += quantity  # 수량 업데이트
            portfolio.save()

        elif transaction_type == "SELL":
            portfolio = Portfolio.objects.filter(user=user, stock=stock).first()
            if not portfolio or portfolio.quantity < quantity:
                return Response({"error": "Not enough stock to sell"}, status=status.HTTP_400_BAD_REQUEST)

            user.balance += stock.current_price * quantity  # 판매로 인한 금액 입금
            portfolio.quantity -= quantity  # 수량 감소
            if portfolio.quantity == 0:
                portfolio.delete()  # 수량이 0이면 포트폴리오 삭제
            else:
                portfolio.save()

        user.save()

        # 거래 기록 저장
        transaction = Transaction.objects.create(
            user=user,
            stock=stock,
            quantity=quantity,
            price=stock.current_price,
            transaction_type=transaction_type,
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def portfolio_view(request):
    """
    현재 사용자의 포트폴리오를 반환합니다.
    """
    user = request.user
    portfolios = Portfolio.objects.filter(user=user)
    serializer = PortfolioSerializer(portfolios, many=True)

    return Response({
        "balance": user.balance,
        "portfolio": serializer.data,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    try:
        transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)