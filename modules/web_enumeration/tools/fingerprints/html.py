"""
HTML fingerprint detector.
"""

from __future__ import annotations


def detect_html(html: str) -> set[str]:
    """
    Detect technologies from HTML source.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # WordPress
    #

    if "wp-content" in html:
        technologies.add("WordPress")

    if "wp-includes" in html:
        technologies.add("WordPress")

    #
    # Drupal
    #

    if "/sites/default/" in html:
        technologies.add("Drupal")

    #
    # Joomla
    #

    if "/media/system/js/" in html:
        technologies.add("Joomla")

    #
    # React
    #

    if "__next" in html:
        technologies.add("Next.js")

    if "_next/static" in html:
        technologies.add("Next.js")

    if 'id="__next"' in html:
        technologies.add("Next.js")

    if 'id="root"' in html:
        technologies.add("React")

    if "react" in html:
        technologies.add("React")

    #
    # Angular
    #

    if "ng-app" in html:
        technologies.add("Angular")

    if "ng-version" in html:
        technologies.add("Angular")

    #
    # Vue
    #

    if "__vue__" in html:
        technologies.add("Vue.js")

    if "data-v-" in html:
        technologies.add("Vue.js")

    #
    # Nuxt
    #

    if "__nuxt" in html:
        technologies.add("Nuxt.js")

    #
    # Svelte
    #

    if "__svelte" in html:
        technologies.add("Svelte")

    #
    # Gatsby
    #

    if "gatsby" in html:
        technologies.add("Gatsby")

    return technologies