from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from order.models import Order, OrderItem
from order.serializers import ViewOrderItemSerializer, ViewOrderSerializer
from .serializers import CategorySerializers, MyStoreProductSerializers, MyStoreSerializers, ProductImageSerializers, StoreProductSerializers, StoreSerializers, ViewStoreProductSerializers, ViewStoreSerializers
from .models import Category, Store, StoreProduct

# Create your views here.

# stores
@api_view(['GET'])
def stores(request):
    stores = Store.objects.all()
    data = []

    for s in stores:
        store_serializer = ViewStoreSerializers(s)
        inventory = s.store_inventory.all()
        
        data.append(store_serializer.data)
        data[-1]['inventory'] = []

        for item in inventory:
            item_serializer = ViewStoreProductSerializers(item).data
            item_images = ProductImageSerializers(item.product_image.all(), many=True)
            item_serializer['images'] = []
            for x in item_images.data:
                item_serializer['images'].append(x['image'])
            
            data[-1]['inventory'].append(item_serializer)

    return Response(data, status=status.HTTP_200_OK)


# new store
@swagger_auto_schema(method='POST', request_body=StoreSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def new_store(request):
    request.data._mutable = True
    data = request.data
    data['owner'] = request.user.id

    if request.method == 'POST':
        serializer = StoreSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

# get single store
@api_view(['GET'])
def store(request, id):
    store = Store.objects.get(id=id)

    store_serializer = ViewStoreSerializers(store)
    inventory = store.store_inventory.all()
    data = store_serializer.data
    data['inventory'] = []

    for item in inventory:
        item_serializer = ViewStoreProductSerializers(item).data
        item_images = ProductImageSerializers(item.product_image.all(), many=True)
        item_serializer['images'] = []
        for x in item_images.data:
            item_serializer['images'].append(x['image'])
        
        data['inventory'].append(item_serializer)

    return Response(data, status=status.HTTP_200_OK)


# get single store product
@api_view(['GET'])
def store_product(request, id):
    product = StoreProduct.objects.get(id=id)
    product_serializer = ViewStoreProductSerializers(product)
    data = product_serializer.data
    
    product_images = ProductImageSerializers(product.product_image.all(), many=True)
    data['images'] = []
    for x in product_images.data:
        data['images'].append(x['image'])

    return Response(data, status=status.HTTP_200_OK)


# my store
@swagger_auto_schema(method='PUT', request_body=MyStoreSerializers)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_store(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response({
            "error": "store not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = MyStoreSerializers(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        inventory = store.store_inventory.all()[:3]
        store_serializer = MyStoreSerializers(store)
        data = store_serializer.data
        data['inventory'] = []

        for item in inventory:
            item_serializer = ViewStoreProductSerializers(item).data
            item_images = ProductImageSerializers(item.product_image.all(), many=True)
            item_serializer['images'] = []
            for x in item_images.data:
                item_serializer['images'].append(x['image'])
            
            data['inventory'].append(item_serializer)
        try:
            data['orders'] = []
            # get all the order items that belong to this store
            order_items = OrderItem.objects.filter(order_item__store=store, has_been_picked_up=False)
            
            orders = {item.order: [] for item in order_items}
            for item in order_items:
                orders[item.order].append(item)

            for key, value in orders.items():
                order_serializer = ViewOrderSerializer(key).data
                order_serializer['order_items'] = []
                for order_item in value:
                    order_serializer['order_items'].append(ViewOrderItemSerializer(order_item).data)
                    order_serializer['order_items'][-1]['item'] = (ViewStoreProductSerializers(order_item.order_item).data)
                    order_serializer['order_items'][-1]['item']['image'] = ProductImageSerializers(order_item.order_item.product_image.first()).data['image']

                data['orders'].append(order_serializer)
            
        except OrderItem.DoesNotExist:
            data['orders'] = []
            
        return Response(data, status=status.HTTP_200_OK)


# view and add new inventory category in my store
@swagger_auto_schema(methods=['POST'], request_body=CategorySerializers)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_store_category(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response({
            'error': "store not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    request.data['store'] = store.id
    
    if request.method == 'POST':
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        categories = Category.objects.filter(store=store)
        serializer = CategorySerializers(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# view and add new inventory category in my store
@swagger_auto_schema(methods=['PUT'], request_body=CategorySerializers)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def my_category(request, id):
    category = Category.objects.filter(store=store)

    if category.store.owner == request.user:
        if request.method == 'GET':
            serializer = CategorySerializers(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.method == 'PUT':
            serializer = CategorySerializers(category, data=request.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        if request.method == 'DELETE':
            category.delete()
            return Response({
                "message": "Category deleted"
            }, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({
            "error": "Unauthorized access"
        }, status=status.HTTP_401_UNAUTHORIZED)


# view and add new inventory in my store
@swagger_auto_schema(methods=['POST'], request_body=MyStoreProductSerializers)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_store_inventory(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response({
            'error': "store not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    request.data._mutable = True
    request.data['store'] = store.id
    
    if request.method == 'POST':
        serializer = StoreProductSerializers(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            images = []
            data = serializer.data

            # Process and save images
            images_data = request.data.getlist('images')  # Assuming 'images' is the field name for the images
            for image in images_data:
                image_serializer = ProductImageSerializers(data={'image': image})
                if image_serializer.is_valid():
                    image_serializer.save(product=product)
                    images.append(image_serializer.data['image'])
                else:
                    product.delete()  # Delete the product if any image is invalid
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            data['images'] = images
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        inventory = StoreProduct.objects.filter(store=store)
        serializer = StoreProductSerializers(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# view and edit a product in my store
@swagger_auto_schema(methods=['PUT'], request_body=MyStoreProductSerializers)
@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
def my_store_product(request, id):
    try:
        store = Store.objects.get(owner=request.user)
        try:
            product = StoreProduct.objects.get(id=id, store=store)
        except StoreProduct.DoesNotExist:
            return Response({
                'error': "inventory product not found"
            },status=status.HTTP_404_NOT_FOUND)
        
    except Store.DoesNotExist:
        return Response({
            'error': "store not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        data = StoreProductSerializers(product).data
        data['images'] = []
        for img in product.product_image.all():
            data['images'].append(ProductImageSerializers(img).data['image'])

        return Response(data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = MyStoreProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_order_items(request):
    try:
        store = Store.objects.get(owner=request.user)

        try:
            data = []
            # get all the order items that belong to this store
            order_items = OrderItem.objects.filter(order_item__store=store, has_been_picked_up=False)
            
            orders = {item.order: [] for item in order_items}
            for item in order_items:
                orders[item.order].append(item)

            for key, value in orders.items():
                order_serializer = ViewOrderSerializer(key).data
                order_serializer['order_items'] = []
                for order_item in value:
                    order_serializer['order_items'].append(ViewOrderItemSerializer(order_item).data)
                    order_serializer['order_items'][-1]['item'] = (ViewStoreProductSerializers(order_item.order_item).data)
                    order_serializer['order_items'][-1]['item']['image'] = ProductImageSerializers(order_item.order_item.product_image.first()).data['image']

                data.append(order_serializer)
        
            return Response(data, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({
                    'message': "No orders found"
                }, status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({
            'error' : "You do not have a store."
        },status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def single_order(request, id):
    # find order
    try:
        store = Store.objects.get(owner=request.user)
        try:
            order = Order.objects.get(id=id)
            items = order.orderitem.filter(store=store)
        except Order.DoesNotExist:
            return Response({
                "error": "order not found"
            }, status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({
            "error": "store not found"
        }, status=status.HTTP_404_NOT_FOUND)



# @swagger_auto_schema(methods=['PUT'], request_body=UpdateOrderItemSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def single_order_item(request, id):
    try:
        store = Store.objects.get(owner=request.user)
        try:
            order_item = OrderItem.objects.filter(id=id, store=store)
        except OrderItem.DoesNotExist:
            return Response({
                    'error': "order item not found"
                }, status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({
            'error' : "You do not have a store."
        },status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ViewOrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        if not order_item.has_been_picked_up:
            serializer = ViewOrderItemSerializer(order_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
