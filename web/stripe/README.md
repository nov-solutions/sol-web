# Stripe Module

This module provides a complete Stripe integration, including customer management, subscriptions, payments, and webhook handling.

## Features

- **Customer Management**: Automatically create and manage Stripe customers linked to Django users
- **Product & Pricing**: Sync products and prices from Stripe
- **Subscriptions**: Handle subscription lifecycle (create, update, cancel)
- **Payments**: Process one-time payments and manage payment methods
- **Webhooks**: Robust webhook handling for all major Stripe events
- **Admin Interface**: Full Django admin integration for managing Stripe data
- **Customer Portal**: Integration with Stripe's hosted customer portal

## Setup

### 1. Environment Variables

Add these to your `.env` file:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_LIVE_MODE=False
```

### 2. Install Dependencies

```bash
pip install stripe
```

### 3. Add to INSTALLED_APPS

The module should already be added if you're using the template structure:

```python
INSTALLED_APPS = [
    ...
    'stripe.apps.StripeConfig',
]
```

### 4. Include URLs

In your main `urls.py`:

```python
urlpatterns = [
    ...
    path('api/stripe/', include('stripe.urls')),
]
```

### 5. Run Migrations

```bash
python manage.py makemigrations stripe
python manage.py migrate
```

### 6. Sync Stripe Data

```bash
python manage.py sync_stripe_data
```

## Usage

### Creating a Checkout Session

```python
from django.views import View
from stripe.utils import get_or_create_stripe_customer

class CreateCheckoutView(View):
    def post(self, request):
        customer = get_or_create_stripe_customer(request.user)
        # Create checkout session...
```

### Handling Subscriptions

```python
from stripe.models import StripeSubscription

# Get active subscriptions for a user
subscriptions = StripeSubscription.objects.filter(
    customer__user=user,
    status__in=['active', 'trialing']
)

# Check if user has specific product
has_pro = subscriptions.filter(
    price__product__metadata__contains={'tier': 'pro'}
).exists()
```

### Webhook Setup

For development, use Stripe CLI:

```bash
stripe listen --forward-to localhost:8000/api/stripe/webhook/
```

For production, configure the webhook endpoint in Stripe Dashboard:

- Endpoint URL: `https://yourdomain.com/api/stripe/webhook/`
- Events to listen for: Select all events or choose specific ones

## Models

- **StripeCustomer**: Links Django users to Stripe customers
- **StripeProduct**: Mirrors Stripe products
- **StripePrice**: Mirrors Stripe prices (one-time or recurring)
- **StripeSubscription**: Tracks subscription status and details
- **StripePaymentMethod**: Stores customer payment methods
- **StripePayment**: Records payment intents
- **StripeWebhookEvent**: Logs all webhook events for debugging

## Management Commands

- `sync_stripe_data`: Sync products and prices from Stripe
  ```bash
  python manage.py sync_stripe_data
  python manage.py sync_stripe_data --products-only
  python manage.py sync_stripe_data --dry-run
  ```

## Customization

### Auto-create Customers

By default, a Stripe customer is created when a Django user is created. Disable this:

```python
STRIPE_AUTO_CREATE_CUSTOMER = False
```

### Extend Webhook Handlers

Add custom logic to `webhook_handlers.py`:

```python
def handle_invoice_payment_succeeded(event):
    # Default handling...

    # Add your custom logic
    invoice = event['data']['object']
    send_receipt_email(invoice)
```

### Custom Metadata

Use metadata fields on models to store additional information:

```python
subscription.metadata = {
    'plan_features': ['feature1', 'feature2'],
    'discount_code': 'SAVE20'
}
subscription.save()
```

## Testing

Run the test suite:

```bash
python manage.py test stripe
```

For webhook testing:

```bash
stripe trigger payment_intent.succeeded
```

## Security Notes

- Never expose `STRIPE_SECRET_KEY` in frontend code
- Always verify webhook signatures
- Use HTTPS in production
- Implement proper access controls on views
- Store sensitive data only in Stripe, not locally

## Removing the Module

If you don't need Stripe functionality:

1. Remove from INSTALLED_APPS
2. Delete the `stripe` directory
3. Remove from `settings/__init__.py`
4. Remove `settings/components/stripe.py`
5. Remove Stripe URLs from your main `urls.py`
