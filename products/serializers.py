from rest_framework import serializers

from . models import Category, Product, ProductImage, Review


# single product serializer
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'product_code', 'long_description', 'short_description', 'image')

# product image serializer
class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product_image']

# category list serializer
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name', 'short_description']

# product review serializer
class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment']
    