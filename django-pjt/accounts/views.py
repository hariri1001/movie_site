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

