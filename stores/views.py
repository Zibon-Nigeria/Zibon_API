from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from order.models import Order
from order.serializers import OrderSerializer, UpdateOrderSerializer
from products.serializers import ProductSerializers, ProductImageSerializers
from .serializers import MyStoreInventorySerializers, MyStoreSerializers, StoreSerializers, StoreInventorySerializers
from .models import Store, StoreInventory

# Create your views here.

# new store
@swagger_auto_schema(method='POST', request_body=StoreSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_store(request):
    data = request.data
    data['owner'] = request.user

    if request.method == 'POST':
        serializer = StoreSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# get all stores
@api_view(['GET'])
def nearby_stores(request):
    stores = Store.objects.all()
    data = {}

    for s in range(0, len(stores)):
        store_serializer = StoreSerializers(stores[s])
        inventory = stores[s].store_inventory.all()
        
        data[f'{s}'] = {}
        data[f'{s}']['store'] = store_serializer.data
        data[f'{s}']['inventory'] = []

        for i in range(0, len(inventory)):
            invetory_serializer = StoreInventorySerializers(inventory[i])
            product_serializer = ProductSerializers(inventory[i].product)
        
            data[f'{s}']['inventory'].append({})
            data[f'{s}']['inventory'][i]['product'] = invetory_serializer.data
            data[f'{s}']['inventory'][i]['details'] = product_serializer.data

    return Response(data)

# get single store
@api_view(['GET'])
def store(request, id):
    store = Store.objects.get(id=id)
    inventory = store.store_inventory.all()
    data = {}

    store_serializer = StoreSerializers(store)
    data['store'] = store_serializer.data
    data['inventory'] = []

    for i in range(0, len(inventory)):
        invetory_serializer = StoreInventorySerializers(inventory[i])
        product_serializer = ProductSerializers(inventory[i].product)
        
        data['inventory'].append({})
        data['inventory'][i]['product'] = invetory_serializer.data
        data['inventory'][i]['details'] = product_serializer.data

    return Response(data)

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
    
    serializer = MyStoreSerializers(data=request.data)
    
    if request.method == 'PUT':
        # check for user permission and valid data
        if serializer.is_valid() & serializer.has_object_permission(request, store):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        inventory = store.store_inventory.all()
        data = {}

        store_serializer = MyStoreSerializers(store)
        data['store'] = store_serializer.data
        data['inventory'] = []

        for i in range(0, len(inventory)):
            invetory_serializer = StoreInventorySerializers(inventory[i])
            product_serializer = ProductSerializers(inventory[i].product)
            
            data['inventory'].append({})
            data['inventory'][i]['product'] = invetory_serializer.data
            data['inventory'][i]['details'] = product_serializer.data

        return Response(data)
    

# add new and edit inventory in my store
@swagger_auto_schema(methods=['POST'], request_body=MyStoreInventorySerializers)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def store_inventory(request):
    try:
        store = Store.objects.get(owner=request.user)
    except Store.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.data['store'] = store
    
    if request.method == 'POST':
        serializer = MyStoreInventorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        serializer = MyStoreInventorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_orders(request):
    try:
        store = Store.objects.get(owner=request.user)
        try:
            orders = Order.objects.filter(store=store)
            serializers = OrderSerializer(orders, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
       
        except Order.DoesNotExist:
            return Response({
                    'message': "No orders found"
                }, status=status.HTTP_404_NOT_FOUND)
        
    except Store.DoesNotExist:
        return Response({
            'message' : "You do not have a store."
        },status=status.HTTP_404_NOT_FOUND)
    

@swagger_auto_schema(methods=['PUT'], request_body=UpdateOrderSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def single_order(request, id):
    try:
        store = Store.objects.get(owner=request.user)
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({
                    'message': "No order found"
                }, status=status.HTTP_404_NOT_FOUND)
        
    except Store.DoesNotExist:
        return Response({
            'message' : "You do not have a store."
        },status=status.HTTP_404_NOT_FOUND)
    
    # check if order belongs to this store
    if order.store == store: 
        if request.method == "GET":
            serializers = OrderSerializer(order)
            return Response(serializers.data, status=status.HTTP_200_OK)
        if request.method=="PUT":
            serializer = UpdateOrderSerializer(order, data=request.data )
            return Response({
                    "order": serializer.data,
                    "message": "order updated successfully"
                }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message':'Order doesnot belong to this store.'
        }, status=status.HTTP_404_NOT_FOUND)
        
