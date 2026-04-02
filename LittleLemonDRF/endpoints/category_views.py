from rest_framework import generics, permissions
from ..models import Category
from ..serializers import CategorySerializer
from ..permissions import IsManager

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Public or Authenticated users can see the categories
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        # Only Managers can create a new category (POST)
        return [IsManager()]