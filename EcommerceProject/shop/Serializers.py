from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, Order, OrderItem, Review, Payment

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True, required=True
    )
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["created_at", "category"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name is required.")
        return value

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Stock must be 0 or a positive integer.")
        return value
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.all(), write_only=True)
    class Meta:

        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Order
        fields = "__all__"
    
    def create(self, validated_data):
        # items will be processed in the view (we will handle stock update there)
        raise NotImplementedError("Use OrderViewSet.create to handle order creation logic.")

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]
        read_only_fields = ["created_at", "user"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["created_at"]
    
