import pytest
import json
from unittest.mock import patch, Mock
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from apps.payment.models import SubscriptionPlan, UserSubscription

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="test@test.com", password="testpass123"
    )


@pytest.fixture
def plan():
    return SubscriptionPlan.objects.create(
        name="Test Plan",
        price=99.99,
        external_id="price_123",
        gateway="stripe",
        is_active=True,
    )


@pytest.mark.django_db
class TestCreatePortalSession:
    def test_portal_session_success(self, api_client, user):
        url = reverse("create-portal-session")
        session_id = "sess_123"

        with patch("stripe.checkout.Session.retrieve") as mock_retrieve:
            mock_retrieve.return_value = Mock(customer=str(user.id))
            with patch("stripe.billing_portal.Session.create") as mock_create:
                mock_create.return_value = Mock(url="https://stripe.com/portal")

                response = api_client.post(url, {"session_id": session_id})

                assert response.status_code == 200
                assert response.json() == {"url": "https://stripe.com/portal"}

                mock_retrieve.assert_called_once_with(session_id)
                mock_create.assert_called_once_with(
                    customer=str(user.id),
                    return_url=f"http://{settings.ALLOWED_HOSTS[0]}:4242",
                )

    def test_portal_session_missing_session_id(self, api_client):
        url = reverse("create-portal-session")
        response = api_client.post(url, {})
        assert response.status_code == 400


@pytest.mark.django_db
class TestCreateCheckoutSession:
    def test_checkout_session_success(self, api_client):
        url = reverse("create-checkout-session")
        lookup_key = "test_key"

        with patch("stripe.Price.list") as mock_list:
            mock_list.return_value = Mock(data=[Mock(id="price_123")])
            with patch("stripe.checkout.Session.create") as mock_create:
                mock_create.return_value = Mock(url="https://stripe.com/checkout")
                response = api_client.post(
                    url, {"lookup_key": lookup_key, "session_id": "sess_123"}
                )
                assert response.status_code == 200
                assert response.json() == {"url": "https://stripe.com/checkout"}

    def test_checkout_session_missing_lookup_key(self, api_client):
        url = reverse("create-checkout-session")
        response = api_client.post(url, {})
        assert response.status_code == 500


@pytest.mark.django_db
class TestStripeWebhook:
    def test_webhook_invalid_payload(self, api_client):
        url = reverse("stripe-webhook")
        response = api_client.post(
            url, data="invalid json", content_type="application/json"
        )
        assert response.status_code == 400

    def test_webhook_user_not_found(self, api_client, plan):
        url = reverse("stripe-webhook")
        event_data = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {"user_id": "99999", "plan_id": str(plan.id)},
                    "subscription": "sub_123",
                }
            },
        }
        with patch("stripe.Webhook.construct_event") as mock_construct:
            mock_construct.return_value = event_data
            response = api_client.post(
                url,
                data=json.dumps(event_data),
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="dummy",
            )
            assert response.status_code == 400

    def test_webhook_non_checkout_event(self, api_client):
        url = reverse("stripe-webhook")
        event_data = {"type": "other.event", "data": {"object": {}}}

        with patch("stripe.Webhook.construct_event") as mock_construct:
            mock_construct.return_value = event_data

            response = api_client.post(
                url,
                data=json.dumps(event_data),
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="dummy",
            )

            assert response.status_code == 200
            assert not UserSubscription.objects.exists()
