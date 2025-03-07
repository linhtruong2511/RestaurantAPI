from logging import DEBUG, StreamHandler, Formatter

from django.contrib.auth import aget_user
from django.http import Http404
from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from unicodedata import category

from app.exception import AppException
from app.permission import IsAdminOrReadOnly
from .models import MenuItem, MenuCategory
from .serializer import MenuCategorySerializer, MenuItemSerializer
import logging

logger = logging.getLogger('menu-item')


# Create your views here.
class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        category_name = request.query_params.get('category')
        offset = int(request.query_params.get('offset') or 0)
        limit = int(request.query_params.get('limit') or 10)
        logger.debug(f'query params: {request.query_params}')
        menu_items = []
        if category_name:
            menu_items = MenuItem.objects.filter(category__name=category_name)
        else:
            menu_items = MenuItem.objects.all()
        if len(menu_items) == 0:
            raise AppException(*AppException.CATEGORY_NOT_EXIST)
        
        page = self.paginate_queryset(menu_items)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class MenuCategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        # Lấy tên của category
        query_param = kwargs.pop('pk')
        logger.info(f'get category: {query_param}')
        try:
            category = MenuCategory.objects.get(name=query_param)
            return Response(MenuCategorySerializer(category).data)
        except MenuCategory.DoesNotExist:
            logger.error(f'category {query_param} is not exist')
            raise Http404


class UploadMenuItem(generics.UpdateAPIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAdminUser]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
