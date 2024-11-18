from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('movies/<int:movie_pk>/like/', views.movie_like, name='movie_like'),

    # 장르 관련 URL
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:genre_pk>/', views.genre_movies, name='genre_movies'),
    
    # 사용자 관련 URL
    path('liked/', views.liked_movies, name='liked_movies'),
    
    # 검색 및 추천
    # path('search/', views.search_movies, name='search_movies'),
    # path('recommended/', views.recommended_movies, name='recommended_movies'),
]


