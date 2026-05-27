from django.db import models
from django.contrib.auth import get_user_model
from core.models import ProductVariant  # Ahora sí tiene sentido importar desde core

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.username if self.user else 'Invitado'} - ID: {self.id}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.size}/{self.product_variant.color})"

    @property
    def subtotal(self):
        # Nota: Si en tu modelo de core.models el precio se llama diferente (ej. price), mapealo acá
        return self.product_variant.price * self.quantity