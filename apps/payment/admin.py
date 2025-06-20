from django.contrib import admin
from apps.payment.models import SubscriptionPlan, UserSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
