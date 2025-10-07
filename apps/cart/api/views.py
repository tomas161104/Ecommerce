# apps/cart/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from apps.cart.models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer
from .permissions import IsCartOwner
from apps.products.models import Product

class CartViewSet(viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.filter(user=user)

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart, context={'request': request})
        data = serializer.data
        data['total_items'] = cart.total_items()
        data['total_price'] = cart.total_price()
        return Response(data)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def add_item(self, request):
        """
        payload: { "product": <id>, "quantity": 1 }
        si ya existe el item, incrementa la cantidad
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        qty = serializer.validated_data['quantity']

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': qty})
        if not created:
            new_qty = item.quantity + qty
            if product.stock < new_qty:
                return Response({"detail": "Not enough stock."}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = new_qty
            item.save()
        else:
            if product.stock < item.quantity:
                return Response({"detail": "Not enough stock."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'])
    @transaction.atomic
    def update_item(self, request):
        """
        payload: { "item_id": <id>, "quantity": <n> }
        """
        item_id = request.data.get('item_id')
        qty = int(request.data.get('quantity', 0))
        try:
            item = CartItem.objects.select_related('product', 'cart').get(pk=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        if qty < 1:
            return Response({'detail': 'Quantity must be >= 1'}, status=status.HTTP_400_BAD_REQUEST)
        if item.product.stock < qty:
            return Response({'detail': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = qty
        item.save()
        return Response(CartSerializer(item.cart, context={'request': request}).data)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def remove_item(self, request):
        """
        payload: { "item_id": <id> }
        """
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart, context={'request': request}).data)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def clear(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'detail': 'Cart cleared'}, status=status.HTTP_200_OK)
