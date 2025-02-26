from statistics import quantiles

from rest_framework import viewsets, views
from rest_framework import permissions
from rest_framework.response import Response

from app.exception import AppException
from menu.models import MenuItem
from order.models import Order, OrderItem
from order.serializer import OrderSerializer
from django.http import Http404

from table.models import Table
from table.views import TableViewSet
from django.shortcuts import get_object_or_404
from users.models import Customer
import logging


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


#submit order
class SubmitOrder(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        customer = Customer.objects.get(pk=request.user.id)
        take_away = request.data.get('take_away', False)
        items = request.data.get('items')
        tables = request.data.get('table')  # table: là một mảng danh sách các id của bàn

        order = Order.objects.create(
            customer=customer,
            take_away=take_away
        )

        # Tạo danh sách các menu item được đặt
        self.create_order_item(order, items)

        if not take_away:
            TableViewSet.set_table(order, tables) # xử lý đặt bàn

        order.save()
        return Response(OrderSerializer(order).data)

    def create_order_item(self, order, items):
        for item in items:
            menu_item = get_object_or_404(MenuItem, pk=item.get('id'))
            if menu_item.status == menu_item.OUT_OF_STOCK:
                order.delete() #nếu có lỗi thì xóa order đó đi
                raise AppException(*AppException.MENU_ITEM_OUT_OF_STOCK)
            OrderItem.objects.create(
                order = order,
                menu_item = menu_item,
                quantity = item.get('quantity') or 1
            )

