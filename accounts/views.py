from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  
from drf_yasg.utils import swagger_auto_schema

from accounts.serializers import MyTokenObtainPairSerializer, UserSerializer, ViewUserSerializer

@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        token = MyTokenObtainPairSerializer.get_token(user)

        user_data = ViewUserSerializer(user)
    
        return Response({
                "user": user_data.data,
                'access': str(token.access_token),
                'refresh': str(token)
            }, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = ViewUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    