from rest_framework import serializers

from .models import Delivery, Order, OrderItem

# order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = ['order_number', 'customer', 'total', 'qr_code', 'created_at', 'updated_at']
        # read_only_fields = ['order_number', 'customer', 'qr_code']
        extra_kwargs = {
            'item': {'help_text': "ID of StoreItem"}
        }
        # depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
        read_only_fields = ['sub_total']
        extra_kwargs = {
            'item': {'help_text': "ID of Store Inventoy item"},
            'quantity': {'help_text': "Quantity bought"},
        }


class ViewOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
        depth = 1


class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = ['has_been_picked_up']
        

class PostOrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)


# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =  Order
#         fields = ["has_been_picked_up"]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ['order', 'delivery_address']
        extra_kwargs = {
            'shopper': {'help_text': "User id of shopper"},
            'order': {'help_text': "Id of order"}
        }


class RequestDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['order', 'delivery_address']
        extra_kwargs = {
            'order': {'help_text': "ID of Order object"},
            'destination_address': {'help_text': "address of where oreder should be delivered"},
        }


class AcceptDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['shopper']
        extra_kwargs = {
            'order': {'help_text': "ID of Order object"},
            'destination_address': {'help_text': "address of where oreder should be delivered"},
        }
