from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

from .views import SubmitOrder

router = DefaultRouter()
router.register(
    '',
    views.OrderViewSet
)

urlpatterns = [
    path('', include(router.urls)),
    path('submit', SubmitOrder.as_view())
]
