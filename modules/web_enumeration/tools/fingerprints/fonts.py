"""
Font fingerprint detector.
"""

from __future__ import annotations


def detect_fonts(html: str) -> set[str]:
    """
    Detect web font providers and icon libraries.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # Google Fonts
    #

    if "fonts.googleapis.com" in html:
        technologies.add("Google Fonts")

    if "fonts.gstatic.com" in html:
        technologies.add("Google Fonts")

    #
    # Adobe Fonts
    #

    if "use.typekit.net" in html:
        technologies.add("Adobe Fonts")

    if "typekit" in html:
        technologies.add("Adobe Fonts")

    #
    # Bunny Fonts
    #

    if "fonts.bunny.net" in html:
        technologies.add("Bunny Fonts")

    #
    # Font Awesome
    #

    if "font-awesome" in html:
        technologies.add("Font Awesome")

    if "fontawesome" in html:
        technologies.add("Font Awesome")

    if "kit.fontawesome.com" in html:
        technologies.add("Font Awesome")

    #
    # Bootstrap Icons
    #

    if "bootstrap-icons" in html:
        technologies.add("Bootstrap Icons")

    #
    # Material Icons
    #

    if "material icons" in html:
        technologies.add("Material Icons")

    if "materialicons" in html:
        technologies.add("Material Icons")

    #
    # Remix Icon
    #

    if "remixicon" in html:
        technologies.add("Remix Icon")

    #
    # Boxicons
    #

    if "boxicons" in html:
        technologies.add("Boxicons")

    #
    # Feather Icons
    #

    if "feather-icons" in html:
        technologies.add("Feather Icons")

    if "feather.min.js" in html:
        technologies.add("Feather Icons")

    #
    # Heroicons
    #

    if "heroicons" in html:
        technologies.add("Heroicons")

    #
    # Ionicons
    #

    if "ionicons" in html:
        technologies.add("Ionicons")

    #
    # Line Awesome
    #

    if "line-awesome" in html:
        technologies.add("Line Awesome")

    #
    # Themify Icons
    #

    if "themify-icons" in html:
        technologies.add("Themify Icons")

    #
    # Simple Icons
    #

    if "simple-icons" in html:
        technologies.add("Simple Icons")

    #
    # Devicon
    #

    if "devicon" in html:
        technologies.add("Devicon")

    #
    # Academicons
    #

    if "academicons" in html:
        technologies.add("Academicons")

    #
    # Fork Awesome
    #

    if "fork-awesome" in html:
        technologies.add("Fork Awesome")

    #
    # Google Material Symbols
    #

    if "materialsymbols" in html:
        technologies.add("Material Symbols")

    if "material-symbols" in html:
        technologies.add("Material Symbols")

    return technologies