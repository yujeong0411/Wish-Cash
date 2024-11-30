from django.db import models
from django.conf import settings


class DepositProduct(models.Model):
    dcls_month = models.CharField(max_length=6)  # 공시 제출월
    fin_co_no = models.CharField(max_length=20)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_cd = models.CharField(max_length=50, unique=True)  # 금융 상품 코드
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    join_way = models.TextField(blank=True)  # 가입 방법
    spcl_cnd = models.TextField(blank=True)  # 우대조건
    join_deny = models.IntegerField()  # 가입 제한
    join_member = models.TextField(blank=True)  # 가입대상
    etc_note = models.TextField(blank=True)  # 기타 유의사항


class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=50)
    intr_rate_type_nm = models.CharField(max_length=100, null=True, blank=True)  # 저축 금리 유형명
    rsrv_type_nm = models.CharField(max_length=100, null=True, blank=True)  # 적립 유형명
    save_trm = models.IntegerField(null=True, blank=True)  # 저축 기간
    intr_rate = models.FloatField(null=True, blank=True)  # 저축 금리
    intr_rate2 = models.FloatField(null=True, blank=True)  # 최고 우대금리
    registered_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_deposit_users')


class SavingProduct(models.Model):
    dcls_month = models.CharField(max_length=6)  # 공시 제출월
    fin_co_no = models.CharField(max_length=20)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_cd = models.CharField(max_length=50, unique=True)  # 금융 상품 코드
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    join_way = models.TextField(blank=True)  # 가입 방법
    spcl_cnd = models.TextField(blank=True)  # 우대조건
    join_deny = models.IntegerField()  # 가입 제한
    join_member = models.TextField(blank=True)  # 가입대상
    etc_note = models.TextField(blank=True)  # 기타 유의사항


class SavingOption(models.Model):
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=50)
    intr_rate_type_nm = models.CharField(max_length=100, null=True, blank=True)  # 저축 금리 유형명
    rsrv_type_nm = models.CharField(max_length=100, null=True, blank=True)  # 적립 유형명
    save_trm = models.IntegerField(null=True, blank=True)  # 저축 기간
    intr_rate = models.FloatField(null=True, blank=True)  # 저축 금리
    intr_rate2 = models.FloatField(null=True, blank=True)  # 최고 우대금리
    registered_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_saving_users')


class Exchange(models.Model):
    cur_unit = models.CharField(max_length=10, unique=True)  # 통화 단위
    ttb = models.FloatField()  # 매입환율
    tts = models.FloatField()  # 매도환율
    cur_nm = models.CharField(max_length=50, null=True, blank=True)  # 통화명
