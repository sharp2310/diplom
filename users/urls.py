from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import UserRegisterView, UserListView, UserLoginView, UserProfileView, UserProfileUpdateView, \
    UserDeleteView, UserPasswordResetConfirmView, UserPasswordResetView, confirm_registration, UserRegisterAPIView

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('api/register/', UserRegisterAPIView.as_view(), name='api_register'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'), # сброс пароля пользователя
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'), # подтверждение сброса пароля пользователя
    path('confirm/<str:token>/', confirm_registration, name='confirmation_link'), # путь ссылки на подтверждение регистрации, которая отправляется пользователю по email
    path('confirm-registration/<uuid:token>/', confirm_registration, name='confirm_registration'), # путь запроса, когда пользователь переходит по ссылке для подтверждения регистрации

# token
    path(
        "users/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "users/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),

]