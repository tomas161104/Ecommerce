
from rest_framework import permissions

class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_superuser
        if hasattr(obj, 'cart'):
            return obj.cart.user == request.user or request.user.is_superuser
        return False
