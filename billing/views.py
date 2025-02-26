from django.shortcuts import render
from rest_framework import viewsets

from app.exception import AppException
from order.models import Order
from .serializer import PaymentSerializer
from .models import Payment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        print(kwargs)
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        payment = Payment(
            total_amount= self.get_total_amount(order),
            order=order
        )
        self.create_bill(payment)
        return Response(PaymentSerializer(payment).data)

    @action(methods=['put'], detail=True)
    def pay(self, request, pk = None):
        payment = self.get_object()
        order = payment.order
        method = request.data.get('method')

        #kiểm tra nếu hóa đơn đó đã được thanh toán rôi thì không thanh toán lại nữa
        if payment.paid:
            raise AppException(*AppException.PAYMENT_IS_PAID)

        #update
        self.handle_pay(payment, method)

        return Response(PaymentSerializer(payment).data)

    def get_total_amount(self, order):
        total_amount = 0
        order_items = order.order_items.all()
        for item in order_items:
            total_amount += item.quantity * item.menu_item.price
        return total_amount
    def create_bill(self, payment):
        if payment.order.status == Order.IN_PROGRESS:
            raise AppException(*AppException.ORDER_BILL_EXISTED)
        payment.order.status = Order.IN_PROGRESS
        payment.order.save()
        payment.save()
    def handle_pay(self, payment, method):
        payment.paid = True
        payment.order.status = Order.COMPLETED
        payment.method = method or payment.method

        # Update tình trạng bàn là không bận và xóa order khỏi bàn đó
        for table in payment.order.tables.all():
            table.is_busy = False
            table.order.remove(payment.order)
            table.save()

        payment.order.save()
        payment.save()
