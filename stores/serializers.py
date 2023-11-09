from rest_framework import serializers

from . models import Category, ProductImage, Review, Store, StoreProduct

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

# product image serializer
class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

# Store inventory list serializer
class StoreProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializers(many=True, read_only=True)
    class Meta:
        model = StoreProduct
        fields = "__all__"

# Store inventory list serializer
class ViewStoreProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializers(many=True, read_only=True)
    class Meta:
        model = StoreProduct
        exclude = ["store", "cost_price", "created_at", "updated_at"]
        depth = 1

# my Store Pproduc
class MyStoreProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = '__all__'
        read_only_fields = ['store']

# category list serializer
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'store', 'slug', 'name', 'short_description']
        # read_only_fields = ['store']

# product review serializer
class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment']