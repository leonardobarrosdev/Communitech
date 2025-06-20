import stripe
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.payment.models import SubscriptionPlan, UserSubscription
from apps.payment.serializers import SubscriptionPlanSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN_NAME = f"http://{settings.ALLOWED_HOSTS[0]}:4242"


class SubscriptionPlanListAPIView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        plan_id = request.data.get("plan_id")
        plan = SubscriptionPlan.objects.get(id=plan_id)
        if plan.gateway != "stripe":
            return Response({"error": _("Plan is not Stripe.")}, status=400)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": plan.external_id,
                    "quantity": 1,
                }
            ],
            customer_email=request.user.email,
            success_url=settings.FRONTEND_SUCCESS_URL,
            cancel_url=settings.FRONTEND_CANCEL_URL,
            metadata={"user_id": str(request.user.id), "plan_id": str(plan.id)},
        )
        return Response({"session_url": checkout_session.url})


@api_view(["POST"])
def create_checkout_session(request):
    try:
        session_id = request.data.get("session_id")
        lookup_key = request.data.get("lookup_key")
        prices = stripe.Price.list(lookup_keys=[lookup_key], expand=["data.product"])
        checkout_session = stripe.checkout.Session.create(
            line_items=[{"price": prices.data[0].id, "quantity": 1}],
            mode="subscription",
            success_url=DOMAIN_NAME + f"?success=true&session_id={session_id}",
            cancel_url=DOMAIN_NAME + "?canceled=true",
        )
        return JsonResponse({"url": checkout_session.url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def create_portal_session(request):
    session_id = request.data.get("session_id")
    if not session_id:
        return JsonResponse({"error": "Session ID is required"}, status=400)
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=DOMAIN_NAME,
    )
    return JsonResponse({"url": portal_session.url})


@csrf_exempt
def stripe_webhook(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=webhook_secret
        )
    except Exception as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]
        plan_id = session["metadata"]["plan_id"]
        subscription_id = session["subscription"]

        try:
            User = get_user_model()
            user = User.objects.get(id=user_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except User.DoesNotExist:
            return JsonResponse(
                {
                    "error": "User not found",
                },
                status=400,
            )
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({"error": "Subscription plan not found"}, status=400)

        UserSubscription.objects.create(
            user=user,
            plan=plan,
            external_subscription_id=subscription_id,
            gateway="stripe",
            start_date=now(),
            is_active=True,
        )
    return JsonResponse({"status": "success"})
