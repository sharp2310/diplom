from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from users.permissions import IsAdminOrSelfUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelfUser]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['list', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super(UserViewSet, self).get_permissions()