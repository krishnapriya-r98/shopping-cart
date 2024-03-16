from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

from shopping_cart.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    username = models.CharField(unique=False, null=True, max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return super().__str__()


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()


class Order(models.Model):
    order_status_choices = (
        ("CURRENT", "CURRENT"), ("SUCCESS", "SUCCESS"), ("FAILED", "FAILED"), ("CANCELLED", "CANCELLED")
    )
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    order_status = models.CharField(choices=order_status_choices, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()

    @property
    def total_amount(self):
        total_amount = sum([i.total for i in self.orderitem_set.all()])
        return total_amount



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return super().__str__()

    @property
    def total(self):
        return round(float(self.product.price) * float(self.quantity))


class Payment(models.Model):
    payment_choices = (
        ("CREDIT_CARD", "CREDIT_CARD"), ("DEBIT_CARD", "DEBIT_CARD")
        )
    payment_status_choices = (
        ("SUCCESS", "SUCESS"), ("PENDING", "PENDING"), ("FAILED", "FAILED")
        )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(choices=payment_choices, max_length=15)
    payment_status = models.CharField(choices=payment_status_choices, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return super().__str__()