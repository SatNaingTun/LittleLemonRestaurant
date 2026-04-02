from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('category', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemDetailView.as_view()),
    path('secret', views.secret),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('me/', views.me, name='me'),
    path('manager-view/', views.manager_view, name='manager_view'),
    path('throttle-check/', views.throttle_check, name='throttle_check'),
    path('throttle-check-auth/', views.throttle_check_auth, name='throttle_check_auth'),
    path('groups/manager/users',views.admin_only_view, name='admin_only_view'),

]