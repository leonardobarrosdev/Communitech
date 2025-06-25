from django.urls import path
from .views import UserNotificationPreferenceViewSet


app_name = "notification"

urlpatterns = [
    path("notifications/preferences/", UserNotificationPreferenceViewSet.as_view(), name="preferences"),
    path("notifications/preferences/<int:id>/", UserNotificationPreferenceViewSet.as_view(), name="preference-detail"),
]