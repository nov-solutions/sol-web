import logging

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import StripeCustomer, StripePaymentMethod, StripePrice
from .utils import get_or_create_stripe_customer
from .webhook_handlers import webhook_handler

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            price_id = request.POST.get("price_id")
            if not price_id:
                return JsonResponse({"error": "Price ID is required"}, status=400)

            price = StripePrice.objects.get(stripe_price_id=price_id, active=True)
            customer = get_or_create_stripe_customer(request.user)

            checkout_session = stripe.checkout.Session.create(
                customer=customer.stripe_customer_id,
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price.stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription" if price.recurring_interval else "payment",
                success_url=request.build_absolute_uri(
                    reverse("stripe:checkout-success")
                    + "?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=request.build_absolute_uri(
                    reverse("stripe:checkout-cancel")
                ),
                metadata={
                    "user_id": str(request.user.id),
                    "price_id": price_id,
                },
            )

            return JsonResponse({"checkout_url": checkout_session.url})

        except StripePrice.DoesNotExist:
            return JsonResponse({"error": "Invalid price"}, status=400)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Checkout session error: {str(e)}")
            return JsonResponse({"error": "An error occurred"}, status=500)


class CreatePortalSessionView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            customer = StripeCustomer.objects.get(user=request.user)

            session = stripe.billing_portal.Session.create(
                customer=customer.stripe_customer_id,
                return_url=request.build_absolute_uri(
                    reverse("stripe:billing-portal-return")
                ),
            )

            return JsonResponse({"url": session.url})

        except StripeCustomer.DoesNotExist:
            return JsonResponse({"error": "No billing information found"}, status=404)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Portal session error: {str(e)}")
            return JsonResponse({"error": "An error occurred"}, status=500)


@login_required
def checkout_success(request):
    session_id = request.GET.get("session_id")
    if session_id:
        try:
            stripe.checkout.Session.retrieve(session_id)
            # You can add custom success logic here
            logger.info(f"Checkout successful for session: {session_id}")
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving checkout session: {str(e)}")

    # Redirect to a success page or dashboard
    return redirect("/")


@login_required
def checkout_cancel(request):
    # Handle checkout cancellation
    return redirect("/")


@login_required
def billing_portal_return(request):
    # Handle return from billing portal
    return redirect("/")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid webhook payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid webhook signature")
        return HttpResponse(status=400)

    # Handle the event
    try:
        webhook_handler(event)
        return HttpResponse(status=200)
    except Exception as e:
        logger.error(f"Webhook handler error: {str(e)}")
        return HttpResponse(status=500)


class ListPaymentMethodsView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            customer = StripeCustomer.objects.get(user=request.user)
            payment_methods = customer.payment_methods.all().values(
                "id",
                "stripe_payment_method_id",
                "type",
                "brand",
                "last4",
                "exp_month",
                "exp_year",
                "is_default",
            )

            return JsonResponse({"payment_methods": list(payment_methods)})

        except StripeCustomer.DoesNotExist:
            return JsonResponse({"payment_methods": []})


class SetDefaultPaymentMethodView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            payment_method_id = request.POST.get("payment_method_id")
            if not payment_method_id:
                return JsonResponse(
                    {"error": "Payment method ID is required"}, status=400
                )

            customer = StripeCustomer.objects.get(user=request.user)
            payment_method = StripePaymentMethod.objects.get(
                id=payment_method_id, customer=customer
            )

            # Update Stripe
            stripe.Customer.modify(
                customer.stripe_customer_id,
                invoice_settings={
                    "default_payment_method": payment_method.stripe_payment_method_id
                },
            )

            # Update local records
            customer.payment_methods.update(is_default=False)
            payment_method.is_default = True
            payment_method.save()

            return JsonResponse({"success": True})

        except (StripeCustomer.DoesNotExist, StripePaymentMethod.DoesNotExist):
            return JsonResponse({"error": "Invalid payment method"}, status=400)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Set default payment method error: {str(e)}")
            return JsonResponse({"error": "An error occurred"}, status=500)
