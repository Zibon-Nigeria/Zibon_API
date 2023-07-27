from rest_framework import serializers

from shopper.models import BankInfo, Delivery, ShopperPersonalInfo, ShopperProfile

class ShopperProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopperProfile
        fields = '__all__'
        read_only_fields = ['balance']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ['shopper', 'order', 'destination']
        # extra_kwargs = {
        #     'shopper': {'read_only': True},
        #     'order': {'read_only': True},
        #     'destination': {'read_only': True}
        # }


class ShopperPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopperPersonalInfo
        fields = '__all__'


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = '__all__'
        read_only_fields = ['shopper']