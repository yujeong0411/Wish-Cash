from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer, TokenSerializer, TokenModel
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
# 금융상품 시리얼라이저 받아오기

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('nickname','username', 'realname', 'age', 'email', 'gender','birth_date', 'house_bank')

# 로그인
class CustomLoginSerializer(LoginSerializer):
    # email로 로그인 하지 않을 것임.
    email = None   
  



# 회원가입 
class CustomRegisterSerializer(RegisterSerializer):
    # email = None
    # email, username, password1/2는 기본 데이터
    realname = serializers.CharField(required=True, max_length=20)
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=20)
    age = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    GENDER_CHOICES = (('M', '남성'), ('W', '여성'))  # 성별 선택지 정의
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)  # ChoiceField로 변경
    birth_date = serializers.DateField(required=True)
    house_bank = serializers.CharField(required=False, allow_blank=True)
   

    # 주거래 은행 유효성 검증 추가
    def validate_house_bank(self, value):
        # if not value.strip():  # 입력이 비어 있거나 공백만 있는 경우
        #     raise serializers.ValidationError("주거래 은행은 반드시 입력해야 합니다.")
        if len(value.split(',')) > 1:  # 쉼표로 여러 항목이 입력된 경우
            raise serializers.ValidationError("주거래 은행은 한 개만 입력 가능합니다.")
        return value

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value


    # # 이메일 설정 관련해서 지속적 오류남. -> django에서 오류 (원래 자주 발생)
    # def validate_email(self, value):
    #     User = get_user_model()
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("이미 사용중인 이메일입니다.")
    #     return value

    def get_cleaned_data(self):
        # super() : 부모클래스 호출 매서드 
        data_dict = super().get_cleaned_data()

        # validated_data : 유효성 검사를 통과한 데이터(dict)
        # 해당 키의 값이 아니면 none 반환 
        data_dict['realname'] = self.validated_data.get('realname', None) 
        data_dict['username'] = self.validated_data.get('username', None)  
        data_dict['age'] = self.validated_data.get('age', None)
        data_dict['gender'] = self.validated_data.get('gender', None)
        data_dict['birth_date'] = self.validated_data.get('birth_date', None)
        data_dict['house_bank'] = self.validated_data.get('house_bank', None)
        data_dict['nickname'] = self.validated_data.get('nickname', None)
        return data_dict
    
    # 데이터 베이스에 저장 
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        user.realname = self.cleaned_data.get('realname')
        user.username = self.cleaned_data.get('username')
        user.age = self.cleaned_data.get('age')
        user.gender = self.cleaned_data.get('gender')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.house_bank = self.cleaned_data.get('house_bank')
        user.nickname = self.cleaned_data.get('nickname')
        user.save()
        return user
    

# 토큰 정보 생성 시 사용자 정보를 포함하도록 확장 
class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TokenModel
        fields = ('key', 'user',)


# 사용자 정보 수정
class UserChangeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('age', 'email', 'gender','birth_date', 'house_bank', 'nickname',)

