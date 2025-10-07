from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router_order = DefaultRouter()

router_order.register(prefix='order', basename='order', viewset=OrderViewSet)