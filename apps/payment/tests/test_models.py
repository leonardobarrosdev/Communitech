import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from apps.payment.models import SubscriptionPlan, UserSubscription

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def subscription_plan():
    return SubscriptionPlan.objects.create(
        name="Basic Plan",
        description="Basic subscription plan",
        price=9.99,
        currency="USD",
        billing_interval="month",
        gateway="stripe",
        external_id="prod_123",
    )


@pytest.mark.django_db
class TestSubscriptionPlan:
    def test_create_subscription_plan(self, subscription_plan):
        assert subscription_plan.name == "Basic Plan"
        assert subscription_plan.price == 9.99
        assert subscription_plan.is_active is True

    def test_duplicate_gateway_external_id(self, subscription_plan):
        with pytest.raises(IntegrityError):
            SubscriptionPlan.objects.create(
                name="Duplicate Plan",
                price=19.99,
                gateway="stripe",
                external_id="prod_123",
            )

    def test_string_representation(self, subscription_plan):
        assert str(subscription_plan) == "Basic Plan (stripe)"


@pytest.mark.django_db
class TestUserSubscription:
    def test_create_user_subscription(self, user, subscription_plan):
        subscription = UserSubscription.objects.create(
            user=user,
            plan=subscription_plan,
            gateway="stripe",
            external_subscription_id="sub_123",
            start_date=timezone.now(),
        )
        assert subscription.is_active is True
        assert subscription.user == user
        assert subscription.plan == subscription_plan

    def test_duplicate_user_subscription(self, user, subscription_plan):
        UserSubscription.objects.create(
            user=user,
            plan=subscription_plan,
            gateway="stripe",
            external_subscription_id="sub_123",
            start_date=timezone.now(),
        )

        with pytest.raises(IntegrityError):
            UserSubscription.objects.create(
                user=user,
                plan=subscription_plan,
                gateway="stripe",
                external_subscription_id="sub_123",
                start_date=timezone.now(),
            )

    def test_string_representation(self, user, subscription_plan):
        subscription = UserSubscription.objects.create(
            user=user,
            plan=subscription_plan,
            gateway="stripe",
            external_subscription_id="sub_123",
            start_date=timezone.now(),
        )
        assert str(subscription) == "testuser - Basic Plan"
