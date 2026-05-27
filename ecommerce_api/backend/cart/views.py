from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from core.models import ProductVariant

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated] # Exigimos que el usuario esté logueado

    def get_queryset(self):
        # Cada usuario solo puede ver SU propio carrito
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Cuando se crea un carrito, se lo asignamos automáticamente al usuario actual
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        """Ruta personalizada para agregar o actualizar ítems en el carrito"""
        # Intentamos obtener el carrito del usuario; si no existe, se lo creamos en el acto
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        variant_id = request.data.get('product_variant')
        quantity = int(request.data.get('quantity', 1))

        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error": "La variante de producto no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Buscamos si esa variante ya estaba en el carrito
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

        if not item_created:
            # Si ya existía, le sumamos la nueva cantidad
            cart_item.quantity += quantity
        else:
            # Si es nuevo, le asignamos la cantidad inicial
            cart_item.quantity = quantity

        # Validamos el stock usando el serializador antes de guardar de verdad
        serializer = CartItemSerializer(cart_item, data={'quantity': cart_item.quantity, 'product_variant': variant.id}, partial=True)
        if serializer.is_valid():
            cart_item.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)