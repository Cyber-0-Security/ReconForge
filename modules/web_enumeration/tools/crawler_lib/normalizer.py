"""
Crawler URL Normalizer

Normalizes URLs before they are added to the crawl queue.
"""

from __future__ import annotations

from urllib.parse import (
    parse_qsl,
    urlencode,
    urlparse,
    urlunparse,
)


class URLNormalizer:
    """
    Normalizes URLs to reduce duplicate crawling.
    """

    TRACKING_PARAMETERS = {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid",
        "msclkid",
    }

    def normalize(
        self,
        url: str,
    ) -> str:
        """
        Normalize a URL.
        """

        parsed = urlparse(url)

        scheme = parsed.scheme.lower()

        hostname = (parsed.hostname or "").lower()

        # Remove leading www.
        if hostname.startswith("www."):
            hostname = hostname[4:]

        # Remove default ports
        port = parsed.port

        if port in (80, 443, None):
            netloc = hostname
        else:
            netloc = f"{hostname}:{port}"

        # Normalize path
        path = parsed.path or "/"

        while "//" in path:
            path = path.replace("//", "/")

        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]

        # Remove fragments
        fragment = ""

        # Remove tracking parameters
        params = []

        for key, value in parse_qsl(
            parsed.query,
            keep_blank_values=True,
        ):

            if key.lower() in self.TRACKING_PARAMETERS:
                continue

            params.append((key, value))

        params.sort()

        query = urlencode(
            params,
            doseq=True,
        )

        return urlunparse(
            (
                scheme,
                netloc,
                path,
                "",
                query,
                fragment,
            )
        )


normalizer = URLNormalizer()