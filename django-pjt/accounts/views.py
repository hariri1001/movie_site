from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.response import Response


from rest_framework import status

@api_view(['POST'])
def signup(request):
    print('회원가입 요청 데이터:', request.data)  # 데이터 확인
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        print('생성된 사용자:', user)  # 생성된 사용자 확인
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UserProfileSerializer(request.user)
    print('프로필 데이터:', serializer.data)  # 데이터 확인용 로그
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    print('받은 데이터:', request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print('유효성 검사 실패:', serializer.errors)  # 에러 확인
    return Response(serializer.errors, status=400)


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