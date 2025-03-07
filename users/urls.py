from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register('', views.UserViewSet)
# router.register('upload_avatar', views.UploadAvatar, 'upload'),
urlpatterns = [
    path('<int:pk>/info', views.MyAccount.as_view()),
    path('info', views.Info.as_view()),
    path('register', views.RegisterUser.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('upload_avatar/<int:pk>', views.UploadAvatar.as_view()),
    path('', include(router.urls)),
]


