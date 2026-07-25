"""
Cookie fingerprint detector.
"""

from __future__ import annotations

from requests.cookies import RequestsCookieJar


def detect_cookies(
    cookies: RequestsCookieJar,
) -> set[str]:
    """
    Detect technologies from response cookies.
    """

    technologies: set[str] = set()

    for cookie in cookies:

        name = cookie.name.lower()

        #
        # PHP
        #

        if name == "phpsessid":
            technologies.add("PHP")

        #
        # Laravel
        #

        if name == "laravel_session":
            technologies.add("Laravel")
            technologies.add("PHP")

        #
        # Django
        #

        if name == "csrftoken":
            technologies.add("Django")

        if name == "sessionid":
            technologies.add("Django")

        #
        # ASP.NET
        #

        if name.startswith("asp.net"):
            technologies.add("ASP.NET")

        if name == "aspnetsessionid":
            technologies.add("ASP.NET")

        #
        # Ruby on Rails
        #

        if "_session" in name:
            technologies.add("Ruby on Rails")

        #
        # WordPress
        #

        if name.startswith("wordpress"):
            technologies.add("WordPress")

        if name.startswith("wp-"):
            technologies.add("WordPress")

        #
        # Cloudflare
        #

        if name == "__cf_bm":
            technologies.add("Cloudflare")

        if name == "__cflb":
            technologies.add("Cloudflare")

        if name == "cf_clearance":
            technologies.add("Cloudflare")

        #
        # Google
        #

        if name.startswith("__secure-"):
            technologies.add("Google Services")

        #
        # Amazon
        #

        if name.startswith("aws"):
            technologies.add("AWS")

    return technologies