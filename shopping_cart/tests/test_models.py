from django.test import TestCase
from django.contrib.auth import get_user_model
from shopping_cart.models import Product, Order, OrderItem, Payment

User = get_user_model()

class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))

class ProductModelTestCase(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Test Product", price=10.99)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 10.99)

class OrderModelTestCase(TestCase):
    def test_order_creation(self):
        user = User.objects.create_user(email="test@example.com", password="testpassword")
        order = Order.objects.create(user=user, order_status="CURRENT")
        self.assertEqual(order.user, user)
        self.assertEqual(order.order_status, "CURRENT")

class OrderItemModelTestCase(TestCase):
    def test_order_item_creation(self):
        product = Product.objects.create(name="Test Product", price=10.99)
        user = User.objects.create_user(email="test@example.com", password="testpassword")
        order = Order.objects.create(user=user, order_status="CURRENT")
        order_item = OrderItem.objects.create(product=product, order=order, quantity=2)
        self.assertEqual(order_item.product, product)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.quantity, 2)

class PaymentModelTestCase(TestCase):
    def test_payment_creation(self):
        user = User.objects.create_user(email="test@example.com", password="testpassword")
        order = Order.objects.create(user=user, order_status="CURRENT")
        payment = Payment.objects.create(order=order, total_amount=20.50, payment_mode="CREDIT_CARD", payment_status="PENDING")
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.total_amount, 20.50)
        self.assertEqual(payment.payment_mode, "CREDIT_CARD")
        self.assertEqual(payment.payment_status, "PENDING")
