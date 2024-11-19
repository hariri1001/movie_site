from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 영화 정보 저장
    path('save/', views.save_movie, name='save_movie'),

    # 장르 관련 URL
    # path('genres/', views.genre_list, name='genre_list'),
    # path('genres/<int:genre_pk>/', views.genre_movies, name='genre_movies'),
    
    # 사용자 관련 URL
    path('<int:movie_id>/likes/', views.likes, name='likes'),

    # 검색 및 추천
    path('search/', views.search_movies, name='search_movies'),
    
    # 영화 좋아요
    path('liked-movies/', views.user_liked_movies, name='user_liked_movies'),


]

