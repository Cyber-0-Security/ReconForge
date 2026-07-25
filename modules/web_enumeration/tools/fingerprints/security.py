"""
Security technology fingerprint detector.
"""

from __future__ import annotations


def detect_security(
    headers: dict,
    html: str,
) -> set[str]:
    """
    Detect security products, WAFs and browser security mechanisms.
    """

    technologies: set[str] = set()

    html = html.lower()

    server = headers.get("Server", "").lower()

    powered = headers.get("X-Powered-By", "").lower()

    all_headers = {
        k.lower(): str(v).lower()
        for k, v in headers.items()
    }

    headers_text = " ".join(
        f"{k}:{v}"
        for k, v in all_headers.items()
    )

    #
    # Cloudflare
    #

    if "cloudflare" in server:
        technologies.add("Cloudflare")

    if "cf-ray" in all_headers:
        technologies.add("Cloudflare")

    if "cf-cache-status" in all_headers:
        technologies.add("Cloudflare")

    if "__cf_bm" in html:
        technologies.add("Cloudflare Bot Management")

    #
    # Akamai
    #

    if "akamai" in server:
        technologies.add("Akamai")

    if "akamaighost" in server:
        technologies.add("Akamai")

    #
    # Imperva
    #

    if "incapsula" in headers_text:
        technologies.add("Imperva")

    if "x-iinfo" in all_headers:
        technologies.add("Imperva")

    if "visid_incap" in html:
        technologies.add("Imperva")

    #
    # Sucuri
    #

    if "x-sucuri-id" in all_headers:
        technologies.add("Sucuri")

    if "x-sucuri-cache" in all_headers:
        technologies.add("Sucuri")

    #
    # AWS WAF
    #

    if "awselb" in server:
        technologies.add("AWS")

    if "x-amzn-requestid" in all_headers:
        technologies.add("AWS")

    if "x-amz-cf-id" in all_headers:
        technologies.add("Amazon CloudFront")

    #
    # F5 BIG-IP
    #

    if "bigip" in html:
        technologies.add("F5 BIG-IP")

    if "x-waf-event-info" in all_headers:
        technologies.add("F5 BIG-IP ASM")

    #
    # Barracuda
    #

    if "barra" in headers_text:
        technologies.add("Barracuda WAF")

    #
    # Fortinet
    #

    if "fortigate" in headers_text:
        technologies.add("Fortinet")

    #
    # Citrix
    #

    if "citrix" in headers_text:
        technologies.add("Citrix ADC")

    #
    # ModSecurity
    #

    if "mod_security" in headers_text:
        technologies.add("ModSecurity")

    if "modsecurity" in headers_text:
        technologies.add("ModSecurity")

    #
    # reCAPTCHA
    #

    if "www.google.com/recaptcha" in html:
        technologies.add("Google reCAPTCHA")

    if "grecaptcha" in html:
        technologies.add("Google reCAPTCHA")

    #
    # hCaptcha
    #

    if "hcaptcha.com" in html:
        technologies.add("hCaptcha")

    if "h-captcha" in html:
        technologies.add("hCaptcha")

    #
    # Turnstile
    #

    if "challenges.cloudflare.com" in html:
        technologies.add("Cloudflare Turnstile")

    #
    # Content Security Policy
    #

    if "content-security-policy" in all_headers:
        technologies.add("Content Security Policy")

    #
    # HSTS
    #

    if "strict-transport-security" in all_headers:
        technologies.add("HSTS")

    #
    # X-Frame-Options
    #

    if "x-frame-options" in all_headers:
        technologies.add("X-Frame-Options")

    #
    # XSS Protection
    #

    if "x-xss-protection" in all_headers:
        technologies.add("XSS Protection")

    #
    # X-Content-Type-Options
    #

    if "x-content-type-options" in all_headers:
        technologies.add("X-Content-Type-Options")

    #
    # Referrer Policy
    #

    if "referrer-policy" in all_headers:
        technologies.add("Referrer Policy")

    #
    # Permissions Policy
    #

    if "permissions-policy" in all_headers:
        technologies.add("Permissions Policy")

    #
    # Expect-CT
    #

    if "expect-ct" in all_headers:
        technologies.add("Expect-CT")

    #
    # Cross-Origin Policies
    #

    if "cross-origin-opener-policy" in all_headers:
        technologies.add("COOP")

    if "cross-origin-resource-policy" in all_headers:
        technologies.add("CORP")

    if "cross-origin-embedder-policy" in all_headers:
        technologies.add("COEP")

    return technologies