# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

class ArticleListCreateAPIView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)# 현재 로그인한 사용자로 author 설정


class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class UserArticleListAPIView(ListAPIView):
    """
    현재 로그인한 사용자가 작성한 게시글 목록 반환
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)  # 현재 사용자 게시글만 반환
    
class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            article = Article.objects.get(pk=pk)
            if request.user in article.liked_users.all():
                article.liked_users.remove(request.user)
                liked = False
            else:
                article.liked_users.add(request.user)
                liked = True
            # 디버깅용 출력
            print("현재 좋아요 개수:", article.liked_users.count())
            return Response({"liked": liked, "likes_count": article.liked_users.count()})
        except Article.DoesNotExist:
            return Response({"error": "Article not found."}, status=404)


class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(
            articles, many=True, context={'request': request}
        )
        return Response(serializer.data)