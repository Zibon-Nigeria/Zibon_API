from rest_framework import serializers

from .models import Delivery, Order, OrderItem

# order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = '__all__'
        read_only_fields = ['order_number', 'customer', 'order_number', 'store']
        extra_kwargs = {
            'item': {'help_text': "ID of StoreItem"}
        }
        depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
        read_only_fields = ['sub_total']
        extra_kwargs = {
            'item': {'help_text': "ID of Store Inventoy item"},
            'quantity': {'help_text': "Quantity bought"},
        }


class OrderPostSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model =  Order
        fields = '__all__'
        read_only_fields = ['customer', 'order_number', 'store']
        extra_kwargs = {
            'items': {'help_text': "Array of order items"}
        }


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = ["has_been_picked_up"]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ['order', 'destination_address']
        extra_kwargs = {
            'shopper': {'help_text': "User id of shopper"},
            'order': {'help_text': "Id of order"}
        }


class RequestDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['order', 'destination_address']
        extra_kwargs = {
            'order': {'help_text': "ID of Order object"},
            'destination_address': {'help_text': "address of where oreder should be delivered"},
        }