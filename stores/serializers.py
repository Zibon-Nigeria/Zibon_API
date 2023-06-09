from rest_framework import serializers

from . models import Store, StoreInventory

# Store serializer
class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'store_name', 'store_address')

# Store inventory list serializer
class StoreInventoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = ('id', 'product', 'price')