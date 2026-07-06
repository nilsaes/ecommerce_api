from django.contrib import admin
from .models import Category, Product, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_at']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = ['id', 'product']