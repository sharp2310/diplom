from rest_framework.permissions import BasePermission


class IsAdminOrSelfUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user