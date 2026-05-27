from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ProductViewSet, CategoryViewSet

# Creamos el enrutador automático de Django REST Framework
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conectamos las rutas del enrutador a la URL de nuestra API
    path('api/', include(router.urls)),
]