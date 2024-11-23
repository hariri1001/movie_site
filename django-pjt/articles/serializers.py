from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'liked_users']

    def get_is_liked(self, obj):
        """
        현재 요청한 사용자가 게시글을 좋아요 했는지 여부 반환
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.liked_users.all()
        return False
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'article']
        read_only_fields = ('author', 'article')