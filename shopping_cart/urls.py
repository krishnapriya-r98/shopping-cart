from rest_framework import routers
from django.urls import path

from . import views


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("orders", views.OrderViewSet, basename="order")
router.register("order-item", views.OrderItemViewset, basename="order-item")
router.register("payments", views.PaymentViewset, basename="payment")

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
] + router.urls