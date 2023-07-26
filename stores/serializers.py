from rest_framework import serializers

from . models import Store, StoreInventory

# Store serializer
class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ['owner', 'balance']
        extra_kwargs = {
            'store_name': {'help_text': 'Business/Store name'},
            'store_address': {'help_text': 'Store street address'},
            # Add other fields with their descriptions
        }

# Store inventory list serializer
class StoreInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        exclude = ['cost_price']
        depth = 1
        extra_kwargs = {
            'product': {'help_text': 'Product ID'},
            # Add other fields with their descriptions
        }

class MyStoreSerializers(serializers.ModelSerializer):
    def has_object_permission(self, request, obj):
        return request.user == obj.owner
    
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['owner', 'balance']
        extra_kwargs = {
            'store_name': {'help_text': 'Business/Store name'},
            'store_address': {'help_text': 'Store street address'},
            # Add other fields with their descriptions
        }


class MyStoreInventorySerializers(serializers.ModelSerializer):
    def has_object_permission(self, request, obj):
        return request.user == obj.store.owner
    
    class Meta:
        model = StoreInventory
        fields = '__all__'
        read_only_fields = ['store']
        depth = 1
        extra_kwargs = {
            'product': {'help_text': 'Product ID'},
            # Add other fields with their descriptions
        }