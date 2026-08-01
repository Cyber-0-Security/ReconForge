"""
Technology Detector

Fingerprint technologies used by a web application.
"""

from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup


class TechnologyDetector:
    """
    Detect common web technologies.
    """

    def detect(
        self,
        soup: BeautifulSoup,
        response: requests.Response,
    ) -> list[str]:

        technologies: set[str] = set()

        html = response.text.lower()

        headers = {
            k.lower(): v.lower()
            for k, v in response.headers.items()
        }

        # -------------------------------------------------
        # Server
        # -------------------------------------------------

        server = headers.get("server", "")

        if "cloudflare" in server:
            technologies.add("Cloudflare")

        if "nginx" in server:
            technologies.add("Nginx")

        if "apache" in server:
            technologies.add("Apache")

        if "iis" in server:
            technologies.add("Microsoft IIS")

        # -------------------------------------------------
        # CMS
        # -------------------------------------------------

        if "/wp-content/" in html:
            technologies.add("WordPress")

        if "/sites/default/" in html:
            technologies.add("Drupal")

        if "joomla" in html:
            technologies.add("Joomla")

        if "shopify" in html:
            technologies.add("Shopify")

        if "wixstatic" in html:
            technologies.add("Wix")

        if "squarespace" in html:
            technologies.add("Squarespace")

        # -------------------------------------------------
        # JavaScript Libraries
        # -------------------------------------------------

        if re.search(r"jquery(\.min)?\.js", html):
            technologies.add("jQuery")

        if "react" in html or "__next" in html:
            technologies.add("React")

        if "_nuxt" in html:
            technologies.add("Nuxt.js")

        if "next.js" in html:
            technologies.add("Next.js")

        if "vue" in html:
            technologies.add("Vue.js")

        if "angular" in html:
            technologies.add("Angular")

        # -------------------------------------------------
        # CSS Frameworks
        # -------------------------------------------------

        if "bootstrap" in html:
            technologies.add("Bootstrap")

        if "tailwind" in html:
            technologies.add("Tailwind CSS")

        if "bulma" in html:
            technologies.add("Bulma")

        if "foundation" in html:
            technologies.add("Foundation")

        # -------------------------------------------------
        # Analytics
        # -------------------------------------------------

        if "google-analytics.com" in html:
            technologies.add("Google Analytics")

        if "googletagmanager.com" in html:
            technologies.add("Google Tag Manager")

        if "gtag(" in html:
            technologies.add("Google Analytics")

        if "clarity.ms" in html:
            technologies.add("Microsoft Clarity")

        if "hotjar" in html:
            technologies.add("Hotjar")

        if "facebook.net" in html:
            technologies.add("Facebook Pixel")

        # -------------------------------------------------
        # Security
        # -------------------------------------------------

        if "cf-ray" in headers:
            technologies.add("Cloudflare CDN")

        if "x-powered-by" in headers:

            powered = headers["x-powered-by"]

            if "php" in powered:
                technologies.add("PHP")

            elif ".net" in powered:
                technologies.add("ASP.NET")

            else:
                technologies.add(powered)

        # -------------------------------------------------
        # Web Server Hints
        # -------------------------------------------------

        generator = soup.find(
            "meta",
            attrs={"name": "generator"},
        )

        if generator:

            content = generator.get("content")

            if content:

                technologies.add(content.strip())

        return sorted(technologies)


technology_detector = TechnologyDetector()