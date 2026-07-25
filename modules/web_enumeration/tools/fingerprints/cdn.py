"""
CDN, hosting and edge network fingerprint detector.
"""

from __future__ import annotations


def detect_cdn(
    headers: dict,
    html: str,
) -> set[str]:
    """
    Detect CDN and edge providers.
    """

    technologies: set[str] = set()

    html = html.lower()

    server = headers.get("Server", "").lower()

    powered = headers.get("X-Powered-By", "").lower()

    all_headers = " ".join(
        f"{k}:{v}".lower()
        for k, v in headers.items()
    )

    #
    # Cloudflare
    #

    if "cloudflare" in server:
        technologies.add("Cloudflare")

    if "cf-ray" in all_headers:
        technologies.add("Cloudflare")

    if "__cf_bm" in html:
        technologies.add("Cloudflare")

    #
    # AWS CloudFront
    #

    if "cloudfront" in server:
        technologies.add("Amazon CloudFront")

    if "x-amz-cf-id" in all_headers:
        technologies.add("Amazon CloudFront")

    if "cloudfront.net" in html:
        technologies.add("Amazon CloudFront")

    #
    # Fastly
    #

    if "fastly" in server:
        technologies.add("Fastly")

    if "fastly-debug" in all_headers:
        technologies.add("Fastly")

    if "fastly.net" in html:
        technologies.add("Fastly")

    #
    # Akamai
    #

    if "akamai" in server:
        technologies.add("Akamai")

    if "akamaized.net" in html:
        technologies.add("Akamai")

    if "akamaihd.net" in html:
        technologies.add("Akamai")

    #
    # BunnyCDN
    #

    if "bunnycdn" in html:
        technologies.add("BunnyCDN")

    if "b-cdn.net" in html:
        technologies.add("BunnyCDN")

    #
    # jsDelivr
    #

    if "cdn.jsdelivr.net" in html:
        technologies.add("jsDelivr")

    #
    # cdnjs
    #

    if "cdnjs.cloudflare.com" in html:
        technologies.add("cdnjs")

    #
    # unpkg
    #

    if "unpkg.com" in html:
        technologies.add("unpkg")

    #
    # KeyCDN
    #

    if "kxcdn.com" in html:
        technologies.add("KeyCDN")

    #
    # StackPath
    #

    if "stackpathcdn.com" in html:
        technologies.add("StackPath")

    #
    # Netlify
    #

    if "netlify" in server:
        technologies.add("Netlify")

    if "netlify.app" in html:
        technologies.add("Netlify")

    #
    # Vercel
    #

    if "vercel" in powered:
        technologies.add("Vercel")

    if "x-vercel-id" in all_headers:
        technologies.add("Vercel")

    if "vercel.app" in html:
        technologies.add("Vercel")

    #
    # GitHub Pages
    #

    if "github.io" in html:
        technologies.add("GitHub Pages")

    #
    # Azure CDN
    #

    if "azureedge.net" in html:
        technologies.add("Azure CDN")

    #
    # Google CDN
    #

    if "gstatic.com" in html:
        technologies.add("Google CDN")

    if "googleusercontent.com" in html:
        technologies.add("Google CDN")

    return technologies