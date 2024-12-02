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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.conf import settings
import requests


from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()


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
def user_liked_movies(request, username=None):
    try:
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        
        liked_movies = user.like_movies.all()
        serializer = MovieSerializer(liked_movies, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

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


###########################################

TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# 장르 ID 매핑
genre_mapping = {
    "액션": 28,
    "로맨스": 10749,
    "공포": 27,
    "코미디": 35,
    "SF": 878
}

@csrf_exempt
@require_http_methods(["POST"])
def recommend_movies(request):
   try:
       data = json.loads(request.body)
       genre = data.get('0')
       
       # JWT 토큰으로 인증 헤더 설정
       headers = {
           'Authorization': f'Bearer {settings.VITE_TMDB_API_KEY}',
           'accept': 'application/json'
       }
       
       response = requests.get(
           f'{TMDB_BASE_URL}/discover/movie', # TMDB API의 영화 검색 URL
           headers=headers,  # Bearer 인증 사용 - 헤더 추가
           params={
               'language': 'ko-KR',
               'sort_by': 'popularity.desc',
               'with_genres': genre_mapping.get(genre, '28'),
               'page': 1
           }
       )
       
       print(f"Response status: {response.status_code}") # 디버깅
       print(f"Response content: {response.text}") # 디버깅
       
       # TMDB에서 반환된 영화 목록을 파싱하여 상위 5개 영화만 선택
       movies = response.json().get('results', [])[:5]

       recommendations = [{
           'title': movie['title'],
           'rating': movie['vote_average'],
           'overview': movie.get('overview', '등록된 줄거리가 없습니다.'),
           'poster_path': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
       } for movie in movies]

        # 추천 목록을 JSON 형식으로 반환
       return JsonResponse(recommendations, safe=False)
   except Exception as e:
       print(f"Error: {type(e).__name__}, {str(e)}")
       return JsonResponse({'error': str(e)}, status=400)










