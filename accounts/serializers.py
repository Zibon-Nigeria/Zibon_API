from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser, UserProfile

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'account_type')
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email')

# Store serializer
class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'firstname', 'lastname', 'address', 'city', 'state')