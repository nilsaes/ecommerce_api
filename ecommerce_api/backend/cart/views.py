from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Cart, CartItem
from orders.models import Order, OrderItem
from core.models import ProductVariant
from .serializers import CartSerializer 
from django.contrib.auth import get_user_model

User = get_user_model()

class CartViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Cart.objects.filter(user_id=1)
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """ Lógica para agregar productos al carrito de forma segura """
        variant_id = request.data.get('product_variant_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            variant = ProductVariant.objects.get(id=variant_id)
            
            if request.user.is_anonymous:
                target_user = User.objects.get(id=1)
            else:
                target_user = request.user

            cart, _ = Cart.objects.get_or_create(user=target_user)
            
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
@permission_classes([AllowAny])
def confirm_purchase(request):
    """ Mueve los productos del carrito a una orden real y limpia el carrito """
    try:
        # 1. Identificar el usuario de pruebas
        if request.user.is_anonymous:
            target_user = User.objects.get(id=1)
        else:
            target_user = request.user

        cart = Cart.objects.get(user=target_user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Crear la orden de compra maestra
        nueva_orden = Order.objects.create(
            user=target_user,
            status='PAID',  
            shipping_address="Dirección de Prueba 123",
            phone_number="123456789"
        )

        # 3. Traspasar ítems del carrito usando 'price_at_purchase'
        for item in cart_items:
            OrderItem.objects.create(
                order=nueva_orden,
                product_variant_id=item.product_variant.id,
                quantity=item.quantity,
                price_at_purchase=item.product_variant.price 
            )

        
        total_final = nueva_orden.total_price

        # 4. Vaciar el carrito de la base de datos
        cart_items.delete()

        return Response({
            "message": "¡Compra procesada con éxito!",
            "order_id": nueva_orden.id,
            "total": total_final
        }, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({"error": "No hay un carrito activo para este usuario"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error en la transacción: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)