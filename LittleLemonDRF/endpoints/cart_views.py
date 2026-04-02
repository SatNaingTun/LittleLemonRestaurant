from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Cart, MenuItem
from ..serializers import CartSerializer

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        # Returns current items in the cart for the current user token
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 1. Get the menuitem ID from the POST data
        menuitem_id = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')
        
        # 2. Fetch the MenuItem object to get the real price
        item = get_object_or_404(MenuItem, pk=menuitem_id)
        
        # 3. Calculate prices
        unit_price = item.price
        total_price = int(quantity) * unit_price
        
        # 4. Save with the authenticated user and calculated values
        serializer.save(
            user=self.request.user, 
            unit_price=unit_price, 
            price=total_price
        )

    def delete(self, request, *args, **kwargs):
        # Deletes all menu items created by the current user token
        self.get_queryset().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)