from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Profile, LikedMovie

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')

    if password1 != password2:
        return Response({'error': '비밀번호가 불일치 합니다. 다시 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password1'))
        user.save()
        # 회원가입 시 프로필 자동 생성
        Profile.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile = request.user.profile
    profile_serializer = ProfileSerializer(profile)
    liked_movies = LikedMovie.objects.filter(user=request.user)
    movie_serializer = MovieSerializer(liked_movies, many=True)

    data = {
        'profile': profile_serializer.data,
        'liked_movies': movie_serializer.data
    }
    return Response(data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     user = request.user
#     old_password = request.data.get('old_password')
#     new_password = request.data.get('new_password')

#     if not user.check_password(old_password):
#         return Response({'error': '현재 비밀번호가 일치하지 않습니다.'}, 
#                       status=status.HTTP_400_BAD_REQUEST)

#     user.set_password(new_password)
#     user.save()
#     return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def toggle_follow(request, user_id):
#     try:
#         target_profile = Profile.objects.get(user_id=user_id)
#         my_profile = request.user.profile

#         if my_profile.followers.filter(id=target_profile.id).exists():
#             my_profile.followers.remove(target_profile)
#             followed = False
#         else:
#             my_profile.followers.add(target_profile)
#             followed = True

#         return Response({
#             'status': 'success',
#             'followed': followed,
#             'followers_count': target_profile.get_followers_count()
#         })
#     except Profile.DoesNotExist:
#         return Response({'error': '사용자를 찾을 수 없습니다.'}, 
#                       status=status.HTTP_404_NOT_FOUND)