"""
Payment gateway fingerprint detector.
"""

from __future__ import annotations


def detect_payment(html: str) -> set[str]:
    """
    Detect payment gateways and checkout providers.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # Stripe
    #

    if "js.stripe.com" in html:
        technologies.add("Stripe")

    if "stripe.com" in html:
        technologies.add("Stripe")

    if "stripe.js" in html:
        technologies.add("Stripe")

    #
    # PayPal
    #

    if "paypal.com/sdk/js" in html:
        technologies.add("PayPal")

    if "paypalobjects.com" in html:
        technologies.add("PayPal")

    if "paypal checkout" in html:
        technologies.add("PayPal")

    #
    # Razorpay
    #

    if "checkout.razorpay.com" in html:
        technologies.add("Razorpay")

    if "razorpay" in html:
        technologies.add("Razorpay")

    #
    # Braintree
    #

    if "braintree" in html:
        technologies.add("Braintree")

    #
    # Square
    #

    if "squareup.com" in html:
        technologies.add("Square")

    if "square payment" in html:
        technologies.add("Square")

    #
    # Authorize.Net
    #

    if "authorize.net" in html:
        technologies.add("Authorize.Net")

    #
    # Adyen
    #

    if "adyen" in html:
        technologies.add("Adyen")

    #
    # Klarna
    #

    if "klarna" in html:
        technologies.add("Klarna")

    #
    # Afterpay
    #

    if "afterpay" in html:
        technologies.add("Afterpay")

    #
    # Zip
    #

    if "zipmoney" in html:
        technologies.add("Zip")

    if "zip.co" in html:
        technologies.add("Zip")

    #
    # Paddle
    #

    if "paddle.com" in html:
        technologies.add("Paddle")

    if "cdn.paddle.com" in html:
        technologies.add("Paddle")

    #
    # Lemon Squeezy
    #

    if "lemonsqueezy" in html:
        technologies.add("Lemon Squeezy")

    #
    # Shopify Payments
    #

    if "shopify-payments" in html:
        technologies.add("Shopify Payments")

    #
    # Apple Pay
    #

    if "apple-pay" in html:
        technologies.add("Apple Pay")

    if "applepay" in html:
        technologies.add("Apple Pay")

    #
    # Google Pay
    #

    if "google-pay" in html:
        technologies.add("Google Pay")

    if "pay.google.com" in html:
        technologies.add("Google Pay")

    #
    # Amazon Pay
    #

    if "amazon pay" in html:
        technologies.add("Amazon Pay")

    if "pay.amazon.com" in html:
        technologies.add("Amazon Pay")

    #
    # Paytm
    #

    if "paytm" in html:
        technologies.add("Paytm")

    #
    # PhonePe
    #

    if "phonepe" in html:
        technologies.add("PhonePe")

    #
    # Cashfree
    #

    if "cashfree" in html:
        technologies.add("Cashfree")

    #
    # CCAvenue
    #

    if "ccavenue" in html:
        technologies.add("CCAvenue")

    return technologies