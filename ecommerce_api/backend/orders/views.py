from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(mixins.CreateModelMixin, 
                mixins.ListModelMixin, 
                mixins.RetrieveModelMixin, 
                viewsets.GenericViewSet):
    """
    ViewSet que permite a los usuarios logueados crear órdenes,
    ver la lista de sus órdenes y ver el detalle de una orden específica.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] # Súper seguro: solo usuarios logueados

    def get_queryset(self):
        # El cliente SOLO puede ver sus propias órdenes de compra
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Al guardar la orden, le inyectamos de forma segura el usuario que disparó la petición
        serializer.save(user=self.request.user)
