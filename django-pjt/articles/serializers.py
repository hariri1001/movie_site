from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 
            'rating', 'created_at', 'likes_count', 
            'is_liked', 'liked_users',
            # 영화 관련 필드 명시적으로 추가
            'movie_id', 'movie_title', 'movie_poster_path', 
            'movie_release_date', 'movie_overview'
        ]
        read_only_fields = ['author', 'liked_users']

    def get_is_liked(self, obj):
        """
        현재 요청한 사용자가 게시글을 좋아요 했는지 여부 반환
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.liked_users.all()
        return False
    
    def create(self, validated_data):
        """
        영화 정보를 포함하여 게시글 생성
        """
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        영화 정보를 포함하여 게시글 수정
        """
        instance = super().update(instance, validated_data)
        return instance

    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'article']
        read_only_fields = ('author', 'article')