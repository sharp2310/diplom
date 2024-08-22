from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from edu_modules.models import Module
from edu_modules.pagination import ModulePagination
from edu_modules.permissions import IsModeratorOrAuthor
from edu_modules.serialozers import ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulePagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.author = self.request.user
        new_module.save()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModeratorOrAuthor]

        return [permission() for permission in permission_classes]