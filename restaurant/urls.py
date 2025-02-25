"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API",
        default_version='v1',
        description="API documentation for the Restaurant Management System",
        terms_of_service="https://www.your-restaurant.com/terms/",
        contact=openapi.Contact(email="support@your-restaurant.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
      path('admin/', admin.site.urls),
      path('user/', include('users.urls')),
      path('order/', include('order.urls')),
      path('menu/', include('menu.urls')),
      path('table/', include('table.urls')),
      path('billing/', include('billing.urls')),
      # url(r'^$', schema_view)

      path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
      path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
