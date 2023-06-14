from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import CategorySerializers, ProductSerializers, ProductImageSerializers, ReviewListSerializers
from .models import Category, Product

# Create your views here.
# get all categories
@api_view(['GET', 'POST'])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializers(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get single category
@api_view(['GET'])
def get_category(request, slug):
    category = Category.objects.get(slug=slug)
    category_serializer = CategorySerializers(category)
    product_serializer = ProductSerializers(category.category_product.all(), many=True)
    data = {
        'category': category_serializer.data,
        'products': product_serializer.data,
    }
    return Response(data)


# get all categories
@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# get single product
@api_view(['GET'])
def get_product(request, id):
    product = Product.objects.get(id=id)
    product_serializer = ProductSerializers(product)
    product_image_serializer = ProductImageSerializers(product.product_image.all(), many=True)
    # product_review_serializer = ReviewListSerializers(product.product_review.all(), many=True)
    data = {
        'product': product_serializer.data,
        'images': product_image_serializer.data,
        # 'reviews': product_review_serializer.data
    }
    return Response(data)