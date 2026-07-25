"""
Meta tag fingerprint detector.
"""

from __future__ import annotations

import re


def detect_meta(html: str) -> set[str]:
    """
    Detect technologies from HTML meta tags.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # Meta Generator
    #

    generators = re.findall(
        r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']+)["\']',
        html,
    )

    for generator in generators:

        if "wordpress" in generator:
            technologies.add("WordPress")

        elif "drupal" in generator:
            technologies.add("Drupal")

        elif "joomla" in generator:
            technologies.add("Joomla")

        elif "wix" in generator:
            technologies.add("Wix")

        elif "shopify" in generator:
            technologies.add("Shopify")

        elif "ghost" in generator:
            technologies.add("Ghost CMS")

        elif "squarespace" in generator:
            technologies.add("Squarespace")

    #
    # React
    #

    if '<meta name="react' in html:
        technologies.add("React")

    #
    # Next.js
    #

    if '<meta name="next-head-count"' in html:
        technologies.add("Next.js")

    #
    # Gatsby
    #

    if "gatsby" in html:
        technologies.add("Gatsby")

    #
    # Nuxt
    #

    if "__nuxt" in html:
        technologies.add("Nuxt.js")

    return technologies