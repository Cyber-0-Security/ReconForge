"""
JavaScript fingerprint detector.
"""

from __future__ import annotations

import re


def detect_javascript(html: str) -> set[str]:
    """
    Detect technologies from JavaScript files.
    """

    technologies: set[str] = set()

    html = html.lower()

    scripts = re.findall(
        r'<script[^>]+src=["\']([^"\']+)["\']',
        html,
    )

    for script in scripts:

        #
        # JavaScript Libraries
        #

        if "jquery" in script:
            technologies.add("jQuery")

        if "bootstrap" in script:
            technologies.add("Bootstrap")

        if "react" in script:
            technologies.add("React")

        if "react-dom" in script:
            technologies.add("React")

        if "vue" in script:
            technologies.add("Vue.js")

        if "angular" in script:
            technologies.add("Angular")

        if "ember" in script:
            technologies.add("Ember.js")

        if "backbone" in script:
            technologies.add("Backbone.js")

        if "preact" in script:
            technologies.add("Preact")

        if "svelte" in script:
            technologies.add("Svelte")

        if "next" in script or "_next/" in script:
            technologies.add("Next.js")

        if "_nuxt" in script:
            technologies.add("Nuxt.js")

        #
        # Analytics
        #

        if "google-analytics" in script:
            technologies.add("Google Analytics")

        if "gtag" in script:
            technologies.add("Google Analytics")

        if "googletagmanager" in script:
            technologies.add("Google Tag Manager")

        if "analytics.js" in script:
            technologies.add("Google Analytics")

        if "hotjar" in script:
            technologies.add("Hotjar")

        if "clarity" in script:
            technologies.add("Microsoft Clarity")

        if "segment" in script:
            technologies.add("Segment")

        if "mixpanel" in script:
            technologies.add("Mixpanel")

        #
        # Ads
        #

        if "doubleclick" in script:
            technologies.add("Google Ads")

        if "adsbygoogle" in script:
            technologies.add("Google AdSense")

        #
        # CDN
        #

        if "cloudflare" in script:
            technologies.add("Cloudflare")

        if "cdnjs" in script:
            technologies.add("cdnjs")

        if "jsdelivr" in script:
            technologies.add("jsDelivr")

        if "unpkg" in script:
            technologies.add("unpkg")

    return technologies