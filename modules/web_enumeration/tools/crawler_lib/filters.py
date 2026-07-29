"""
Crawler Filters

Filters extracted URLs before they are added to the crawl queue.
"""

from __future__ import annotations

from urllib.parse import urlparse

from .models import (
    CrawlConfig,
    Link,
)


class CrawlFilters:
    """
    Filters discovered links.
    """

    STATIC_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".ico",
        ".webp",
        ".css",
        ".js",
        ".map",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".7z",
        ".rar",
        ".mp3",
        ".mp4",
        ".avi",
        ".mov",
        ".wmv",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
    }

    # ---------------------------------------------------------

    def is_valid(
        self,
        link: Link,
        config: CrawlConfig,
    ) -> tuple[bool, str]:
        """
        Validate a discovered URL.

        Returns:
            (True, "ok")
            (False, "<reason>")
        """

        url = link.url.strip()

        if not url:
            return False, "empty"

        if self._is_fragment(url):
            return False, "fragment"

        if self._is_mail(url):
            return False, "mailto"

        if self._is_tel(url):
            return False, "telephone"

        if self._is_javascript(url):
            return False, "javascript"

        if self._is_external(url, config):
            return False, "external"

        if self._is_static_file(url):
            return False, "static"

        return True, "ok"

    # ---------------------------------------------------------

    @staticmethod
    def _is_fragment(
        url: str,
    ) -> bool:

        return url.startswith("#")

    # ---------------------------------------------------------

    @staticmethod
    def _is_mail(
        url: str,
    ) -> bool:

        return url.startswith("mailto:")

    # ---------------------------------------------------------

    @staticmethod
    def _is_tel(
        url: str,
    ) -> bool:

        return url.startswith("tel:")

    # ---------------------------------------------------------

    @staticmethod
    def _is_javascript(
        url: str,
    ) -> bool:

        return url.startswith("javascript:")

    # ---------------------------------------------------------

    def _is_external(
        self,
        url: str,
        config: CrawlConfig,
    ) -> bool:
        """
        Return True only if the URL is outside the allowed scope.
        """

        target = urlparse(config.url)
        parsed = urlparse(url)

        # Relative URLs are always internal.
        if not parsed.netloc:
            return False

        target_host = target.netloc.lower()
        host = parsed.netloc.lower()

        # Same host
        if host == target_host:
            return False

        # Allow subdomains if enabled
        if config.include_subdomains:
            if host.endswith("." + target_host):
                return False

        return True

    # ---------------------------------------------------------

    def _is_static_file(
        self,
        url: str,
    ) -> bool:

        path = urlparse(url).path.lower()

        for extension in self.STATIC_EXTENSIONS:

            if path.endswith(extension):
                return True

        return False


filters = CrawlFilters()