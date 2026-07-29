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
    ) -> list[str]:
        """
        Extract every URL from a sitemap.
        Supports both sitemap.xml and sitemap index files.
        """

        soup = BeautifulSoup(
            xml,
            "xml",
        )

        urls: list[str] = []

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


sitemap = SitemapParser()