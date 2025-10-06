from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin (admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'added_at']