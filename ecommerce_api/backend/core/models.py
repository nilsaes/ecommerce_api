from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50)   # Talla (ej: M, L, XL)
    color = models.CharField(max_length=50)  # Color (ej: Negro, Blanco)
    price = models.DecimalField(max_length=10, decimal_places=2, max_digits=10) # Precio específico de la variante
    stock = models.PositiveIntegerField(default=0) # Stock disponible de esta variante

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.color}"