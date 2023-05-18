from rest_framework import serializers

from . models import Category, Product, ProductImage, Review

# category list serializer
class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name', 'short_description', 'image')

# single category serializer
class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name', 'short_description', 'image')

# product list serializer
class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'short_description', 'image')

# single product serializer
class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'short_description', 'long_description', 'image')

# product image serializer
class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product_image')

# product review serializer
class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'rating', 'comment')
    