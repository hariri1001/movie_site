from django.urls import path
from .views import (
    ArticleListCreateAPIView, 
    ArticleDetailAPIView, 
    UserArticleListAPIView, 
    ArticleLikeAPIView, 
    ArticleListAPIView
)

urlpatterns = [
    path('articles/', ArticleListCreateAPIView.as_view(), name='article_list_create'),
    path('articles/<int:pk>/', ArticleDetailAPIView.as_view(), name='article_detail'),
    path('articles/user/', UserArticleListAPIView.as_view(), name='user_articles'),
    path('articles/<int:pk>/like/', ArticleLikeAPIView.as_view(), name='article_like'),
    path('articles/list/', ArticleListAPIView.as_view(), name='article_list'),
]
