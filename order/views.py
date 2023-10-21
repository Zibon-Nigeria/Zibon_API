from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from accounts.models import User
from order.models import Delivery, Order, OrderItem
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File

from order.serializers import DeliverySerializer, OrderItemSerializer, PostOrderSerializer, OrderSerializer, RequestDeliverySerializer
from stores.models import Store, StoreInventory


# Create your views here.
@swagger_auto_schema(method='POST', request_body=PostOrderSerializer)
@api_view(['POST'])
def make_order(request):
    request.data['customer'] = request.user.id
    items = request.data['items']

    # create order object
    order_serializer = OrderSerializer(data=request.data)
    if order_serializer.is_valid():

        data = order_serializer.validated_data

        # Generate a order QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_image = File(buffer, name=f'{data}.png')

        # Save the data and QR code image in the database
        order = order_serializer.save(qr_code=qr_code_image)

        order_total = 0
        # data = order_serializer.data
        data['items'] = []

    for item in items:
        item['order'] = order.id
        item_serializier = OrderItemSerializer(data=item)
        if item_serializier.is_valid():
            order_item = item_serializier.save()
            data['items'].append(item_serializier.data)

            order_total += order_item.subtotal  # add order item subtotal to order total
        
        order.total = order_total
        order.save()

    return Response(data, status=status.HTTP_201_CREATED)


# view to request delivery
@swagger_auto_schema(method='POST', request_body=DeliverySerializer)
@api_view(['POST'])
def request_delivery(request):
    order = Order.objects.get(id=request.data['order'])
    
    # check if order belongs to logged in user
    if request.user == order.customer:
        serializer = DeliverySerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': "Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)