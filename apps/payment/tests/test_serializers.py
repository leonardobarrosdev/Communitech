import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from apps.payment.models import SubscriptionPlan, UserSubscription
from apps.payment.serializers import (
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
)

User = get_user_model()


@pytest.fixture
def subscription_plan():
    return SubscriptionPlan.objects.create(
        name="Test Plan",
        description="Test Description",
        price=99.99,
        currency="USD",
        billing_interval="monthly",
        gateway="stripe",
        external_id="price_123",
        is_active=True,
    )


@pytest.fixture
def user():
    return User.objects.create_user(email="test@example.com", password="testpass")


@pytest.fixture
def user_subscription(user, subscription_plan):
    return UserSubscription.objects.create(
        user=user,
        plan=subscription_plan,
        gateway="stripe",
        external_subscription_id="sub_123",
        is_active=True,
        start_date=datetime.now(),
        end_date=datetime.now(),
    )


@pytest.mark.django_db
def test_subscription_plan_serializer(subscription_plan):
    serializer = SubscriptionPlanSerializer(subscription_plan)
    assert serializer.data["name"] == "Test Plan"
    assert serializer.data["price"] == "99.99"
    assert serializer.data["currency"] == "USD"
    assert serializer.data["billing_interval"] == "monthly"
    assert serializer.data["is_active"] is True


@pytest.mark.django_db
def test_user_subscription_serializer(user_subscription):
    serializer = UserSubscriptionSerializer(user_subscription)
    assert serializer.data["plan_name"] == "Test Plan"
    assert serializer.data["gateway"] == "stripe"
    assert serializer.data["external_subscription_id"] == "sub_123"
    assert serializer.data["is_active"] is True
