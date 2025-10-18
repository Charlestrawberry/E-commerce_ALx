from rest_framework import viewsets, permissions
from .models import Product, Category, Order, OrderItem, Review, Payment
from .Serializers import CategorySerilizers, ProductSerilizers, OrderSerilizers, OrderItemSerilizers, ReviewSerilizers, PaymentSerilizers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerilizers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerilizers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerilizers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerilizers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]