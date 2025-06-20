import uuid
from django.db import models
from django.contrib.auth import get_user_model

Author = get_user_model()


class SubscriptionPlan(models.Model):
    GATEWAY_CHOICES = (
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
        ("mercadopago", "MercadoPago"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default="BRL")
    billing_interval = models.CharField(
        max_length=20, default="month"
    )  # month, year, etc.
    gateway = models.CharField(max_length=30, choices=GATEWAY_CHOICES, default="stripe")
    external_id = models.CharField(max_length=255)  # ID of product/price in gateway
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("gateway", "external_id")

    def __str__(self):
        return f"{self.name} ({self.gateway})"


class UserSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, related_name="subscriptions"
    )
    gateway = models.CharField(max_length=30, default="stripe")
    external_subscription_id = models.CharField(
        max_length=255
    )  # ex: Stripe subscription ID
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "external_subscription_id")

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
