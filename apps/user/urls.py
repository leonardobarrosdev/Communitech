from django.urls import path, include, re_path
from .views import RegisterAPIView


app_name = "user"

urlpatterns = [
    path("api/auth/register/", RegisterAPIView.as_view(), name="register"),
    re_path(r"api/auth/", include("knox.urls")),
]
