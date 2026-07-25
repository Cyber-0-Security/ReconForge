"""
Header fingerprint detector.
"""

from __future__ import annotations

from requests.structures import CaseInsensitiveDict


def detect_headers(
    headers: CaseInsensitiveDict,
) -> set[str]:
    """
    Detect technologies from HTTP response headers.
    """

    technologies: set[str] = set()

    server = headers.get("Server", "").lower()
    powered_by = headers.get("X-Powered-By", "").lower()

    #
    # Web Servers
    #

    if "apache" in server:
        technologies.add("Apache")

    if "nginx" in server:
        technologies.add("Nginx")

    if "iis" in server:
        technologies.add("Microsoft IIS")

    if "openresty" in server:
        technologies.add("OpenResty")

    if "caddy" in server:
        technologies.add("Caddy")

    #
    # CDN / Proxy
    #

    if "cloudflare" in server:
        technologies.add("Cloudflare")

    if headers.get("CF-RAY"):
        technologies.add("Cloudflare")

    if headers.get("CF-Cache-Status"):
        technologies.add("Cloudflare")

    if headers.get("X-Served-By"):
        technologies.add("Fastly")

    if headers.get("X-Cache"):
        value = headers["X-Cache"].lower()

        if "akamai" in value:
            technologies.add("Akamai")

    #
    # Backend
    #

    if "php" in powered_by:
        technologies.add("PHP")

    if "express" in powered_by:
        technologies.add("Express.js")

    if "asp.net" in powered_by:
        technologies.add("ASP.NET")

    if "laravel" in powered_by:
        technologies.add("Laravel")

    return technologies