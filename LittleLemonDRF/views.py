from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    # The data source for this view
    queryset = MenuItem.objects.all()

    # The serializer used to validate and map the data
    serializer_class = MenuItemSerializer

    # Fields that can be used for sorting (e.g., ?ordering=price)
    ordering_fields = ['price', 'inventory']

    # Fields that can be used for exact filtering
    filterset_fields = ['price', 'inventory']

    # Fields that can be used for text-based search (e.g., ?search=bakery)
    search_fields = ['category__title']


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer




