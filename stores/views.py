from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderSerializer, UpdateOrderItemSerializer, ViewOrderItemSerializer
from products.serializers import ProductSerializers, ProductImageSerializers
from .serializers import MyStoreInventorySerializers, MyStoreSerializers, StoreSerializers, StoreInventorySerializers, ViewStoreInventorySerializers, ViewStoreSerializers
from .models import Store, StoreInventory

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
            item_serializer = ViewStoreInventorySerializers(item)
            data[-1]['inventory'].append(item_serializer.data)

    return Response(data, status=status.HTTP_200_OK)


# new store
@swagger_auto_schema(method='POST', request_body=StoreSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_store(request):
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
    inventory = store.store_inventory.all()
    
    store_serializer = ViewStoreSerializers(store)
    data = store_serializer.data
    data['inventory'] = []

    for item in inventory:
        item_serializer = ViewStoreInventorySerializers(item)
        data['inventory'].append(item_serializer.data)

    return Response(data, status=status.HTTP_200_OK)


# get single store product
@api_view(['GET'])
def store_product(request, id):
    inventory_product = StoreInventory.objects.get(id=id)

    invetory_product_serializer = StoreInventorySerializers(inventory_product)
    product_image_serializer = ProductImageSerializers(inventory_product.product.product_image.all(), many=True)

    data = {
        'product': invetory_product_serializer.data,
        'images': product_image_serializer.data
    }

    return Response(data)


# my store
@swagger_auto_schema(method='PUT', request_body=MyStoreSerializers)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_store(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = MyStoreSerializers(store, data=request.data)
        if serializer.is_valid() & serializer.has_object_permission(request, store):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        inventory = store.store_inventory.all()
        store_serializer = MyStoreSerializers(store)
        data = store_serializer.data
        data['inventory'] = []

        for i in inventory:
            invetory_serializer = ViewStoreInventorySerializers(i)
            
            data['inventory'].append(invetory_serializer.data)
        return Response(data, status=status.HTTP_200_OK)
    

# view and add new inventory in my store
@swagger_auto_schema(methods=['POST'], request_body=MyStoreInventorySerializers)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def my_store_inventory(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response({
            'error': "store not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    request.data['store'] = store
    
    if request.method == 'POST':
        serializer = StoreInventorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        inventory = store.store_inventory.all()
        
        store_serializer = ViewStoreSerializers(store)
        data = store_serializer.data
        data['inventory'] = []

        for item in inventory:
            item_serializer = ViewStoreInventorySerializers(item)
            data['inventory'].append(item_serializer.data)
        return Response(data, status=status.HTTP_200_OK)


# view and edit a product in my store
@swagger_auto_schema(methods=['PUT'], request_body=MyStoreInventorySerializers)
@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
def my_store_product(request, id):
    try:
        store = Store.objects.get(owner=request.user)
        try:
            product = StoreInventory.objects.get(id=id, store=store)
        except StoreInventory.DoesNotExist:
            return Response({
                'error': "inventory product not found"
            },status=status.HTTP_404_NOT_FOUND)
    except Store.DoesNotExist:
        return Response({
            'error': "store not found"
        },status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StoreInventorySerializers(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = MyStoreInventorySerializers(product, data=request.data)
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
            # get all the order items that belong to this store
            order_items = OrderItem.objects.filter(store=store, has_been_picked_up=False)
            serializers = ViewOrderItemSerializer(order_items, many=True)
            
            # create a set of order objects based on order items
            orderSet = {}
            for item in serializers.data:
                orderSet.add(item['order'])

            data = list(map(lambda x, y: [y for y in serializers.data if y['order'] == x], orderSet, serializers.data))
            
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



@swagger_auto_schema(methods=['PUT'], request_body=UpdateOrderItemSerializer)
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

        
