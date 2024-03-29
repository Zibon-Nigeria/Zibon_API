from rest_framework import serializers

from stores.models import Store
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Customize JWT Claim
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['fullname'] = user.fullname
        token['is_active'] = user.is_active
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add your extra responses here
        data['has_store'] = Store.objects.filter(owner=self.user).exists()
        return data
    
    
# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "fullname", "phone", "address", "image", "account_type"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    # set email to read only on update
    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['email'].read_only = True
        return fields
    
    def create(self, validated_data):
        user = User.objects.create(
                    email=validated_data['email'],
                    fullname=validated_data['fullname'],
                    # phone=phone,
                    # address=address,
                    # account_type=validated_data['account_type'],
                )
    
        user.set_password(validated_data['password'])
        user.save()
        return user

class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'phone', 'address', 'image', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']