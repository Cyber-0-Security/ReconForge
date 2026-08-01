"""
Technology Detection

Identifies technologies used by a web page.
"""

from __future__ import annotations

from bs4 import BeautifulSoup


class TechnologyDetector:
    """
    Detect common web technologies.
    """

    def detect(
        self,
        soup: BeautifulSoup,
        headers: dict[str, str],
    ) -> dict[str, str]:

        tech: dict[str, str] = {}

        # -------------------------------------------------
        # Server
        # -------------------------------------------------

        if headers.get("Server"):

            tech["Server"] = headers["Server"]

        # -------------------------------------------------
        # Powered By
        # -------------------------------------------------

        if headers.get("X-Powered-By"):

            tech["Powered By"] = headers[
                "X-Powered-By"
            ]

        # -------------------------------------------------
        # Generator
        # -------------------------------------------------

        generator = soup.find(
            "meta",
            attrs={"name": "generator"},
        )

        if generator:

            value = generator.get("content")

            if value:

                tech["Generator"] = value

        # -------------------------------------------------
        # React
        # -------------------------------------------------

        html = str(soup)

        if "__NEXT_DATA__" in html:

            tech["Next.js"] = "Yes"

        if "_next/static" in html:

            tech["Next.js"] = "Yes"

        if "react" in html.lower():

            tech["React"] = "Possible"

        # -------------------------------------------------
        # Angular
        # -------------------------------------------------

        if "ng-app" in html:

            tech["Angular"] = "Yes"

        # -------------------------------------------------
        # Vue
        # -------------------------------------------------

        if "__vue__" in html.lower():

            tech["Vue"] = "Yes"

        if "vue.js" in html.lower():

            tech["Vue"] = "Yes"

        # -------------------------------------------------
        # Bootstrap
        # -------------------------------------------------

        if "bootstrap" in html.lower():

            tech["Bootstrap"] = "Yes"

        # -------------------------------------------------
        # jQuery
        # -------------------------------------------------

        if "jquery" in html.lower():

            tech["jQuery"] = "Yes"

        # -------------------------------------------------
        # WordPress
        # -------------------------------------------------

        if "/wp-content/" in html:

            tech["CMS"] = "WordPress"

        if "/wp-includes/" in html:

            tech["CMS"] = "WordPress"

        # -------------------------------------------------
        # Drupal
        # -------------------------------------------------

        if "Drupal.settings" in html:

            tech["CMS"] = "Drupal"

        # -------------------------------------------------
        # Joomla
        # -------------------------------------------------

        if "com_content" in html:

            tech["CMS"] = "Joomla"

        # -------------------------------------------------
        # Cloudflare
        # -------------------------------------------------

        if headers.get("CF-Cache-Status"):

            tech["CDN"] = "Cloudflare"

        if headers.get("CF-Ray"):

            tech["WAF"] = "Cloudflare"

        return tech


technology_detector = TechnologyDetector()