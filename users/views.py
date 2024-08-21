from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """User creation controller"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """User login controller"""

    serializer_class = MyTokenObtainPairSerializer


class UserUpdateAPIView(UpdateAPIView):
    """User update controller"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    """User list controller"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    """User retrieve controller"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    """User delete controller"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]