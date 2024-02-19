from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from order.models import Delivery, Order
import qrcode
from io import BytesIO
from django.core.files import File

from order.serializers import DeliverySerializer, OrderItemSerializer, PostOrderSerializer, OrderSerializer, ViewDeliverySerializer, ViewOrderItemSerializer, ViewOrderSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    # get all orders that belong to the loggedin customer
    orders = Order.objects.filter(customer=request.user)

    data = []
    for order in orders:
        order_serializer = OrderSerializer(order).data
        items = ViewOrderItemSerializer(order.orderitem_set.all(), many=True).data
        order_serializer['items'] = items
        data.append(order_serializer)

    return Response(data, status=status.HTTP_200_OK)
       

@swagger_auto_schema(method='POST', request_body=PostOrderSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_order(request):
    if request.method == 'POST':
        request.data['customer'] = request.user.id
        order_items = request.data['order_items']

        # create order object
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():

            data = order_serializer.validated_data

            # Generate a QR code for order
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
            ord_items = []

            # create order_items for order
            for item in order_items:
                item['order'] = order.id
                print(item)
                item_serializier = OrderItemSerializer(data=item)
                if item_serializier.is_valid():
                    order_item = item_serializier.save()

                    ord_items.append(item_serializier.data) # add item to list of order items
                    order_total += order_item.subtotal  # add order item subtotal to order total

            # update order total    
            order.total = order_total
            order.save()

            order_serializer = ViewOrderSerializer(order).data

            # create delivery
            if order.order_type == "Delivery":
                delivery_serializer = DeliverySerializer(data={
                        "order": order.id,
                        "delivery_address": request.data['delivery_address']
                    })
                
                if delivery_serializer.is_valid():
                    delivery = delivery_serializer.save()
                    order_serializer['delivery_details'] = ViewDeliverySerializer(delivery).data

            order_serializer['customer'] = {
                "fullname": request.user.fullname,
                "phone": request.user.phone
            }

        return Response(order_serializer, status=status.HTTP_201_CREATED)


# single order
# @swagger_auto_schema(method='PUT')
@api_view(['GET', "PUT"])
@permission_classes([IsAuthenticated])
def single_order(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({
            "error": "Order not found"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":

        order_serializer = ViewOrderSerializer(order).data
        items = ViewOrderItemSerializer(order.orderitem_set.all(), many=True).data
        order_serializer['items'] = items
        data.append(order_serializer)

        data = OrderSerializer(order).data
        if order.order_type == "Delivery":
            order_serializer['delivery'] = DeliverySerializer(order.delivery).data
            
        return Response(data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        pass


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_paid(request, order_number):
    # find order
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({
            "error": "order does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    order.is_paid = True
    order.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_order(request, order_number):
    # find order
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({
            "error": "order does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    # order.is_paid = True
    # order.save()
    
    data = OrderSerializer(order).data
    if order.order_type == "Delivery":
        data['delivery'] = ViewDeliverySerializer(order.delivery).data

    data['items'] = []
    for orderItem in order.orderitem_set.all():
        item = ViewOrderItemSerializer(orderItem).data
        item['']
        data['items'].append(ViewOrderItemSerializer(orderItem).data)
    return Response(data, status=status.HTTP_200_OK)


# single delivery
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_delivery(request, id):
    try:
        delivery = Delivery.objects.get(id=id)
    except Delivery.DoesNotExist:
        return Response({
            "error": "Delivery nor found"
        }, status=status.HTTP_404_NOT_FOUND)

    data = DeliverySerializer(delivery).data
    data['order'] = ViewOrderSerializer(delivery.order).data

    return Response(data, status=status.HTTP_200_OK)


# shopper accept delivery
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accept_delivery(request, id):
    # check if logged in user is a shopper
    if request.user.account_type == "Shopper":
        try:
            delivery = Delivery.objects.get(id=id)
            # assign delivery to shopper
            delivery.shopper = request.user
            delivery.delivery_status = 'Pending'
            delivery.save()

            data = DeliverySerializer(delivery).data
            data['order'] = ViewOrderSerializer(delivery.order).data

            return Response(data, status=status.HTTP_202_ACCEPTED)

        except Delivery.DoesNotExist:
            return Response({
                "error": "Delivery not found"
            }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "error": "User must be a shopper"
        }, status=status.HTTP_403_FORBIDDEN)
