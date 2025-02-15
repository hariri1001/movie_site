from rest_framework import serializers
from django.contrib.auth import get_user_model

class MyUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2  = serializers.CharField(write_only=True)
    profile_image = serializers.SerializerMethodField()
    
    # password1, 2 필드는 write_only=True로 설정
    # → 이는 비밀번호가 응답(response)에는 포함되지 않고, 
    # → 요청(request)때만 사용됨을 의미 (보안을 위해)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'profile_image')

      
    def create(self, validated_data):
            # 비밀번호 일치 검증
            if validated_data['password1'] != validated_data['password2']:
                raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
            
            # create_user 메서드 사용
            # create_user가 자동으로 비밀번호 해싱
            user = get_user_model().objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password1'],  
                first_name=validated_data.get('first_name', ''),  # first_name 저장
            )
            
            return user
    
    def get_profile_image(self, obj):  # 추가
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None



# 나의 프로필
class MyUpdateUserSerializer(serializers.ModelSerializer):
    # 비밀번호 수정시 필요
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'profile_image', 'password')
        read_only_fields = ('username',)
        
    # 비밀번호 수정
    def update(self, instance, validated_data):
        # 비밀번호 처리
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        
        # 나머지 필드 업데이트
        return super().update(instance, validated_data)
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None
    

User = get_user_model()
# 다른 사용자의 프로필
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followers_count', 'followings_count', 'is_followed', 'profile_image' )

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(pk=request.user.pk).exists()
        return False

    def get_profile_image(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None


    # 'first_name' 필드를 to_representation에서 확인
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.profile_image:
            request = self.context.get('request')
            if request:
                data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)
        
        # first_name 필드를 명시적으로 포함하도록 처리
        data['first_name'] = instance.first_name
        return data
