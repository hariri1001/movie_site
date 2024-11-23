from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

######
from django.contrib.auth import get_user_model

User = get_user_model()


# 게시글 생성 (ListCreateAPIView 대체)
@api_view(['GET', 'POST'])
def article_list_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # 현재 로그인한 사용자로 author 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세보기
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 좋아요
@api_view(['POST'])
def article_like(request, pk):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user in article.liked_users.all():
        article.liked_users.remove(request.user)
        liked = False
    else:
        article.liked_users.add(request.user)
        liked = True

    return Response({"liked": liked, "likes_count": article.liked_users.count()})

# 게시글 목록
@api_view(['GET'])
def article_list(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)

# # 로그인한 사용자의 게시글 목록
# @api_view(['GET'])
# def user_article_list(request):
#     if not request.user.is_authenticated:
#         return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
#     articles = Article.objects.filter(author=request.user)
#     serializer = ArticleSerializer(articles, many=True, context={'request': request})
#     return Response(serializer.data)

@api_view(['GET'])
def user_article_list(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # username 파라미터가 있으면 해당 사용자의 게시글을, 없으면 현재 로그인한 사용자의 게시글을 반환
    username = request.GET.get('username')
    
    if username:
        # 특정 사용자의 게시글 조회
        try:
            user = User.objects.get(username=username)
            articles = Article.objects.filter(author=user)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        # 현재 로그인한 사용자의 게시글 조회
        articles = Article.objects.filter(author=request.user)
    
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)