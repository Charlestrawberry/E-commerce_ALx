from rest_framework import serializers
from .models import Product, Category, Order, OrderItem, Review, Payment


class CategorySerilizers(serializers.ModelSerializer):
    class meta:
        model = Category
        fields = "__all__"
        
class ProductSerilizers(serializers.ModelSerializer):
    category = CategorySerilizers(read_only=True)
    class meta:
        model = Product
        fields = "__all__"
        
class OrderItemSerilizers(serializers.ModelSerializer):
    class meta:

        model = OrderItem
        fields = "__all__"

class OrderSerilizers(serializers.ModelSerializer):
    items = OrderItemSerilizers(many=True, read_only=True)
    class meta:
        model = Order
        fields = "__all__"

class ReviewSerilizers(serializers.ModelSerializer):
    class meta:
        model = Review
        fields = "__all__"

class PaymentSerilizers(serializers.ModelSerializer):
    class meta:
        model = Payment
        fields = "__all__"
    
