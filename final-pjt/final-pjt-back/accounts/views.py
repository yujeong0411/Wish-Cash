from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserChangeInfoSerializer, UserSerializer
# 금융상품 모델 import

# 사용자 정보 조회(프로필 페이지)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.user.username != username:
        return Response({"error" : "접근할 수 없는 페이지입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 정보 조회
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # 사용자 정보 수정
    elif request.method == 'PUT':
        serializer = UserChangeInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, username):
    # 사용자 삭제
    user = get_object_or_404(get_user_model(), username=username)
    if request.method == 'DELETE':
        if request.user.username == username:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        