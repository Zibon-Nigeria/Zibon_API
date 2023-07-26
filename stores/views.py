from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from products.serializers import ProductSerializers, ProductImageSerializers

from .serializers import MyStoreInventorySerializers, MyStoreSerializers, StoreSerializers, StoreInventorySerializers
from .models import Store, StoreInventory

# Create your views here.

# new store
# @swagger_auto_schema(method='POST', request_body=StoreSerializers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_store(request):
    data = request.data
    data['owner'] = request.user

    print(data)

    if request.method == 'POST':
        serializer = StoreSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# get all stores
@api_view(['GET'])
def stores(request):
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
    store_serializer = StoreSerializers(inventory_product.store)
    product_details_serializer = ProductSerializers(inventory_product.product)
    product_image_serializer = ProductImageSerializers(inventory_product.product.product_image.all(), many=True)

    data = {
        'store': store_serializer.data,
        'product': invetory_product_serializer.data,
        'details': product_details_serializer.data,
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
@swagger_auto_schema(methods=['POST', 'PUT'], request_body=MyStoreInventorySerializers)
@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def store_inventory(request):
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
    