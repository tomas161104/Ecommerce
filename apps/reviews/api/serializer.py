from rest_framework import serializers
from apps.reviews.models import Review
from apps.users.api.serializer import UserSerializer
from apps.products.api.serializer import ProductSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer
    product = ProductSerializer
    class Meta:
        model = Review
        fields = ['id', 'product', 'img', 'content', 'user']