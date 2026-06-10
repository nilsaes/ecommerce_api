from django.contrib import admin
from .models import Product, ProductVariant, Cart, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'price', 'stock')
    list_filter = ('size', 'color', 'product')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    # Quitamos 'subtotal' de readonly_fields para evitar el error E035
    readonly_fields = () 

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Dejamos solo los campos reales que existen en tu clase Cart
    list_display = ('id', 'user', 'created_at') 
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # Dejamos solo los campos reales que existen en tu clase CartItem
    list_display = ('id', 'cart', 'product_variant', 'quantity')