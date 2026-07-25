"""
CSS fingerprint detector.
"""

from __future__ import annotations

import re


def detect_css(html: str) -> set[str]:
    """
    Detect technologies from linked CSS files.
    """

    technologies: set[str] = set()

    html = html.lower()

    stylesheets = re.findall(
        r'<link[^>]+href=["\']([^"\']+)["\']',
        html,
    )

    for stylesheet in stylesheets:

        #
        # CSS Frameworks
        #

        if "bootstrap" in stylesheet:
            technologies.add("Bootstrap")

        if "tailwind" in stylesheet:
            technologies.add("Tailwind CSS")

        if "bulma" in stylesheet:
            technologies.add("Bulma")

        if "foundation" in stylesheet:
            technologies.add("Foundation")

        if "semantic" in stylesheet:
            technologies.add("Semantic UI")

        if "material" in stylesheet:
            technologies.add("Material UI")

        if "uikit" in stylesheet:
            technologies.add("UIkit")

        if "purecss" in stylesheet:
            technologies.add("Pure CSS")

        if "animate" in stylesheet:
            technologies.add("Animate.css")

        if "font-awesome" in stylesheet:
            technologies.add("Font Awesome")

        if "bootstrap-icons" in stylesheet:
            technologies.add("Bootstrap Icons")

        #
        # Fonts
        #

        if "fonts.googleapis.com" in stylesheet:
            technologies.add("Google Fonts")

        if "fonts.gstatic.com" in stylesheet:
            technologies.add("Google Fonts")

        if "fontawesome" in stylesheet:
            technologies.add("Font Awesome")

        #
        # CDN
        #

        if "cdnjs.cloudflare.com" in stylesheet:
            technologies.add("cdnjs")

        if "cdn.jsdelivr.net" in stylesheet:
            technologies.add("jsDelivr")

        if "unpkg.com" in stylesheet:
            technologies.add("unpkg")

        if "cloudflare" in stylesheet:
            technologies.add("Cloudflare")

    return technologies