"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.reviews.api.router import router_review
from apps.products.api.router import router_product, router_category
from apps.payments.api.router import router_payment
from apps.cart.api.router import router_Cart
from apps.orders.api.router import router_order


SchemaView = get_schema_view(
   openapi.Info(
      title="ecommerce API",
      default_version='v1',
      description="ecommerce API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tomastrigal680@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('apps.users.api.router')),
    path('api/', include(router_review.urls)),
    path('api/', include(router_category.urls)),
    path('api/', include(router_product.urls)),
    path('api/', include(router_payment.urls)),
    path('api/', include(router_Cart.urls)),
    path('api/', include(router_order.urls))
]
