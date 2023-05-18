from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'password', 'firstname', 'lastname', 'address', 'city', 'state')
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'firstname', 'lastname', 'address', 'city', 'state')
