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
    
    readonly_fields = () 

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'created_at') 
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'cart', 'product_variant', 'quantity')