from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from app.exception import AppException
from table.models import Table
from table.serializer import TableSerializer


# Create your views here.
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

    @staticmethod
    def set_table(order, tables):
        if not isinstance(tables, list):
            raise AppException(*AppException.TYPE_ERROR)

        for id in tables:
            table = Table.objects.get(pk=id)
            if table.is_busy:
                order.delete()
                raise AppException(*AppException.TABLE_BUSY)
            table.order.add(order)
            table.is_busy = True
            table.save()
