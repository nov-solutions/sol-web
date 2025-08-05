import os

# Stripe API Keys
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
APPLICATION_FEE_PERCENT = 4  # base fee is 2.9% + $0.30

# Stripe Configuration
STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE", "False").lower() == "true"


# Subscription settings
STRIPE_TRIAL_PERIOD_DAYS = int(os.environ.get("STRIPE_TRIAL_PERIOD_DAYS", "30"))

# Payment settings
STRIPE_PAYMENT_METHOD_TYPES = [
    "card",
    "us_bank_account",
]  # Can be extended with other payment methods
STRIPE_AUTOMATIC_TAX = os.environ.get("STRIPE_AUTOMATIC_TAX", "False").lower() == "true"

# Customer portal configuration
STRIPE_CUSTOMER_PORTAL_ENABLED = (
    os.environ.get("STRIPE_CUSTOMER_PORTAL_ENABLED", "True").lower() == "true"
)

# Stripe CLI webhook forwarding (for development)
STRIPE_CLI_WEBHOOK_PORT = os.environ.get("STRIPE_CLI_WEBHOOK_PORT", "8000")
