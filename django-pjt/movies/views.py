from .models import Movie
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import MovieSerializer
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def likes(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
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









# # 장르 목록
# @api_view(['GET'])
# def genre_list(request):
#     genres = Genre.objects.all()
#     serializer = GenreSerializer(genres, many=True)
#     return Response(serializer.data)

# # 특정 장르의 영화 목록
# @api_view(['GET'])
# def genre_movies(request, genre_pk):
#     movies = Movie.objects.filter(genre_ids=genre_pk)
#     serializer = MovieSerializer(movies, many=True)
#     return Response(serializer.data)