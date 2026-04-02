from rest_framework import generics, permissions
from ..models import MenuItem
from ..serializers import MenuItemSerializer
from ..permissions import IsManager 

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        # Allow anyone (even without a token/login) to view the menu
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        
        # Only Managers can POST (Create)
        # This will return 403 if you aren't logged in AS a Manager
        return [IsManager()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        # Allow anyone to view a single item detail
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        
        # Only Managers can PUT, PATCH, or DELETE
        return [IsManager()]