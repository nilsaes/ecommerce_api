from rest_framework import serializers
from .models import Cart, CartItem
from core.models import ProductVariant

class CartItemSerializer(serializers.ModelSerializer):
    # Traemos detalles de la variante para que el frontend pueda mostrar el nombre, talla y color
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    size = serializers.CharField(source='product_variant.size', read_only=True)
    color = serializers.CharField(source='product_variant.color', read_only=True)
    price = serializers.DecimalField(source='product_variant.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'product_name', 'size', 'color', 'price', 'quantity', 'subtotal']

    def validate(self, data):
        # ¡Validación Avanzada de Stock! Evitamos que metan al carrito más de lo que hay disponible
        variant = data['product_variant']
        quantity = data['quantity']
        
        if quantity > variant.stock:
            raise serializers.ValidationError(
                f"No podés agregar {quantity} unidades. Solo quedan {variant.stock} en stock de esta variante."
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    # Anidamos los ítems adentro del carrito para ver todo el detalle junto
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']