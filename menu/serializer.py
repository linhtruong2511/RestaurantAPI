from rest_framework import serializers
from .models import MenuItem, MenuCategory

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'