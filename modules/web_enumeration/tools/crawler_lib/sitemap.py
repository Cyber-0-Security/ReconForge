"""
Sitemap Parser

Downloads and parses XML sitemaps.
"""

from __future__ import annotations

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class SitemapParser:
    """
    Handles sitemap discovery.
    """

    MAX_SUB_SITEMAPS = 5

    MAX_SITEMAP_DEPTH = 2

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

        try:

            response = requests.get(

                sitemap_url,

                timeout=timeout,

                verify=verify_ssl,

                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(ReconForge)"
                    )
                },

            )

            if response.status_code != 200:

                return None

            return response.text

        except requests.RequestException:

            return None

    # ---------------------------------------------------------

    def parse(
        self,
        xml: str,
        timeout: int = 10,
        verify_ssl: bool = True,
        _depth: int = 0,
    ) -> list[str]:
        """
        Extract every real page URL from a sitemap.

        Supports both a plain sitemap (<urlset> containing <url><loc>
        entries) and a sitemap index (<sitemapindex> containing
        <sitemap><loc> entries pointing at other sitemap files). For
        an index, each sub-sitemap is fetched and parsed in turn so
        callers always get back real page URLs, never sitemap XML
        file URLs themselves.
        """

        soup = BeautifulSoup(
            xml,
            "xml",
        )

        # A sitemap index references other sitemap files rather than
        # listing pages directly - each <sitemap><loc> is a URL to
        # another sitemap, not a page to crawl.
        if soup.find("sitemapindex"):

            urls: list[str] = []

            # Bound recursion - a very large site could have many
            # sub-sitemaps, and each one is itself a network request.
            sub_sitemap_locs = soup.find_all("loc")[:self.MAX_SUB_SITEMAPS]

            if _depth >= self.MAX_SITEMAP_DEPTH:
                return urls

            for tag in sub_sitemap_locs:

                sub_url = tag.get_text(strip=True)

                if not sub_url:
                    continue

                sub_content = self.fetch_url(
                    sub_url,
                    timeout=timeout,
                    verify_ssl=verify_ssl,
                )

                if not sub_content:
                    continue

                urls.extend(
                    self.parse(
                        sub_content,
                        timeout=timeout,
                        verify_ssl=verify_ssl,
                        _depth=_depth + 1,
                    )
                )

            return list(dict.fromkeys(urls))

        urls = []

        # Standard sitemap
        for tag in soup.find_all("loc"):

            value = tag.get_text(
                strip=True,
            )

            if value:

                urls.append(value)

        return list(
            dict.fromkeys(urls)
        )

    # ---------------------------------------------------------

    def fetch_url(
        self,
        url: str,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> str | None:
        """
        Download an arbitrary sitemap URL (used for sub-sitemaps
        referenced by a sitemap index).
        """

        try:

            response = requests.get(
                url,
                timeout=timeout,
                verify=verify_ssl,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(ReconForge)"
                    )
                },
            )

            if response.status_code != 200:
                return None

            return response.text

        except requests.RequestException:

            return None


sitemap = SitemapParser()