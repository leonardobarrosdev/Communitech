from django.urls import path, include, re_path
from .views import RegisterAPIView, UpdateProfileAPIView, UpdateAuthAPIView


app_name = "profile"

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("profiles/<int:id>/update/", UpdateProfileAPIView.as_view(), name="update"),
    path(
        "profiles/<int:id>/update-auth/",
        UpdateAuthAPIView.as_view(),
        name="update-auth",
    ),
    re_path(r"auth/", include("knox.urls")),
]
