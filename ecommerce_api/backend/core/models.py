from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50, blank=True, null=True)  # Ejemplo: S, M, L o Talle 40
    color = models.CharField(max_length=50, blank=True, null=True) # Ejemplo: Rojo, Negro
    price = models.DecimalField(max_digits=10, decimal_places=2)    # Soporta montos grandes para Guaraníes o dólares
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.color}"
    
    class Cart(models.Model):
    # Por ahora lo dejamos simple. Más adelante lo vincularemos con el usuario si el profesor lo pide.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito Nro: {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"
    
    @property
    def total_price(self):
        # Multiplica la cantidad por el precio de la variante elegida
        return self.quantity * self.product_variant.price