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

    # def validate(self, data):
    #     if data['password1'] != data['password2']:
    #         raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
    #     return data        
    def create(self, validated_data):
            # 비밀번호 일치 검증
            if validated_data['password1'] != validated_data['password2']:
                raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
            
            # create_user 메서드 사용
            user = get_user_model().objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password1'],  # create_user가 자동으로 비밀번호 해싱
                first_name=validated_data.get('first_name', ''),  # first_name 저장
            )
            
            return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'profile_image')
        read_only_fields = ('username',)