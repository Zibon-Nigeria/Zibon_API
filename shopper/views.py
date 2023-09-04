from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated  
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from order.models import Delivery
from order.serializers import DeliverySerializer

from shopper.models import BankInfo, ShopperPersonalInfo, ShopperProfile
from shopper.serializers import BankInfoSerializer, ShopperPersonalInfoSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    try:
        shopper = ShopperProfile.objects.get(user=request.user)
    except ShopperPersonalInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    deliveries_serializer = DeliverySerializer(shopper.delivery.all(), many=True)
    shopper_serializer = ShopperPersonalInfoSerializer(shopper)

    return Response({
            'shopper': shopper_serializer.data,
            'deliveries': deliveries_serializer.data
        }, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=ShopperPersonalInfoSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def shopper_personal_info(request):
    data = request.data
    data['shopper'] = request.user.shopper_profile.id

    if request.method == 'POST':
        personal_info_serializer = ShopperPersonalInfoSerializer(data=data)
        if personal_info_serializer.is_valid():
            personal_info_serializer.save()
            return Response(personal_info_serializer.data, status=status.HTTP_201_CREATED)
        return Response(personal_info_serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "GET":
        try:
            user_shopper_info = ShopperPersonalInfo.objects.get(user=request.user.shopper_profile)
        except ShopperPersonalInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        shopper_info_serializer = ShopperPersonalInfoSerializer(user_shopper_info)
        return Response(shopper_info_serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_deliveries(request):
    deliveries = Delivery.objects.filter(delivery_status='Available')
    serializer = DeliverySerializer(deliveries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def delivery(request, id):
    user = request.user

    try:
        delivery = Delivery.objects.get(id=id)
    except Delivery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":        
        if delivery.delivery_status != "Available":
            return Response({
                'message': "This order has already been taken or delivered by another shopper"
            }, status=status.HTTP_410_GONE)
        
        delivery.shopper = user
        delivery.delivery_status = 'Pending'
        delivery.save()

        serializer = DeliverySerializer(delivery)
        return Response({
            'message': "You have accepted to carryout this delivery",
            'delivery': serializer.data
        }, status=status.HTTP_202_ACCEPTED)


# view history of previous deliveries made
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_history(request):
    user = request.user
    deliveries_history = Delivery.objects.filter(shopper=user)
    serializer = DeliverySerializer(deliveries_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# view details of previous delivery
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_history_detail(request, id):
    try:
        delivery = Delivery.objects.get(id=id)
    except Delivery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DeliverySerializer(delivery)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=BankInfoSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bank_info(request):
    data = request.data
    data['shopper'] = request.user.shopper_profile.id

    try:
        bank_info = BankInfo.objects.filter(shopper=request.user.shopper_profile)
    except ShopperPersonalInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        info_serializer = BankInfo(bank_info, many=True)
        return Response(info_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        info_serializer = BankInfo(data=data)
        if info_serializer.is_valid():
            info_serializer.save()
            return Response(info_serializer.data, status=status.HTTP_201_CREATED)
        return Response(info_serializer._errors, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def bank(request, id):
    try:
        bank_info = BankInfo.objects.get(id=id)
    except ShopperPersonalInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        info_serializer = BankInfo(bank_info)
        return Response(info_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        info_serializer = BankInfo(bank_info, data=request.data)
        if info_serializer.is_valid():
            info_serializer.save()
            return Response(info_serializer.data, status=status.HTTP_201_CREATED)
        return Response(info_serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        