from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('item', views.MenuItemViewSet, 'item')
router.register('category', views.MenuCategoryViewSet, 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('item/<int:pk>/image', views.UploadMenuItem.as_view())
]
