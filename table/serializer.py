from rest_framework import serializers

from order.models import Order
from table.models import Table


class TableSerializer(serializers.ModelSerializer):
    # order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True)
    class Meta:
        model = Table
        fields = '__all__'