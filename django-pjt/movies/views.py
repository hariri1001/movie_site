from django.shortcuts import render
from .models import Movie, Genre
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import MovieSerializer, GenreSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.like_users.filter(pk=user.pk).exists():
        # 이미 좋아요 한 경우 -> 좋아요 취소
        movie.like_users.remove(user)
        liked = False
    else:
        # 좋아요 하지 않은 경우 -> 좋아요 추가
        movie.like_users.add(user)
        liked = True

    return Response({
        'liked': liked,
        'like_count': movie.like_users.count()
    })


# 사용자가 좋아요한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    movies = request.user.like_movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 검색 (제목 기준)
@api_view(['GET'])
def search_movies(request):
    query = request.query_params.get('query', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    return Response([])

# 장르 목록
@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

# 특정 장르의 영화 목록
@api_view(['GET'])
def genre_movies(request, genre_pk):
    movies = Movie.objects.filter(genre_ids=genre_pk)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)