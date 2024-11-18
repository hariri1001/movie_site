# 1. User 모델 가져오기
from django.contrib.auth import get_user_model

# 2. 기본 회원가입 폼 가져오기
from django.contrib.auth.forms import UserCreationForm
# Django에서 제공하는 기본 회원가입 폼

# 3. User 모델 할당
User = get_user_model()
# get_user_model() 함수를 통해 가져온 User 모델을 User 변수에 할당

# 4. 커스텀 회원가입 폼 생성
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # 위에서 가져온 User 모델 사용
        fields = ('username', 'email', 'password1', 'password2')