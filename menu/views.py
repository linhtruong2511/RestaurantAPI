from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from .models import MenuItem, MenuCategory
from .serializer import MenuCategorySerializer, MenuItemSerializer


# Create your views here.
class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]
    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class MenuCategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class UploadMenuItem(generics.UpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


