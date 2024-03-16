from rest_framework import serializers
from shopping_cart.models import Product, Order, OrderItem, Payment
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=254)
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            raise serializers.ValidationError(
                {"password2": ["The two password fields didn't match."]}
            )
        try:
            validate_password(password2)
        except Exception as error:
            raise serializers.ValidationError({"password1": list(error)})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=make_password(validated_data["password1"]),
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    default_error_messages = {
        'invalid_credentials': 'Unable to log in with provided credentials.'
    }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(self.default_error_messages['invalid_credentials'])

        if not user.check_password(password):
            raise serializers.ValidationError(self.default_error_messages['invalid_credentials'])

        return {'email': user.email, 'tokens': self.get_tokens_for_user(user)}

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "quantity_available",
        )


class OrderSerializers(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "order_status", "created_at", "updated_at", "total_amount")

    def get_total_amount(self, obj):
        return obj.total_amount

       
class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("quantity", "product")
        read_only_fields = ("order_id", )

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data.get("product")
        if product.quantity_available <= 0:
            raise serializers.ValidationError(
                "Product is unavilable."
            )
        orders = Order.objects.filter(user=user, order_status="CURRENT")
        if orders.exists():
            order = orders[0]
        else:
            order = Order(
            user=user,
            order_status="CURRENT"
            )
            order.save()
        order_items = OrderItem.objects.filter(order=order, product=product)
        if order_items.exists():
            order_item = order_items[0]
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1
            )
        product.quantity_available -= 1
        product.save()
        return order_item
    
    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity')
        if quantity == 0:
            instance.delete()
            return
        instance.quantity = quantity
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "payment_status": {"required": False}
        }
        read_only_fields = ("total_amount", "created_at", "updated_at", "is_success")

    def create(self, validated_data):
        order = validated_data.get("order")
        payment_mode = validated_data.get("payment_mode")
        payment = Payment.objects.create(
            order=order,
            total_amount=order.total_amount,
            payment_mode=payment_mode,
            payment_status='PENDING',
        )
        return payment
    
    def update(self, instance, validated_data):
        payment_status = validated_data.get('payment_status')
        if payment_status in ['SUCCESS', 'FAILED']:
            instance.payment_status = payment_status
            instance.order.order_status = payment_status
            instance.order.save()
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("Invalid status!")