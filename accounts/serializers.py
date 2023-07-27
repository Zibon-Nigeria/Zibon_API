from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser, UserProfile


# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "account_type"]
        extra_kwargs = {
                    'password': {'write_only': True}
                }
        
    def create(self, validated_data):
        user = CustomUser.objects.create(
                                    email=validated_data['email'],
                                    account_type=validated_data['account_type']
                                )
    
        user.set_password(validated_data['password'])
        user.save()
        return user


# Store serializer
class UserProfileSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname', 'phone', 'address', 'city', 'state')



class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'password', 'account_type']
        extra_kwargs = {
                    'password': {'write_only': True}
                }
        
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email')