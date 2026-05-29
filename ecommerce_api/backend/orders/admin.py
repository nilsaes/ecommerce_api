from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """Permite ver los productos comprados dentro de la misma pantalla de la Orden"""
    model = OrderItem
    extra = 0
    # Hacemos que estos campos sean de solo lectura para que nadie altere una compra ya hecha
    readonly_fields = ['product_variant', 'quantity', 'price_at_purchase', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columnas que vas a ver en la lista general de órdenes
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    # Filtros laterales para buscar rápido por estado o fecha
    list_filter = ['status', 'created_at']
    # Buscador por nombre de usuario
    search_fields = ['user__username', 'id']
    
    # Metemos los productos de la orden adentro de la vista principal
    inlines = [OrderItemInline]
