from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from app.exception import AppException
from table.models import Table
from table.serializer import TableSerializer
import logging

logger = logging.getLogger('table')

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
            logger.error(f'wrong data type list of table {type(tables)} -> must be list')
            raise AppException(*AppException.TYPE_ERROR)

        for id in tables:
            table = Table.objects.get(pk=id)
            if table.is_busy:
                logger.error(f'has table is busy')
                order.delete()
                raise AppException(*AppException.TABLE_BUSY)
            table.order.add(order)
            table.is_busy = True
            table.save()
