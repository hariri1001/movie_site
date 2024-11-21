from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='liked_users.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def get_is_liked(self, obj):
        """
        현재 요청한 사용자가 게시글을 좋아요 했는지 여부 반환
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.liked_users.all()
        return False