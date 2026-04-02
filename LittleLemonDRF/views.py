from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    # The data source for this view
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
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
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search=request.query_params.get('search')
        ordering=request.query_params.get('ordering')
        perpage=request.query_params.get('perpage',default=2)
        page=request.query_params.get('page',default=1)
        if category_name:
            menu_items = menu_items.filter(category__title=category_name)
        if to_price:
            menu_items = menu_items.filter(price__lte=to_price)
        if search:
            menu_items = menu_items.filter(title__icontains=search)
        if ordering:
            ordering_fields=ordering.split(',')  # Split the ordering fields by comma
            menu_items = menu_items.order_by(*ordering_fields)
        paginator = Paginator(menu_items, per_page=perpage)
        try:
            menu_items = paginator.page(page)
        except PageNotAnInteger:
            menu_items = paginator.page(1)
        except EmptyPage:
            menu_items = []
            # menu_items = paginator.page(paginator.num_pages)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "This is a secret message!"})

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only managers should see this!"})
    else:
        return Response({"message": "You are not authorized to view this."}, status=status.HTTP_403_FORBIDDEN)
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(requsest):
    return Response({"message": "successfully accessed throttle check endpoint!"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message": "successfully accessed throttle check endpoint!"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_only_view(request):
    username=request.data['username']
    if username:
        try:
            user=get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='Manager')
            if request.method == 'POST':
                manager_group.user_set.add(user)
            elif request.method == 'DELETE':
                manager_group.user_set.remove(user)
            return Response({"message": f"User '{username}' has been modified."})
        except User.DoesNotExist:
            return Response({"message": f"User '{username}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"message": "Manager group does not exist."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)