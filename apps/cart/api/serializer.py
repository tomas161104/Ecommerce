# apps/cart/serializers.py
from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.api.serializer import ProductSerializer 

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=...) 
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'added_at']
        read_only_fields = ['id', 'product_detail', 'added_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def validate(self, attrs):
        product = attrs.get('product') or getattr(self.instance, 'product', None)
        qty = attrs.get('quantity') or getattr(self.instance, 'quantity', None)
        if product and qty:
            if product.stock < qty:
                raise serializers.ValidationError("Not enough stock for this product.")
        return attrs

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price', 'created_at']
        read_only_fields = ['id', 'user', 'items', 'total_items', 'total_price', 'created_at']
