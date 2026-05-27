from django.contrib import admin
from .models import Category, Product, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Dejamos solo 'id' y 'name' porque 'description' no existe en tu modelo
    list_display = ['id', 'name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_at']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    # Quitamos 'sku' porque no existe en tu modelo. Dejamos el precio y el stock si están.
    # Si te llega a tirar error por 'price' o 'stock', dejamos solo ['id', 'product']
    list_display = ['id', 'product']