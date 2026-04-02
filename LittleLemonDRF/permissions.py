from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Ensure this returns a Boolean (True/False)
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Delivery-Crew').exists()