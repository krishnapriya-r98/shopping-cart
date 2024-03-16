from shopping_cart.models import Product, Order, Payment, OrderItem
from rest_framework import viewsets
from shopping_cart.serializers import ProductSerializer, OrderSerializers, OrderItemSerializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import PaymentSerializer, RegisterSerializer, LoginSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().create(request)
        else:
            return Response("You do not have permission to create a Product", status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().update(request)
        else:
            return Response("You do not have permission to edit a Product", status=status.HTTP_400_BAD_REQUEST)      

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializers
    queryset = Order.objects.all().order_by("id")


class OrderItemViewset(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializers
    queryset = OrderItem.objects.all().order_by("id")

class PaymentViewset(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by("id")


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
