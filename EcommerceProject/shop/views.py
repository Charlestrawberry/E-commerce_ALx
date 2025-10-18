from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import Product, Category, Order, OrderItem, Review, Payment
from .Serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    ReviewSerializer,
    PaymentSerializer,
)
from .payment import create_payment_intent  # keep your existing payment helper


# Custom permission: only admin/staff can create/update/delete products
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Safe methods allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # For unsafe methods require staff or superuser
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description"]
    filterset_fields = {
        "category": ["exact"],
        "price": ["gte", "lte"],
        "stock": ["gte", "lte"],
    }


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # only return user's orders unless staff
        if request.user.is_staff:
            qs = self.get_queryset()
        else:
            qs = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Expect payload like:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1}
            ]
        }
        """
        items = request.data.get("items", [])
        if not items:
            return Response({"detail": "No items provided."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            total = 0
            order = Order.objects.create(user=request.user, total_amount=0)
            created_items = []
            for it in items:
                product_id = it.get("product_id")
                qty = int(it.get("quantity", 1))
                try:
                    product = Product.objects.select_for_update().get(pk=product_id)
                except Product.DoesNotExist:
                    transaction.set_rollback(True)
                    return Response({"detail": f"Product {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)
                if product.stock < qty:
                    transaction.set_rollback(True)
                    return Response({"detail": f"Not enough stock for product {product.name}."}, status=status.HTTP_400_BAD_REQUEST)
                price = product.price
                OrderItem.objects.create(order=order, product=product, quantity=qty, price_at_order=price)
                # decrement stock
                product.stock -= qty
                product.save()
                total += float(price) * qty
                created_items.append({"product": product.name, "quantity": qty})

            order.total_amount = total
            order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("product", "user").all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("order").all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="create-intent")
    def create_intent(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response({"detail": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)
        intent = create_payment_intent(float(amount))
        return Response({"client_secret": intent.client_secret})


# simple function endpoint (kept for compatibility)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_payment(request):
    amount = request.data.get("amount")
    intent = create_payment_intent(float(amount))
    return Response({"client_secret": intent.client_secret})
