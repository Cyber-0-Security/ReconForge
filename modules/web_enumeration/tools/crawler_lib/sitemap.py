"""
Sitemap Parser

Downloads and parses XML sitemaps.
"""

from __future__ import annotations

import gzip
from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class SitemapParser:
    """
    Handles sitemap discovery.
    """

    MAX_SUB_SITEMAPS = 10

    MAX_SITEMAP_DEPTH = 3

    def __init__(self) -> None:
        """
        Reuse HTTP connections.
        """

        self._session = requests.Session()

    # ---------------------------------------------------------

    def fetch(
        self,
        url: str,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> str | None:
        """
        Download sitemap.xml.
        """

        sitemap_url = urljoin(
            url,
            "/sitemap.xml",
        )

        return self.fetch_url(
            sitemap_url,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )

    # ---------------------------------------------------------

    def parse(
        self,
        xml: str,
        timeout: int = 10,
        verify_ssl: bool = True,
        _depth: int = 0,
    ) -> list[str]:
        """
        Parse a sitemap or sitemap index.
        """

        soup = BeautifulSoup(
            xml,
            "xml",
        )

        #
        # Sitemap index
        #

        if soup.find("sitemapindex"):

            urls: set[str] = set()

            if _depth >= self.MAX_SITEMAP_DEPTH:

                return []

            sub_sitemaps = soup.find_all("sitemap")

            for sitemap_tag in sub_sitemaps[: self.MAX_SUB_SITEMAPS]:

                loc = sitemap_tag.find("loc")

                if loc is None:

                    continue

                sub_url = loc.get_text(strip=True)

                if not sub_url:

                    continue

                content = self.fetch_url(
                    sub_url,
                    timeout=timeout,
                    verify_ssl=verify_ssl,
                )

                if not content:

                    continue

                urls.update(

                    self.parse(
                        content,
                        timeout=timeout,
                        verify_ssl=verify_ssl,
                        _depth=_depth + 1,
                    )

                )

            return sorted(urls)

        #
        # Standard sitemap
        #

        urls = set()

        for tag in soup.find_all("url"):

            loc = tag.find("loc")

            if loc is None:

                continue

            value = loc.get_text(strip=True)

            if value:

                urls.add(value)

        return sorted(urls)

    # ---------------------------------------------------------

    def fetch_url(
        self,
        url: str,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> str | None:
        """
        Download an arbitrary sitemap.
        """

        try:

            response = self._session.get(

                url,

                timeout=timeout,

                verify=verify_ssl,

                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(ReconForge)"
                    ),
                    "Accept-Encoding": "gzip, deflate",
                },

            )

            if response.status_code != 200:

                return None

            #
            # Handle compressed sitemap.xml.gz
            #

            if url.lower().endswith(".gz"):

                try:

                    return gzip.GzipFile(

                        fileobj=BytesIO(
                            response.content
                        )

                    ).read().decode(
                        "utf-8",
                        errors="ignore",
                    )

                except OSError:

                    return None

            return response.text

        except requests.RequestException:

            return None


sitemap = SitemapParser()