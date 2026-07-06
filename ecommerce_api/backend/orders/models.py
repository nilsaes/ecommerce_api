from django.db import models
from django.contrib.auth.models import User
from core.models import ProductVariant

class Order(models.Model):
    # Estados posibles de la orden
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente de Pago'),
        ('PAID', 'Pagado'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Datos de envío básicos
    shipping_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Orden {self.id} - {self.user.username} ({self.get_status_display()})"

    @property
    def total_price(self):
    
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    

    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_variant} (Orden {self.order.id})"

    @property
    def subtotal(self):
        return self.quantity * self.price_at_purchase