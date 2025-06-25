from rest_framework import serializers
from apps.notification.models import UserNotificationPreference


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    notification_type = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    label = serializers.CharField(source='notification_type.name', read_only=True)
    category = serializers.CharField(source='notification_type.category', read_only=True)

    class Meta:
        model = UserNotificationPreference
        fields = ['notification_type', 'label', 'category', 'via_email', 'via_platform']
