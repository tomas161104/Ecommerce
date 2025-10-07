from rest_framework.routers import DefaultRouter
from .views import CartViewSet


router_Cart = DefaultRouter()

router_Cart.register(prefix='cart', basename='cart', viewset=CartViewSet)