from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2  = serializers.CharField(write_only=True)
    # password 필드는 write_only=True로 설정
    # → 이는 비밀번호가 응답(response)에는 포함되지 않고, 
    # → 요청(request)때만 사용됨을 의미 (보안을 위해)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'password1', 'password2')