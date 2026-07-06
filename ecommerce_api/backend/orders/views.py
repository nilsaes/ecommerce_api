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
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
    
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
            
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)
