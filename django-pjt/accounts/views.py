from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.response import Response


from rest_framework import status

# 회원가입
@api_view(['POST'])
def signup(request):
    print('회원가입 요청 데이터:', request.data)  # 데이터 확인
    serializer = UserSerializer(data=request.data)
    
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
    serializer = UserProfileSerializer(request.user)
    print('프로필 데이터:', serializer.data)  # 데이터 확인용 로그
    return Response(serializer.data)

#프로필 수정
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


# 프로필 이미지 업로드
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_image_upload(request):
    if 'image' not in request.FILES:
        return Response({'error': '이미지가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.profile_image = request.FILES['image']
    user.save()
    
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

