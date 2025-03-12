from datetime import datetime, timedelta
from logging import raiseExceptions
from statistics import quantiles

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, views
from rest_framework import permissions
from rest_framework.response import Response

from app.exception import AppException
from menu.models import MenuItem
from menu.views import logger
from order.models import Order, OrderItem
from order.serializer import OrderSerializer

from table.views import TableViewSet
from django.shortcuts import get_object_or_404
from users.models import Customer
import logging

logger = logging.getLogger('ORDER')


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# submit order
class SubmitOrder(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        customer = Customer.objects.get(pk=request.user.id)
        take_away = request.data.get('take_away', False)
        items = request.data.get('items')
        tables = request.data.get('table')  # table: là một mảng danh sách các id của bàn
        order_date_str = request.data.get('order_date')
        number_of_guests = request.data.get('number_of_guests')

        order = Order.objects.create(
            customer=customer,
            take_away=take_away,
            create_date=timezone.now(),
            number_of_guests=number_of_guests or 1,
        )

        if order_date_str:
            order_date = parse_datetime(order_date_str)
            if not order_date:
                logger.error('time fomat error: ' + str(order_date_str))
                raise AppException(*AppException.ERROR_TIME_FORMAT)

            order.order_date = order_date
            self.check_order_datetime(
                order)  # kiểm soát lưu lượng khách hàng cùng 1 thời gian (10 khách hàng trong 1 thời gian)

        # Tạo danh sách các menu item được đặt
        self.create_order_item(order, items)

        if not take_away:
            TableViewSet.set_table(order, tables)  # xử lý đặt bàn

        logger.info(f'customer [ {order.customer.user} ] has successfully placed an order')
        logger.info(f'order date is: {order.order_date}')

        order.save()
        return Response(OrderSerializer(order).data)

    def create_order_item(self, order, items):
        for item in items:
            menu_item = get_object_or_404(MenuItem, pk=item.get('id'))
            if menu_item.status == menu_item.OUT_OF_STOCK:
                logger.warning(f'item [{menu_item.name} is out of stock]')
                order.delete()  # nếu có lỗi thì xóa order đó đi
                raise AppException(*AppException.MENU_ITEM_OUT_OF_STOCK)

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item.get('quantity') or 1
            )

    def check_order_datetime(self, order):
        if order.order_date < order.create_date:
            logger.warning(f'invalid order time: {order.order_date} < {order.create_date}')
            order.delete()  # xóa đi nếu sai
            raise AppException(*AppException.ORDER_TIME_ERROR)

        # Kiểm tra các order trước và sau order này 90 phút vì trước 90p thì khách cũ có thể chưa rời quán
        # Đơn được đặt lúc 4h30 thì các đơn lúc 3h có thể vẫn còn ở quán -> quá tải
        # Tương tự với đơn đặt lúc 4h30 nhưng mà lúc 5h thì đã có 10 đơn đặt trước rồi -> quá tải

        # vấn đề là lượng chỗ ngồi của quán thì sao ?? nếu vẫn trong khoảng thời gian quá tải mà khách lại về trước so với dự tính -> thừa chỗ ngồi
        # lúc đó thì có thể đặt đơn mới  :>>>
        order_check = Order.objects.filter(
            order_date__lte=order.order_date + timedelta(minutes=90),
            order_date__gte=order.order_date - timedelta(minutes=90)
        ).exclude(
            status=Order.COMPLETED
        ).count()
        if order_check > 10:  # cho phép 10 order cùng 1 thời gian
            order.delete()  # xóa đi nếu sai
            logger.info('There are more than 10 orders in a period of time')
            # sau này sẽ làm thêm chức năng kiểm tra nếu request lỗi này đến 1 IP thì đó chính là tấn công
            raise AppException(*AppException.ORDER_FULL)
