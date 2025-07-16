from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import PaymentListAPIView, UserCreateAPIView, UserListAPIView, UserProfileAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/me/", UserProfileAPIView.as_view(), name="user_profile"),
]
