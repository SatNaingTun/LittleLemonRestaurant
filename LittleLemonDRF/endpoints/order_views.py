from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..models import Order, OrderItem, Cart, MenuItem
from ..serializers import OrderSerializer
from ..permissions import IsManager # Assuming you have a custom permission class

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Manager: Returns all orders with order items by all users
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        
        # Delivery crew: Returns all orders assigned to them
        if user.groups.filter(name='Delivery-crew').exists():
            return Order.objects.filter(delivery_crew=user)
        
        # Customer: Returns all orders created by this user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # 1. Get current cart items for the user
        cart_items = Cart.objects.filter(user=self.request.user)
        
        if not cart_items.exists():
            # If the cart is empty, we can't create an order
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Calculate the total price for the Order record
        total = sum([item.price for item in cart_items])
        
        # 3. Save the Order (Sets user, total, and current date)
        order = serializer.save(user=self.request.user, total=total, date=timezone.now().date())

        # 4. Create OrderItem records from Cart items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        
        # 5. Delete all items from the cart for this user
        cart_items.delete()

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        # Customers and Delivery Crew only see orders related to them
        if user.groups.filter(name='Delivery-crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = self.request.user

        # CUSTOMER logic: Cannot update anything (usually returns 403 or limited)
        if not user.groups.filter(name__in=['Manager', 'Delivery-crew']).exists():
            return Response({"message": "Customers cannot update orders"}, status=status.HTTP_403_FORBIDDEN)

        # DELIVERY CREW logic: Can only update 'status'
        if user.groups.filter(name='Delivery-crew').exists():
            # Check if they are trying to update fields other than 'status'
            if set(request.data.keys()) == {'status'}:
                return super().update(request, *args, **kwargs)
            return Response({"message": "Delivery crew can only update status"}, status=status.HTTP_403_FORBIDDEN)

        # MANAGER logic: Can update status and delivery_crew
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Only Managers can delete orders
        if self.request.user.groups.filter(name='Manager').exists():
            return super().delete(request, *args, **kwargs)
        return Response({"message": "Only managers can delete orders"}, status=status.HTTP_403_FORBIDDEN)