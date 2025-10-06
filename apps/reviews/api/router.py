from rest_framework.routers import DefaultRouter
from .views import ReviewApiViewSet


router_review = DefaultRouter()

router_review.register (prefix='review', basename='review', viewset=ReviewApiViewSet)