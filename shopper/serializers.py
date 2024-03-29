from rest_framework import serializers

from shopper.models import BankInfo, ShopperPersonalInfo, ShopperProfile

class ShopperProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopperProfile
        fields = '__all__'
        read_only_fields = ['user', 'balance']
        depth = 1
        

class ShopperPersonalInfoSerializer(serializers.ModelSerializer):
    id_document = serializers.FileField(max_length=None, use_url=True)
    picture = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = ShopperPersonalInfo
        fields = '__all__'


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = '__all__'