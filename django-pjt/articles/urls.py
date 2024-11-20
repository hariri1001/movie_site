from django.urls import path
from .views import ArticleListCreateAPIView, ArticleDetailAPIView

urlpatterns = [
    path('articles/', ArticleListCreateAPIView.as_view(), name='article_list_create'),
    path('articles/<int:pk>/', ArticleDetailAPIView.as_view(), name='article_detail'),
]
