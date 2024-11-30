from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
import requests

from django.conf import settings

from .models import DepositOption, DepositProduct, SavingOption, SavingProduct, Exchange
from .serializers import DepositOptionSerializer, DepositProductSerializer, SavingOptionSerializer, SavingProductSerializer, ExchangeSerializer

# Create your views here.
api_key = settings.API_KEY
predefined_data = []

@api_view(['GET'])
def save_deposit_products(request):
    print(api_key)
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    deposit = response.get('result')
    deposit_list = deposit.get('baseList')

    for li in deposit_list:
        fin_prdt_cd = li.get('fin_prdt_cd')

        if DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'dcls_month': li.get('dcls_month'),
            'fin_co_no': li.get('fin_co_no'),
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': li.get('kor_co_nm'),
            'fin_prdt_nm': li.get('fin_prdt_nm'),
            'etc_note': li.get('etc_note'),
            'join_deny': li.get('join_deny'),
            'join_member': li.get('join_member'),
            'join_way': li.get('join_way'),
            'spcl_cnd': li.get('spcl_cnd'),
        }

        serializer = DepositProductSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    option_list = deposit.get('optionList')
    for li in option_list:
        fin_prdt_cd = li.get('fin_prdt_cd')
        save_trm = li.get('save_trm')
        rsrv_type_nm = li.get('rsrv_type_nm')

        if DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm, rsrv_type_nm=rsrv_type_nm).exists():
            continue

        save_data = {
            'product': DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd).pk,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'rsrv_type_nm': rsrv_type_nm,
            'save_trm': int(save_trm),
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
        }

        serializer = DepositOptionSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return JsonResponse({'message': 'okay'})


@api_view(['GET'])
def deposit_products(request):
    depositproducts = DepositProduct.objects.all()
    depositproductserializer = DepositProductSerializer(depositproducts, many=True)
    return Response(depositproductserializer.data)


@api_view(['GET'])
def deposit_options(request, fin_prdt_cd):
    depositoptions = DepositOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    depositoptionserializer = DepositOptionSerializer(depositoptions, many=True)

    return Response(depositoptionserializer.data)

@api_view(['GET'])
def save_saving_products(request):
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    saving = response.get('result')
    saving_list = saving.get('baseList')

    for li in saving_list:
        fin_prdt_cd = li.get('fin_prdt_cd')

        if SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'dcls_month': li.get('dcls_month'),
            'fin_co_no': li.get('fin_co_no'),
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': li.get('kor_co_nm'),
            'fin_prdt_nm': li.get('fin_prdt_nm'),
            'etc_note': li.get('etc_note'),
            'join_deny': li.get('join_deny'),
            'join_member': li.get('join_member'),
            'join_way': li.get('join_way'),
            'spcl_cnd': li.get('spcl_cnd'),
        }

        serializer = SavingProductSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    option_list = saving.get('optionList')
    for li in option_list:
        fin_prdt_cd = li.get('fin_prdt_cd')
        save_trm = li.get('save_trm')

        if SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm).exists():
            continue

        save_data = {
            'product': SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd).pk,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': li.get('intr_rate_type_nm'),
            'rsrv_type_nm': li.get('rsrv_type_nm'),
            'save_trm': save_trm,
            'intr_rate': li.get('intr_rate'),
            'intr_rate2': li.get('intr_rate2'),
        }

        serializer = SavingOptionSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    return JsonResponse({'message': 'okay'})

@api_view(['GET', 'POST'])
def saving_products(request):
    depositproducts = SavingProduct.objects.all()
    depositproductserializer = SavingProductSerializer(depositproducts, many=True)

    return Response(depositproductserializer.data)

@api_view(['GET'])
def saving_options(request, fin_prdt_cd):
    depositoptions = SavingOption.objects.filter(fin_prdt_cd=fin_prdt_cd)
    depositoptionserializer = SavingOptionSerializer(depositoptions, many=True)

    return Response(depositoptionserializer.data)

auth_key = settings.AUTH_KEY

@api_view(['GET'])
def save_exchange(request):
    from django.db import IntegrityError

    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={auth_key}&data=AP01'
    response = requests.get(url , verify=False).json()

    for li in response:
        save_data = {
            'cur_unit': li.get('cur_unit'),
            'ttb': float(li.get('ttb').replace(',', '')) if li.get('ttb') else None,
            'tts': float(li.get('tts').replace(',', '')) if li.get('tts') else None,
            'cur_nm' : li.get('cur_nm')
        }

        try:
            # 특정 키(`cur_unit`)를 기준으로 데이터를 업데이트 또는 생성
            obj, created = Exchange.objects.update_or_create(
                cur_unit=save_data['cur_unit'],  # 고유 식별자 조건
                defaults=save_data  # 업데이트 또는 생성할 데이터
            )
            if created:
                print(f"Created new entry: {obj}")
            else:
                print(f"Updated existing entry: {obj}")
        except IntegrityError as e:
            print(f"Error processing data: {save_data}, Error: {str(e)}")

    return JsonResponse({'message': 'okay'})

@api_view(['GET'])
def exchange(request):
    exchange = Exchange.objects.all()
    exchangeSerializer = ExchangeSerializer(exchange, many=True)

    return Response(exchangeSerializer.data)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import openai

class ChatBotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # 프론트엔드에서 전달된 대화 기록과 새로운 메시지 가져오기
            chat_history = request.data.get("chat_history", [])
            user_message = request.data.get("message", "")
            
            if not user_message:
                return Response({"error": "Message is missing."}, status=400)

            # OpenAI API 키 설정
            openai.api_key = settings.GPT_KEY
            if not openai.api_key:
                return Response({"error": "OpenAI API key is not configured."}, status=500)

            # OpenAI API 호출
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=chat_history,
                temperature=0.7,
                max_tokens=2000,
            )

            bot_reply = response["choices"][0]["message"]["content"]

            # 봇 응답을 대화 기록에 추가
            chat_history.append({"role": "assistant", "content": bot_reply})

            return Response({"reply": bot_reply, "chat_history": chat_history}, status=200)

        except Exception as e:
            print(f"Error in ChatBotAPIView: {e}")
            return Response({"error": "An error occurred. Please try again."}, status=500)

from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # 토큰 인증 추가
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def subscribed(request):
    """
    특정 옵션에 대해 구독 처리
    """
    user = request.user  # 이제 인증된 사용자 정보를 얻을 수 있습니다
    option_id = request.data.get('optionId')

    try:
        if request.data.get('optionType'):
            deposit_option = DepositOption.objects.filter(id=option_id).first()
            if deposit_option:
                deposit_option.registered_user.add(user)
                return Response(
                    {'message': f'예금 옵션 {deposit_option.fin_prdt_cd}에 구독 성공'}, 
                    status=status.HTTP_201_CREATED
                )
        else:
            saving_option = SavingOption.objects.filter(id=option_id).first()
            if saving_option:
                saving_option.registered_user.add(user)
                return Response(
                    {'message': f'적금 옵션 {saving_option.fin_prdt_cd}에 구독 성공'}, 
                    status=status.HTTP_201_CREATED
                )
        
        return Response({'error': '옵션을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
import numpy as np

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscribed_list(request):
    """
    회원이 가입한 옵션 리스트와 예금 및 적금 차트 데이터 가져오기
    """
    user = request.user
    print(request.query_params)
    option_type = request.query_params.get('type')  # type 파라미터 가져오기 (deposit or saving)
    print(2)

    # type 유효성 검사
    if option_type not in ["deposit", "saving"]:
        return Response({"error": "Invalid type parameter. Must be 'deposit' or 'saving'."}, status=400)

    try:
        # 예금 및 적금 옵션 가져오기
        deposit_options = user.registered_deposit_users.all()
        saving_options = user.registered_saving_users.all()

        # 예금 리스트
        deposit_list = [
            {
                'id': option.id,
                'bank_name': option.product.kor_co_nm,
                'product_name': option.product.fin_prdt_nm,
                'fin_prdt_cd': option.fin_prdt_cd,
                'save_trm': option.save_trm,
                'intr_rate': option.intr_rate,
                'intr_rate2': option.intr_rate2,
            }
            for option in deposit_options
        ]

        # 적금 리스트
        saving_list = [
            {
                'id': option.id,
                'bank_name': option.product.kor_co_nm,
                'product_name': option.product.fin_prdt_nm,
                'fin_prdt_cd': option.fin_prdt_cd,
                'save_trm': option.save_trm,
                'intr_rate': option.intr_rate,
                'intr_rate2': option.intr_rate2,
            }
            for option in saving_options
        ]

        # 선택된 리스트와 차트 데이터 처리
        if option_type == "deposit":
            selected_list = deposit_list
        else:  # saving
            selected_list = saving_list

        selected_chart_data = {
            "labels": [item["product_name"] for item in selected_list],
            "datasets": [
                {"label": "기본 금리 (%)", "data": [item["intr_rate"] for item in selected_list]},
                {"label": "우대 금리 (%)", "data": [item["intr_rate2"] for item in selected_list]},
            ],
        }

        # 응답 데이터 반환
        return Response({
            "data": selected_list,
            "selected_chart": selected_chart_data,
        }, status=200)

    except Exception as e:
        logger.error(f"Error processing subscribed_list: {e}")
        return Response({'error': 'An unexpected error occurred.'}, status=500)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # 토큰 인증 추가
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def unsubscribe(request):
    """
    특정 옵션 구독 취소
    """
    print(request.query_params.get('optionType'))
    user = request.user  # 인증된 사용자 정보
    option_id = request.query_params.get('optionId')  # 옵션 ID
    option_type = request.query_params.get('optionType')  # 옵션 타입
    print('#', option_type)

    try:
        if option_type == "deposit":  # 예금 구독 취소
            deposit_option = DepositOption.objects.filter(id=option_id).first()
            if deposit_option and user in deposit_option.registered_user.all():
                deposit_option.registered_user.remove(user)
                return Response(
                    {'message': f'예금 옵션 {deposit_option.fin_prdt_cd} 구독 취소 성공'},
                    status=status.HTTP_200_OK
                )
        elif option_type == "saving":  # 적금 구독 취소
            saving_option = SavingOption.objects.filter(id=option_id).first()
            if saving_option and user in saving_option.registered_user.all():
                print(1)
                saving_option.registered_user.remove(user)
                print(2)
                return Response(
                    {'message': f'적금 옵션 {saving_option.fin_prdt_cd} 구독 취소 성공'},
                    status=status.HTTP_200_OK
                )
        else:
            return Response({'error': '옵션을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import get_user_model
from collections import Counter

User = get_user_model()

def get_similar_age_products(request):
    try:
        user = request.user
        user_age = request.GET.get('age')  # URL 파라미터에서 age 값을 가져오기

        if not user_age:
            return JsonResponse({"error": "Age not provided"}, status=400)

        # 같은 나이대 (±5년) 사용자 찾기
        age_range_start = int(user_age) - 5
        age_range_end = int(user_age) + 5

        similar_users = User.objects.filter(age__gte=age_range_start, age__lte=age_range_end)

        # 전체 가입자에서 데이터 수집
        all_deposit_options = DepositOption.objects.all()
        all_saving_options = SavingOption.objects.all()

        # 같은 나이대 사용자에서 데이터 수집
        similar_age_deposit_options = DepositOption.objects.filter(registered_user__in=similar_users)
        similar_age_saving_options = SavingOption.objects.filter(registered_user__in=similar_users)

        # 전체 가입자 데이터 수집
        def collect_products(options):
            products = {}
            for option in options:
                product_code = option.product.fin_prdt_cd
                if product_code not in products:
                    products[product_code] = {
                        "product_name": option.product.fin_prdt_nm,
                        "bank_name": option.product.kor_co_nm,
                        "intr_rate": option.intr_rate,
                        "intr_rate2": option.intr_rate2,
                        "product_code": product_code,
                        "highest_intr_rate2": option.intr_rate2,  # 최고 우대 금리 초기값
                        "count": 0  # 초기 가입자 수
                    }
                # 최고 우대 금리 업데이트
                products[product_code]["highest_intr_rate2"] = max(products[product_code]["highest_intr_rate2"], option.intr_rate2)
                # 가입자 수 증가
                products[product_code]["count"] += 1
            return products

        all_deposit_products = collect_products(all_deposit_options)
        all_saving_products = collect_products(all_saving_options)
        similar_age_deposit_products = collect_products(similar_age_deposit_options)
        similar_age_saving_products = collect_products(similar_age_saving_options)

        # 전체 가입자 상위 3개 추출
        top_all_deposit_products = sorted(all_deposit_products.values(), key=lambda x: x["count"], reverse=True)[:3]
        top_all_saving_products = sorted(all_saving_products.values(), key=lambda x: x["count"], reverse=True)[:3]

        # 같은 나이대 사용자 상위 3개 추출
        top_similar_age_deposit_products = sorted(similar_age_deposit_products.values(), key=lambda x: x["count"], reverse=True)[:3]
        top_similar_age_saving_products = sorted(similar_age_saving_products.values(), key=lambda x: x["count"], reverse=True)[:3]

        return JsonResponse({
            "data": {
                "top_all_deposit_products": top_all_deposit_products,
                "top_all_saving_products": top_all_saving_products,
                "top_similar_age_deposit_products": top_similar_age_deposit_products,
                "top_similar_age_saving_products": top_similar_age_saving_products
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


