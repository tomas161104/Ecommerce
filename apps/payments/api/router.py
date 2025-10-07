from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet


router_payment = DefaultRouter()
router_payment.register(prefix='payment', basename='payment', viewset=PaymentViewSet)