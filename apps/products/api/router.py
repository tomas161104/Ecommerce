from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router_product = DefaultRouter()

router_product.register(prefix='product', basename='product', viewset=ProductViewSet)


router_category = DefaultRouter()

router_category.register(prefix='category', basename='category', viewset=CategoryViewSet)