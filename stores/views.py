from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.serializers import ProductDetailSerializers, ProductImageSerializers, ProductListSerializers

from .serializers import StoreSerializers, StoreInventoryListSerializers
from .models import Store, StoreInventory

# Create your views here.

# get all stores
@api_view(['GET'])
def get_all_stores(request):
    stores = Store.objects.all()
    data = {}

    for s in range(0, len(stores)):
        store_serializer = StoreSerializers(stores[s])
        inventory = stores[s].store_inventory.all()
        # invetory_serializer = StoreInventoryListSerializers(stores[s].store_inventory.all(), many=True)
        
        data[f'{s}'] = {}
        data[f'{s}']['store'] = store_serializer.data
        # data[f'{s}']['inventory'] = invetory_serializer.data
        data[f'{s}']['inventory'] = []

        for i in range(0, len(inventory)):
            invetory_serializer = StoreInventoryListSerializers(inventory[i])
            product_serializer = ProductListSerializers(inventory[i].product)
          
            data[f'{s}']['inventory'].append({})
            data[f'{s}']['inventory'][i]['product'] = invetory_serializer.data
            data[f'{s}']['inventory'][i]['details'] = product_serializer.data

    return Response(data)

# get single stores
@api_view(['GET'])
def get_store(request, id):
    store = Store.objects.get(id=id)
    inventory = store.store_inventory.all()
    data = {}

    store_serializer = StoreSerializers(store)
    data['store'] = store_serializer.data
    data['inventory'] = []

    for i in range(0, len(inventory)):
        invetory_serializer = StoreInventoryListSerializers(inventory[i])
        product_serializer = ProductListSerializers(inventory[i].product)
        
        data['inventory'].append({})
        data['inventory'][i]['product'] = invetory_serializer.data
        data['inventory'][i]['details'] = product_serializer.data

    return Response(data)

# get single store product
@api_view(['GET'])
def get_store_product(request, id):
    inventory_product = StoreInventory.objects.get(id=id)

    invetory_product_serializer = StoreInventoryListSerializers(inventory_product)
    store_serializer = StoreSerializers(inventory_product.store)
    product_details_serializer = ProductDetailSerializers(inventory_product.product)
    product_image_serializer = ProductImageSerializers(inventory_product.product.product_image.all(), many=True)

    data = {
        'store': store_serializer.data,
        'product': invetory_product_serializer.data,
        'details': product_details_serializer.data,
        'images': product_image_serializer.data
    }

    return Response(data)