# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from .serializer import OrderSerializer
from apps.cart.models import Cart, CartItem
from apps.payments.models import Payment

class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'is_staff_member', False):
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Checkout: crea Order + OrderItems + Payment(pending) + decrementa stock.
        Payload opcional: {"shipping_address":"...", "payment_method":"card"}
        """
        user = request.user
        shipping_address = request.data.get('shipping_address')
        payment_method = request.data.get('payment_method', 'card')  # demo

        if not shipping_address:
            return Response({"detail":"shipping_address required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=user)
        items = list(cart.items.select_related('product').all())
        if not items:
            return Response({"detail":"Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Transacción atómica y lock en productos
        with transaction.atomic():
            # Lock products rows
            product_ids = [ci.product.id for ci in items]
            products = {p.id: p for p in (Product.objects.select_for_update().filter(id__in=product_ids))}

            total = 0
            # verificar stock
            for ci in items:
                prod = products.get(ci.product.id)
                if not prod:
                    return Response({"detail": f"Product {ci.product.id} not found"}, status=status.HTTP_400_BAD_REQUEST)
                if prod.stock < ci.quantity:
                    return Response({"detail": f"Not enough stock for product {prod.id}"}, status=status.HTTP_400_BAD_REQUEST)
                total += prod.price * ci.quantity

            # crear Order
            order = Order.objects.create(user=user, total=total, shipping_address=shipping_address, status='pending')

            # crear order items y decrementar stock
            for ci in items:
                prod = products[ci.product.id]
                OrderItem.objects.create(order=order, product=prod, quantity=ci.quantity, price=prod.price)
                prod.stock -= ci.quantity
                prod.save()

            # crear Payment pendiente (luego webhook o procesamiento marcará completed)
            payment = Payment.objects.create(user=user, amount=total, method=payment_method, status='pending')
            order.payment = payment
            order.save()

            # vaciar carrito
            cart.items.all().delete()

        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
