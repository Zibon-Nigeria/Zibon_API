from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  
from drf_yasg.utils import swagger_auto_schema

from accounts.serializers import MyTokenObtainPairSerializer, UserSerializer, ViewUserSerializer
from order.models import OrderItem
from order.serializers import ViewOrderSerializer
from stores.models import Store

@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        token = MyTokenObtainPairSerializer.get_token(user)

        user_data = ViewUserSerializer(user)
    
        return Response({
                # "user": user_data.data,
                'access': str(token.access_token),
                'refresh': str(token),
                'has_store': Store.objects.filter(owner=user).exists()
            }, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = ViewUserSerializer(user)
        data =  serializer.data
        try:
            data['orders'] = []
            # get all the order items that belong to this store
            order_items = OrderItem.objects.filter(order__customer=user)
            
            orders = {item.order: [] for item in order_items}
            for item in order_items:
                orders[item.order].append(item)

            for key, value in orders.items():
                order_serializer = ViewOrderSerializer(key).data
                order_serializer['order_items'] = []
                for order_item in value:
                    order_serializer['order_items'].append({
                        "item": order_item.order_item.name,
                        "retail_price": order_item.order_item.retail_price,
                        "quantity": order_item.quantity,
                        "subtotal": order_item.subtotal,
                    })
                data['orders'].append(order_serializer)
            
        except OrderItem.DoesNotExist:
            data['orders'] = []
            
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    user = request.user
    data =  []
    try:
        # get all the order items that belong to this store
        order_items = OrderItem.objects.filter(order__customer=user)
        
        orders = {item.order: [] for item in order_items}
        for item in order_items:
            orders[item.order].append(item)

        for key, value in orders.items():
            order_serializer = ViewOrderSerializer(key).data
            order_serializer['order_items'] = []
            for order_item in value:
                order_serializer['order_items'].append({
                    "item": order_item.order_item.name,
                    "retail_price": order_item.order_item.retail_price,
                    "quantity": order_item.quantity,
                    "subtotal": order_item.subtotal,
                })
            data.append(order_serializer)
        
    except OrderItem.DoesNotExist:
        pass
    return Response(data, status=status.HTTP_200_OK)