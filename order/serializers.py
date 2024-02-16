from rest_framework import serializers
from .models import Delivery, Order, OrderItem

# order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = ['id', 'order_number', 'order_type', 'customer', 'total', 'qr_code', 'is_paid', 'created_at', 'updated_at']
        read_only_fields = ['is_paid']
        extra_kwargs = {
            'item': {'help_text': "ID of StoreItem"}
        }
        # depth = 1

class ViewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = ['order_number', 'order_type', 'qr_code', 'total', 'is_paid', 'created_at']


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
    order_item = serializers.SerializerMethodField()

    def get_order_item(self, instance):
        return instance.order_item.name
    
    class Meta:
        model =  OrderItem
        fields = ["order_item", "quantity", "subtotal", "has_been_picked_up"]


class PostOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    delivery_address = serializers.CharField()
    class Meta:
        model =  Order
        fields = ['order_type', 'total', 'items', 'delivery_address']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class RequestDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['order', 'delivery_address']
        extra_kwargs = {
            'order': {'help_text': "ID of Order object"},
            'destination_address': {'help_text': "address of where oreder should be delivered"},
        }
