from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AppException):
        return Response({
            "detail": str(exc),
            "status_code" : exc.status_code
        })

    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class AppException(Exception):
    # danh sách lôi được định nghĩa trước
    PAYMENT_IS_PAID = ['payment is paid',]
    ORDER_BILL_EXISTED = ['order bill is exists',]
    TABLE_BUSY = ['table is busy',]
    TYPE_ERROR = ['has field type invalid',]
    MENU_ITEM_OUT_OF_STOCK = ['menu item is out of stock']

    def __init__(self, message, status_code = 400):
        super().__init__(message)
        self.status_code = status_code