from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # This treats 'category' as a foreign key ID
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CurrentUserView(APIView):
    # Only users with a valid Token can access this
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        # menuitem and quantity MUST be writable
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        
        # ONLY these should be read_only
        read_only_fields = ['user', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']
        
class OrderSerializer(serializers.ModelSerializer):
    # If you have order_items nested, keep those here too
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
        # Add this line to stop the "This field is required" error
        read_only_fields = ['user', 'total', 'date']