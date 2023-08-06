from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from accounts.models import CustomUser
from order.models import Delivery, Order, OrderItem

from order.serializers import DeliverySerializer, OrderPostSerializer, OrderSerializer, RequestDeliverySerializer
from stores.models import StoreInventory


# Create your views here.
@swagger_auto_schema(method='POST', request_body=OrderPostSerializer)
@api_view(['POST'])
def make_order(request):
    user = request.user
    items = request.data['items']

    # create order object
    order = Order(
        customer=user,
        total=0
    )
    order.save()

    for i in items:
        item = StoreInventory.objects.get(id=i['item'])

        # create order item
        order_item = OrderItem(
            item=item,
            quantity=i['quantity']
        )
        order_item.save()

        order_item.order = order  # add order item to order
        order.total += int(order_item.subtotal)  # add order item subtotal to order total
        
        order.save()
        order_item.save()

        # serialize order
        order_serializer = OrderSerializer(order)

    return Response(order_serializer.data, status=status.HTTP_201_CREATED)


# view to request delivery
@swagger_auto_schema(method='POST', request_body=RequestDeliverySerializer)
@api_view(['POST'])
def request_delivery(request):
    order = Order.objects.get(id=request.data['order'])

    delivery_request = Delivery(
        order=order,
        destination_address=request.data['destination_address']
    )

    delivery_request.save()
    serializer = DeliverySerializer(delivery_request)

    return Response(serializer.data, status=status.HTTP_201_CREATED)