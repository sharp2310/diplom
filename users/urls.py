from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    MyTokenObtainPairView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("profile/", UserUpdateAPIView.as_view(), name="profile"),
    path("delete/", UserDestroyAPIView.as_view(), name="delete"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:login"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]