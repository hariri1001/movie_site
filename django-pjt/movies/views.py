from .models import Movie, Genre
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import MovieSerializer, GenreSerializer
from rest_framework.decorators import api_view
##################################################
import requests
from django.http import JsonResponse
from django.conf import settings




# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_movie(request):
    data = request.data
    movie, created = Movie.objects.get_or_create(
        tmdb_id=data['tmdb_id'],  # 여기를 수정
        defaults={
            'title': data['title'],
            'overview': data['overview'],
            'release_date': data['release_date'],
            'vote_count': data['vote_count'],
            'vote_average': data['vote_average'],
            'poster_path': data['poster_path']
        }
    )
    return Response({'message': 'Movie saved', 'movie_id': movie.tmdb_id})



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def likes(request, movie_id):
    movie = get_object_or_404(Movie, tmdb_id=movie_id)
    
    if request.method == 'GET':
        is_liked = request.user in movie.like_users.all()
        return Response({
            'is_liked': is_liked,
            'like_count': movie.like_users.count()
        })
        
    elif request.method == 'POST':
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        
        return Response({
            'liked': liked,
            'like_count': movie.like_users.count()
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_movies(request):
    user = request.user
    liked_movies = user.like_movies.all()
    serializer = MovieSerializer(liked_movies, many=True)
    return Response(serializer.data)

# 검색 기능
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('title', '')  # URL 파라미터에서 검색어 가져오기
    
    if query:
        # 영화 제목에 검색어가 포함된 영화들을 검색
        # icontains는 대소문자를 구분하지 않음
        movies = Movie.objects.filter(title__icontains=query)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    return Response({'message': '검색어를 입력해주세요'})


# 장르 목록
@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

# 특정 장르의 영화 목록
@api_view(['GET'])
def genre_movies(request):
    genre_id = request.GET.get('genre_id')
    
    # 전체 영화 또는 특정 장르 영화 필터링
    movies = Movie.objects.filter(genres=genre_id)
    # 영화 목록 생성
    movie_list = [{
        'title': movie.title,
        'genre': movie.genres.name,  # genres 필드 사용
    } for movie in movies]
    
    return Response({'movies': movie_list})


###################################################

def get_random_movie(request):
    # TMDB API 엔드포인트와 API 키 설정
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "sort_by": "popularity.desc",
        "page": 1
    }

    # TMDB API에 요청 보내기
    response = requests.get(url, params=params)
    data = response.json()

    # 결과에서 랜덤으로 영화 선택
    random_movie = random.choice(data["results"])

    # 필요한 영화 정보 추출
    movie_data = {
        "id": random_movie["id"],
        "title": random_movie["title"],
        "poster_path": random_movie["poster_path"],
        "overview": random_movie["overview"]
    }

    return JsonResponse(movie_data)










