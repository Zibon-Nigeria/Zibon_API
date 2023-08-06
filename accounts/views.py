from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  
from drf_yasg.utils import swagger_auto_schema
from accounts.models import CustomUser

from accounts.serializers import UserSerializer

@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
def my_profile(request):
    user = CustomUser.objects.get(id=2)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response.json({"user": "profile"})