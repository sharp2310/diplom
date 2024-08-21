from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from modules.models import Module
from modules.paginators import MyPagination
from modules.serializers import ModuleSerializer
from users.permissions import IsOwner


# Create your views here.
class ModuleViewSet(viewsets.ModelViewSet):
    """Educational module viewset controller"""

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """Module creation function"""
        module = serializer.save()
        module.owner = self.request.user
        module.save()

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["retrieve", "create"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()