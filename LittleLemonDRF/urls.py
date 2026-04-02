from django.urls import path

from .endpoints.menu_views import MenuItemView, SingleMenuItemView
from .endpoints.group_views import GroupUserView, GroupUserDeleteView
from .endpoints.cart_views import CartView
from .endpoints.order_views import OrderView, SingleOrderView
from .endpoints.user_views import CurrentUserView,UserRegistrationView
from .endpoints.category_views import CategoryView

urlpatterns = [
    
    # Users
    path('users', UserRegistrationView.as_view()),
    path('users/users/me/', CurrentUserView.as_view()),
    
    # Categories
    path('categories/', CategoryView.as_view()),
    path('categories/<int:pk>', CategoryView.as_view()),

    # Menu Items
    path('menu-items', MenuItemView.as_view()),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view()),

    # User Group Management
    path('groups/manager/users', GroupUserView.as_view()),
    path('groups/manager/users/<int:pk>', GroupUserDeleteView.as_view()),
    path('groups/delivery-crew/users', GroupUserView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', GroupUserDeleteView.as_view()),

    # Cart Management
    path('cart/menu-items', CartView.as_view()),

    # Order Management
    path('orders', OrderView.as_view()),
    path('orders/<int:pk>', SingleOrderView.as_view()),
]