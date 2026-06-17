from rest_framework import serializers
from .models import Cart, CartItem
from core.models import ProductVariant

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    size = serializers.CharField(source='product_variant.size', read_only=True)
    color = serializers.CharField(source='product_variant.color', read_only=True)
    price = serializers.DecimalField(source='product_variant.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'product_name', 'size', 'color', 'price', 'quantity', 'subtotal']

    def validate(self, data):

        variant = data['product_variant']
        quantity = data['quantity']
        
        if quantity > variant.stock:
            raise serializers.ValidationError(
                f"No podés agregar {quantity} unidades. Solo quedan {variant.stock} en stock de esta variante."
            )
        return data


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        #fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        def get_total_price(self, obj):
         return sum(item.quantity * item.product_variant.price for item in obj.items.all())