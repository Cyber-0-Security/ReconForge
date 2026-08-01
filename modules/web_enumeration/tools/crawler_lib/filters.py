"""
Crawler Filters

Filters extracted URLs before they are added to the crawl queue.
"""

from __future__ import annotations

from urllib.parse import urlparse

from .logger import logger
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

    def is_valid(
        self,
        link: Link,
        config: CrawlConfig,
    ) -> bool:
        """
        Determine whether a link should be crawled.
        """

        url = link.url.strip()

        if not url:
            logger.debug("Skip empty URL")
            return False

        if self._is_fragment(url):
            logger.debug(f"Skip fragment: {url}")
            return False

        if self._is_mail(url):
            logger.debug(f"Skip mailto: {url}")
            return False

        if self._is_javascript(url):
            logger.debug(f"Skip javascript: {url}")
            return False

        if self._is_tel(url):
            logger.debug(f"Skip telephone: {url}")
            return False

        if self._is_external(
            url,
            config,
        ):
            logger.debug(f"Skip external: {url}")
            return False

        if self._is_static_file(url):
            logger.debug(f"Skip static file: {url}")
            return False

        return True

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
        Reject external domains unless allowed.
        """

        target_host = (
            urlparse(config.url)
            .hostname
            or ""
        ).lower()

        current_host = (
            urlparse(url)
            .hostname
            or ""
        ).lower()

        # Relative URL
        if not current_host:
            return False

        # Same host
        if current_host == target_host:
            return False

        # Allow subdomains
        if config.include_subdomains:

            if current_host.endswith(
                "." + target_host
            ):
                return False

        return True

    # ---------------------------------------------------------

    def _is_static_file(
        self,
        url: str,
    ) -> bool:

        path = urlparse(url).path.lower()

        return any(
            path.endswith(ext)
            for ext in self.STATIC_EXTENSIONS
        )


filters = CrawlFilters()