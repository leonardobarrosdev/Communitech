from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "description",
            "price",
            "currency",
            "billing_interval",
            "gateway",
            "external_id",
            "is_active",
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    # user = serializers.CharField(source="user.id", read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            "id",
            "user",
            "plan",
            "plan_name",
            "gateway",
            "external_subscription_id",
            "is_active",
            "start_date",
            "end_date",
        ]
