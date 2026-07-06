from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart

class OrderItemSerializer(serializers.ModelSerializer):
    # Detalles adicionales para que el frontend muestre lindo el resumen
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    size = serializers.CharField(source='product_variant.size', read_only=True)
    color = serializers.CharField(source='product_variant.color', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'product_name', 'size', 'color', 'quantity', 'price_at_purchase', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'shipping_address', 'phone_number', 'items', 'total']
        read_only_fields = ['user', 'status']

    def create(self, validated_data):
        
        user = self.context['request'].user
        
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("No tenés un carrito activo para transformar en orden.")

        
        if not cart.items.exists():
            raise serializers.ValidationError("Tu carrito está vacío. Agrega productos antes de comprar.")

        
        with transaction.atomic():
            # 1. Creamos la orden principal
            order = Order.objects.create(
                user=user,
                shipping_address=validated_data['shipping_address'],
                phone_number=validated_data['phone_number']
            )

            
            for cart_item in cart.items.all():
                variant = cart_item.product_variant

                if cart_item.quantity > variant.stock:
                    raise serializers.ValidationError(
                        f"¡Lo sentimos! Ya no hay stock suficiente de {variant.product.name} ({variant.size}/{variant.color}). Solo quedan {variant.stock} unidades."
                    )

                
                variant.stock -= cart_item.quantity
                variant.save()

                
                OrderItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=cart_item.quantity,
                    price_at_purchase=variant.price 
                )

            
            cart.items.all().delete()

        return order