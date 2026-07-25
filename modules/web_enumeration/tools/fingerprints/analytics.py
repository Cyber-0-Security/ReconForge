"""
Analytics fingerprint detector.
"""

from __future__ import annotations


def detect_analytics(html: str) -> set[str]:
    """
    Detect analytics and tracking technologies.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # Google Analytics
    #

    if "google-analytics.com" in html:
        technologies.add("Google Analytics")

    if "analytics.js" in html:
        technologies.add("Google Analytics")

    if "gtag(" in html:
        technologies.add("Google Analytics")

    if "gtag/js" in html:
        technologies.add("Google Analytics")

    if "ga(" in html:
        technologies.add("Google Analytics")

    #
    # Google Tag Manager
    #

    if "googletagmanager.com" in html:
        technologies.add("Google Tag Manager")

    if "gtm-" in html:
        technologies.add("Google Tag Manager")

    #
    # Google Ads
    #

    if "googlesyndication.com" in html:
        technologies.add("Google Ads")

    if "doubleclick.net" in html:
        technologies.add("Google Ads")

    if "adsbygoogle" in html:
        technologies.add("Google AdSense")

    #
    # Facebook
    #

    if "connect.facebook.net" in html:
        technologies.add("Facebook SDK")

    if "fbq(" in html:
        technologies.add("Facebook Pixel")

    if "facebook pixel" in html:
        technologies.add("Facebook Pixel")

    #
    # Microsoft Clarity
    #

    if "clarity.ms" in html:
        technologies.add("Microsoft Clarity")

    #
    # Hotjar
    #

    if "hotjar.com" in html:
        technologies.add("Hotjar")

    if "hj(" in html:
        technologies.add("Hotjar")

    #
    # Mixpanel
    #

    if "mixpanel" in html:
        technologies.add("Mixpanel")

    #
    # Segment
    #

    if "segment.com" in html:
        technologies.add("Segment")

    if "cdn.segment.com" in html:
        technologies.add("Segment")

    #
    # Matomo
    #

    if "matomo" in html:
        technologies.add("Matomo")

    if "piwik" in html:
        technologies.add("Matomo")

    #
    # Heap
    #

    if "heapanalytics" in html:
        technologies.add("Heap Analytics")

    #
    # Amplitude
    #

    if "amplitude" in html:
        technologies.add("Amplitude")

    #
    # New Relic
    #

    if "newrelic" in html:
        technologies.add("New Relic")

    #
    # Sentry
    #

    if "sentry.io" in html:
        technologies.add("Sentry")

    #
    # Datadog
    #

    if "datadoghq" in html:
        technologies.add("Datadog")

    #
    # FullStory
    #

    if "fullstory" in html:
        technologies.add("FullStory")

    return technologies