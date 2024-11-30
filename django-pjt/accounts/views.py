from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, MyUserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


# 회원가입
@api_view(['POST'])
def signup(request):
    print('회원가입 요청 데이터:', request.data)  # 데이터 확인
    serializer = MyUserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        print('생성된 사용자:', user)  # 생성된 사용자 확인
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 프로필
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UserProfileSerializer(request.user, context={'request': request})
    print('프로필 데이터:', serializer.data)  # 데이터 확인용 로그
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user
    print('받은 데이터:', request.data)
    
    if 'password' in request.data and request.data['password']:
        user.set_password(request.data['password'])

    serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print('유효성 검사 실패:', serializer.errors)
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_image_upload(request):
    if 'image' not in request.FILES:
        return Response({'error': '이미지가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = request.user
        user.profile_image = request.FILES['image']
        user.save()
        
        serializer = UserProfileSerializer(user, context={'request': request})
        print('업로드된 이미지 URL:', user.profile_image.url if user.profile_image else None)  # 로그 추가
        return Response(serializer.data)
    except Exception as e:
        print('이미지 업로드 에러:', str(e))  # 에러 로깅
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    # UserProfileSerializer 사용
    serializer = UserProfileSerializer(user, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, username):
    you = get_object_or_404(User, username=username)
    me = request.user
    
    if you != me:
        if me.followings.filter(pk=you.pk).exists():
            me.followings.remove(you)
            is_followed = False
        else:
            me.followings.add(you)
            is_followed = True
        
        return Response({
            'is_followed': is_followed,
            'followers_count': you.followers.count(),
            'followings_count': you.followings.count(),
        })
    return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=400)