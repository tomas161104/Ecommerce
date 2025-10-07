from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.api.serializer import ProductSerializer 
from apps.cart.api.serializer import CartItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'price']
        read_only_fields = ['id', 'product_detail', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'shipping_address', 'payment', 'items', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'total', 'payment', 'created_at']
