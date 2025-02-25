from django.shortcuts import render
from rest_framework import viewsets

from order.models import Order
from .serializer import PaymentSerializer
from .models import Payment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        order = Order.objects.get(pk=request.data.get('order_id'))
        order.status = Order.IN_PROGRESS
        if not order:
            return Response({
                "error" : 'order is not exist'
            }, 400)

        total_amount = 0
        try:
            order_items = order.order_items.all()
            for item in order_items:
                total_amount += item.quantity * item.menu_item.price
        except Exception as e:
            return Response(str(e), 400)

        payment = Payment(
            total_amount=total_amount,
            order=order
        )
        try:
            order.save()
            payment.save()
            return Response(PaymentSerializer(payment).data, 201)
        except Exception as e:
            return Response({'error' : str(e)}, 400)

    @action(methods=['put'], detail=True)
    def pay(self, request, pk = None):
        payment = self.get_object()
        order = payment.order
        method = request.data.get('method')

        #kiểm tra nếu hóa đơn đó đã được thanh toán rôi thì không thanh toán lại nữa
        if payment.paid:
            return Response({
                'message' : 'payment is paid'
            }, 400)

        #update
        payment.paid = True
        order.tables.clear()
        order.status = Order.COMPLETED
        print("method is : " + str(method))
        if method:
            payment.method = method

        try:
            order.save()
            payment.save()
            return Response(PaymentSerializer(payment).data)
        except Exception as e:
            return Response({
                'error': str(e)
            }, 400)