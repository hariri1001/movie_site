
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Genre

# 장르
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


# 좋아요 기능 관련
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class MovieSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.like_users.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False