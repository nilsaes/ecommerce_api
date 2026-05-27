from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """Esto permite ver y editar los productos adentro del mismo carrito"""
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'created_at', 'updated_at']
    inlines = [CartItemInline] # Metemos los ítems adentro del panel del carrito

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product_variant', 'quantity', 'subtotal']