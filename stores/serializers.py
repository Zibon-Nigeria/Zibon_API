from rest_framework import serializers

from . models import Store, StoreInventory

# Store serializer
class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['balance']
        extra_kwargs = {
            'store_name': {'help_text': 'Business/Store name'},
            'store_address': {'help_text': 'Store street address'},
            # Add other fields with their descriptions
        }

class ViewStoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "store_name", "store_address", "city", "state"]


class MyStoreSerializers(serializers.ModelSerializer):    
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['owner', 'balance']


# Store inventory list serializer
class StoreInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = "__all__"
        extra_kwargs = {
            'product': {'help_text': 'Product ID'},
            # Add other fields with their descriptions
        }

# Store inventory list serializer
class ViewStoreInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = ["id", "product", "retail_price", "stock_qty"]
        depth = 1

# New Store inventory serializer
class NewStoreInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = "__all__"
        extra_kwargs = {
            'product': {'help_text': 'Product ID'},
            # Add other fields with their descriptions
        }


class MyStoreInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = '__all__'
        read_only_fields = ['store', 'product']