from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, confirm_purchase

router = DefaultRouter()
router.register(r'my-cart', CartViewSet, basename='my-cart')

urlpatterns = [
    path('', include(router.urls)),
    path('confirm-purchase/', confirm_purchase, name='confirm-purchase'),
]