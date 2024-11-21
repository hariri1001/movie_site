from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 영화 정보 저장
    path('save/', views.save_movie, name='save_movie'),

    # 장르
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:genre_pk>/', views.genre_movies, name='genre_movies'),
    
    # 사용자(좋아요)
    path('<int:movie_id>/likes/', views.likes, name='likes'),

    # 검색
    path('search/', views.search_movies, name='search_movies'),
    
    # 영화 좋아요
    path('liked-movies/', views.user_liked_movies, name='user_liked_movies'),

    # 영화 추천
    # path('recommendations/', views.movie_recommendations, name='movie_recommendations'),
    # path('update-tags/', views.update_user_tags, name='update_user_tags'),
    # 랜덤 영화 추천
    path('random/', views.get_random_movie, name='random_movie'),

    ]

