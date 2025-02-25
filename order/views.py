from rest_framework import viewsets, views
from rest_framework import permissions
from rest_framework.response import Response

from menu.models import MenuItem
from order.models import Order, OrderItem
from order.serializer import OrderSerializer
from django.http import Http404

from table.models import Table
from table.views import TableViewSet, TableException
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
        #comment test 2
        #test
        customer = Customer.objects.get(pk=request.user.id)
        take_away = request.data.get('take_away', False)
        items = request.data.get('items')
        tables = request.data.get('table')  # table: là một mảng danh sách các id của bàn

        order = Order.objects.create(
            customer=customer,
            take_away=take_away
        )

        # Tạo danh sách các menu item được đặt
        for item in items:
            self.create_order_item(order, **item)

        # Xử lý đặt bàn
        data = {}
        if not take_away:
            try:
                TableViewSet.set_table(order, tables)
                order.save()  # Lưu lại order
                return Response(OrderSerializer(order).data, 200)
            except TableException as e:  # bắt exception nếu mà bàn đó đã bị đặt rồi thì sẽ trả về lỗi
                order.delete()  # xóa order bị lỗi
                data = {
                    "message": e.__str__(),
                    "status": 400
                }
                return Response(data, 400)
            except Table.DoesNotExist as e:
                data = {
                    "message": str(e),
                    "status": 400
                }
                return Response(data, 400)
        else:
            return Response(OrderSerializer(order).data)

    def create_order_item(self, order, id, quantity):
        try:
            menu_item = get_object_or_404(MenuItem, pk=id)
            if menu_item.status == menu_item.OUT_OF_STOCK:
                raise Exception("")
            quantity = quantity
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )
        except MenuItem.DoesNotExist:
            raise Http404

