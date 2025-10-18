import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency="usd"):
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100), # cents
        currency=currency,
        automatic_payment_methods={"enabled": True},
    )
    return intent