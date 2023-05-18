from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import CategoryDetailSerializers, CategoryListSerializers, ProductDetailSerializers, ProductImageSerializers, ProductListSerializers, ReviewListSerializers
from .models import Category, Product

# Create your views here.
# get all categories
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializers(categories, many=True)
    return Response(serializer.data)

# get single category
@api_view(['GET'])
def get_category(request, slug):
    category = Category.objects.get(slug=slug)
    category_serializer = CategoryDetailSerializers(category)
    product_serializer = ProductListSerializers(category.category_product.all(), many=True)
    data = {
        'category': category_serializer.data,
        'products': product_serializer.data,
    }
    return Response(data)

# get single product
@api_view(['GET'])
def get_product(request, id):
    product = Product.objects.get(id=id)
    product_serializer = ProductDetailSerializers(product)
    product_image_serializer = ProductImageSerializers(product.product_image.all(), many=True)
    product_review_serializer = ReviewListSerializers(product.product_review.all(), many=True)
    data = {
        'product': product_serializer.data,
        'images': product_image_serializer.data,
        'reviews': product_review_serializer.data
    }
    return Response(data)