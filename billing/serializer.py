from rest_framework import serializers

from order.models import Order
from order.serializer import OrderSerializer
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True)
    order_detail = OrderSerializer(source='order', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'order', 'date', 'total_amount', 'method', 'order_detail', 'paid']