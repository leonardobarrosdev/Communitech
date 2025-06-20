from django.urls import path
from apps.payment.views import (
    SubscriptionPlanListAPIView,
    CreateCheckoutSessionView,
    create_checkout_session,
    create_portal_session,
    stripe_webhook,
)

urlpatterns = [
    path("plans/", SubscriptionPlanListAPIView.as_view(), name="subscription-plans"),
    path("checkout/", CreateCheckoutSessionView.as_view(), name="create-checkout"),
    path(
        "create-checkout-session/",
        create_checkout_session,
        name="create-checkout-session",
    ),
    path("create-portal-session/", create_portal_session, name="create-portal-session"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
