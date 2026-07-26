"""
Bot-protection / WAF challenge page detector.

Many sites (Cloudflare, Akamai, PerimeterX, DataDome, generic WAFs)
return a short interstitial "are you human" page instead of real
content when a request looks like a script rather than a browser.

A plain requests.get() can't solve these challenges (they require
running JavaScript), so if we don't detect this case explicitly,
every fingerprint check silently fails against the challenge page
and the tool just reports far fewer technologies than expected,
with no explanation of why.
"""

from __future__ import annotations


# Each marker is a (needle, protection_service_name) pair.
# Matching is done against the lowercased HTML.
CHALLENGE_MARKERS: tuple[tuple[str, str], ...] = (
    ("just a moment", "Cloudflare"),
    ("cf-browser-verification", "Cloudflare"),
    ("cf_chl_", "Cloudflare"),
    ("checking your browser before accessing", "Cloudflare"),
    ("attention required! | cloudflare", "Cloudflare"),
    ("perimeterx", "PerimeterX"),
    ("_px-captcha", "PerimeterX"),
    ("datadome", "DataDome"),
    ("akamai-bot-manager", "Akamai Bot Manager"),
    ("ak_bmsc", "Akamai Bot Manager"),
    ("sorry, you have been blocked", "Generic WAF"),
    ("access denied", "Generic WAF"),
    ("request unsuccessful. incapsula", "Imperva Incapsula"),
)


def detect_challenge_page(
    status_code: int,
    html: str,
) -> str | None:
    """
    Check whether a response looks like a bot-protection challenge
    page rather than real site content.

    Returns the name of the detected protection service, or None
    if the response looks like ordinary page content.
    """

    lowered = html.lower()

    for marker, service in CHALLENGE_MARKERS:

        if marker in lowered:
            return service

    #
    # A very short body on a non-2xx status is also suspicious,
    # even without a recognized marker string.
    #

    if status_code >= 400 and len(html) < 2000:
        return "Unknown block page"

    #
    # A suspiciously tiny body on a 200 is also worth flagging -
    # real pages (especially large e-commerce/SPA homepages) are
    # essentially never this small.
    #

    if status_code == 200 and len(html) < 1500:
        return "Unusually small response (possibly a stub/block page)"

    return None
