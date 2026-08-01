"""
Crawler Requester

Downloads web pages for the crawler.
"""

from __future__ import annotations

import requests

from .models import (
    CrawlConfig,
    CrawlTarget,
)


class CrawlRequester:
    """
    Handles HTTP requests for the crawler.
    """

    def request(
        self,
        target: CrawlTarget,
        config: CrawlConfig,
    ) -> requests.Response | None:
        """
        Download a page.
        """

        try:

            response = requests.get(

                target.url,

                timeout=config.timeout,

                allow_redirects=config.follow_redirects,

                verify=config.verify_ssl,

                headers={
                    "User-Agent": config.user_agent,
                },

            )

            return response

        except requests.RequestException:

            return None


requester = CrawlRequester()