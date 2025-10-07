# apps/orders/permissions.py
from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or getattr(request.user, 'is_staff_member', False):
            return True
        return obj.user == request.user

    def has_permission(self, request, view):
        # Para list/create: autenticado
        return request.user and request.user.is_authenticated
