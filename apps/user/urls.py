from django.urls import path, include, re_path
from knox.views import LogoutView
from .views import (
    RegisterAPIView,
    LoginView,
    UpdateProfileAPIView,
    UpdateAuthAPIView
)


app_name = "profile"

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("profiles/<int:id>/update/", UpdateProfileAPIView.as_view(), name="update"),
    path(
        "profiles/<int:id>/update-auth/",
        UpdateAuthAPIView.as_view(),
        name="update-auth",
    ),
    re_path(r"auth/", include("knox.urls")),
]
