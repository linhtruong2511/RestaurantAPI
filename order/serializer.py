from rest_framework import serializers

from menu.models import MenuItem
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.IntegerField(source='menu_item.price', read_only=True)
    class Meta:
        model = OrderItem
        fields = [
            'menu_item_name',
            'menu_item_price',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    menu_item = serializers.CharField(write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
