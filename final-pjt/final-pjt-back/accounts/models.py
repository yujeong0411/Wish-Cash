from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from datetime import datetime


class User(AbstractUser):
    GENDERS = (('M', '남성'), ('W', '여성'))
    nickname = models.CharField(max_length=100, blank=True)
    realname = models.CharField(max_length=20)
    age = models.IntegerField(default=20)
    gender = models.CharField(max_length=1, choices=GENDERS)   # 성별
    birth_date = models.DateField(default='1995-04-11')   # 생년월일
    email = models.EmailField(blank=True) 
    house_bank = models.CharField(max_length=50, blank=True)  # 주거래 은행
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data

        # 기본 필드 저장
        email = data.get('email')
        username = data.get('username')

        # 이메일 설정
        if email:
            user.email = email

        # 유저네임 설정
        if username:
            user.username = username

        # 커스텀 필드 저장
        realname = data.get('realname')
        if realname:
            user.realname = realname

        age = data.get('age')
        if age is not None:
            user.age = age

        gender = data.get('gender')
        if gender:
            user.gender = gender

        birth_date = data.get('birth_date')
        if birth_date:
            if isinstance(birth_date, str):  # 문자열인 경우 변환
                try:
                    birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("올바른 날짜 형식이 아닙니다. 'YYYY-MM-DD' 형식이어야 합니다.")
            user.birth_date = birth_date

        house_bank = data.get('house_bank', '미정')  # 기본값 설정
        user.house_bank = house_bank

        nickname = data.get('nickname', '기본 닉네임')  # 기본값 설정
        user.nickname = nickname

        # 비밀번호 설정
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()

        if commit:
            user.save()

        return user