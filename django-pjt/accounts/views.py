from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password1 = request.data.get('password1')
    password2 = request.data.get('passwordConfirmation')

    if password1 != password2:
        return Response({'error': '비밀번호가 불일치 합니다. 다시 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # set_password로 비밀번호 암호화
        user.set_password(request.data.get('password1'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)