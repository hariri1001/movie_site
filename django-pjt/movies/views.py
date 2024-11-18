from django.shortcuts import render
from .models import Movie, Genre
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import MovieSerializer, GenreSerializer
from django.views.decorators.http import require_POST
# from django.views.decorators.http import require_POST
from django.http.response import HttpResponse, JsonResponse

# Create your views here.
@api_view(['POST'])
def save_movie(request):
    data = request.data
    movie = Movie.objects.create(
        id=data['id'],  # TMDB ID 사용
        title=data['title'],
        overview=data['overview'],
        release_date=data['release_date'],
        vote_count=data['vote_count'],
        vote_average=data['vote_average'],
        poster_path=data['poster_path']
    )
    return Response({'message': 'Movie saved'})



@api_view(['POST', 'GET'])
def likes(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        
        if request.method == 'GET':
            return Response({
                'is_liked': movie.like_users.filter(pk=request.user.pk).exists(),
                'count': movie.like_users.count()
            })
            
        # POST 처리
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        return Response({
            'liked': liked,
            'count': movie.like_users.count()
        })
    return Response(status=401)





# 영화 검색 (제목 기준)
# @api_view(['GET'])
# def search_movies(request):
#     query = request.query_params.get('query', '')
#     if query:
#         movies = Movie.objects.filter(title__icontains=query)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     return Response([])

# 검색기능
@api_view(['GET'])
def movie_search(request):
    query = request.GET.get('q', '')  # 검색어를 가져옵니다. 기본값은 빈 문자열입니다.
    
    if query:
        # 검색어가 있을 경우 영화 제목과 줄거리를 대상으로 필터링합니다.
        movies = Movie.objects.filter(title__icontains=query) | Movie.objects.filter(overview__icontains=query)
        
        if movies.exists():
            serializer = MovieSerializer(movies, many=True)  # 직렬화합니다.
            return Response(serializer.data)
        else:
            return Response({"message": "검색 영화가 없습니다."}, status=404)  # 결과가 없을 경우 404 상태 코드 반환
    else:
        return Response({"message": "검색어를 입력해 주세요."}, status=400)





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