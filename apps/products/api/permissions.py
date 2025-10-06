from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Solo el admin puede modificar el recurso.
    Lectura permitida para todos.
    """

    def has_permission(self, request, view):
        # Lectura siempre permitida
        if request.method in permissions.SAFE_METHODS:
            return True

        # Escritura solo si es admin
        return request.user.is_superuser
