from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('articles/', views.article_list_create, name='article_list_create'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:pk>/like/', views.article_like, name='ArticleLike'),
    path('articles/list/', views.article_list, name='article_list'),
    path('articles/user/', views.user_article_list, name='user_article_list'),
    

]
