from rest_framework import serializers
from .models import MenuItem, MenuCategory

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuCategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(read_only=True, many=True)
    class Meta:
        model = MenuCategory
        fields = '__all__'