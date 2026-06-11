from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem, ProductVariant
from orders.models import Order, OrderItem
from .serializers import CartSerializer # Asegurate de que este import coincida con tu archivo serializers

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        # Retorna el carrito únicamente del usuario logueado
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """ Lógica para agregar productos al carrito de forma segura """
        variant_id = request.data.get('product_variant_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            variant = ProductVariant.objects.get(id=variant_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            
            # Si el producto ya está en el carrito, le sumamos la cantidad
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()
            return Response({"message": "Producto agregado con éxito"}, status=status.HTTP_201_CREATED)
            
        except ProductVariant.DoesNotExist:
            return Response({"error": "La variante de producto no existe"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_purchase(request):
    """ Mueve los productos del carrito a una orden real y limpia el carrito """
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular el total de la compra
        total_orden = sum(item.product_variant.price * item.quantity for item in cart_items)

        # Crear la orden de compra maestra
        nueva_orden = Order.objects.create(
            user=request.user,
            total=total_orden,
            status='PAGADO'
        )

        # Traspasar ítems del carrito congelando precio y metadatos
        for item in cart_items:
            OrderItem.objects.create(
                order=nueva_orden,
                product_variant=item.product_variant,
                product_name=item.product_variant.product.name,
                size=item.product_variant.size,
                color=item.product_variant.color,
                price=item.product_variant.price,
                quantity=item.quantity
            )

        # Vaciar el carrito de la base de datos
        cart_items.delete()

        return Response({
            "message": "¡Compra procesada con éxito!",
            "order_id": nueva_orden.id,
            "total": total_orden
        }, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({"error": "No hay un carrito activo para este usuario"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error en la transacción: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)