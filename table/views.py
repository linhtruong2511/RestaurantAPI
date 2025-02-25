from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from table.models import Table
from table.serializer import TableSerializer


class TableException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.error_code = code

    def __str__(self):
        return super().__str__()


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
            raise TableException("Invalid table list", 400)

        for id in tables:
            table = Table.objects.get(pk=id)
            # print("table busy : " + str(table.is_busy))
            if table.is_busy:
                raise TableException('table is busy', 400)
            table.order.add(order)
            table.is_busy = True
            table.save()
