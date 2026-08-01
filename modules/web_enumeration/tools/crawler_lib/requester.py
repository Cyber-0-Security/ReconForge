"""
Crawler Requester

Downloads web pages for the crawler.
"""

from __future__ import annotations

import requests


class CrawlRequester:
    """
    Handles HTTP requests for the crawler.
    """

    def get(
        self,
        *,
        url: str,
        timeout: int,
        follow_redirects: bool,
        verify_ssl: bool,
        user_agent: str,
    ) -> requests.Response | None:
        """
        Download a page.
        """

        try:

            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=follow_redirects,
                verify=verify_ssl,
                headers={
                    "User-Agent": user_agent,
                },
            )

            return response

        except requests.RequestException:

            return None


requester = CrawlRequester()