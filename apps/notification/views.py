from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.notification.models import UserNotificationPreference
from apps.notification.serializers import NotificationPreferenceSerializer


class UserNotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserNotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
