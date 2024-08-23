from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Пользователь имеет доступ только если он является владельцем объекта или администратором.
    """

    message = 'Доступ запрещен. Вы не являетесь владельцем или администратором.'

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли текущий пользователь владельцем объекта или администратором
        if obj.owner == request.user or request.user.is_staff:
            return True
        return False