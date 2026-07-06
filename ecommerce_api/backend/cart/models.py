from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. MODELOS DE PRODUCTOS Y VARIANTES
# ==========================================

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50)   # Ej: S, M, L, XL
    color = models.CharField(max_length=50)  # Ej: Violeta, Negro
    price = models.DecimalField(max_digits=12, decimal_places=2)

    stock = models.IntegerField(default=9999) 

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.color}"


# ==========================================
# 2. MODELOS PARA EL CARRITO DE COMPRAS
# ==========================================

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant} en el carrito"


