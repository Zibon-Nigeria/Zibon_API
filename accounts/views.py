# from django.shortcuts import render
# from djoser.views import UserViewSet
import profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserProfileSerializer

# from .models import CustomUser
# from .serializers import CustomUserCreateSerializer, CustomUserSerializer

# # Create your views here.

# class CustomUserViewSet(UserViewSet):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
    
# class CustomUserCreateView(UserCreateView):
#     serializer_class = CustomUserCreateSerializer
    
# class CustomTokenCreateView(TokenCreateView):
#     pass


@api_view(['GET, PUT'])
# @permission_classes([IsAuthenticated])
def my_profile(request):
    if request.method == 'PUT':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response.json({"user": "profile"})