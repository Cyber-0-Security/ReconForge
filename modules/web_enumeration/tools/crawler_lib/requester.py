"""
Crawler Requester

Downloads web pages for the crawler.
"""

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .models import (
    CrawlConfig,
    CrawlTarget,
)


class CrawlRequester:
    """
    Handles HTTP requests for the crawler.
    """

    def __init__(self) -> None:
        """
        Create a reusable HTTP session.
        """

        self._session = requests.Session()

        retries = Retry(
            total=2,
            connect=2,
            read=2,
            backoff_factor=0.5,
            status_forcelist=(
                429,
                500,
                502,
                503,
                504,
            ),
            allowed_methods=frozenset({"GET", "HEAD"}),
        )

        adapter = HTTPAdapter(
            max_retries=retries,
            pool_connections=20,
            pool_maxsize=20,
        )

        self._session.mount(
            "http://",
            adapter,
        )

        self._session.mount(
            "https://",
            adapter,
        )

    # ---------------------------------------------------------

    def request(
        self,
        target: CrawlTarget,
        config: CrawlConfig,
    ) -> requests.Response | None:
        """
        Download a page.
        """

        try:

            response = self._session.get(

                target.url,

                timeout=config.timeout,

                allow_redirects=config.follow_redirects,

                verify=config.verify_ssl,

                headers={
                    "User-Agent": config.user_agent,
                    "Accept": (
                        "text/html,"
                        "application/xhtml+xml,"
                        "application/xml;q=0.9,*/*;q=0.8"
                    ),
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                },

            )

            return response

        except (
            requests.Timeout,
            requests.ConnectionError,
            requests.TooManyRedirects,
            requests.RequestException,
        ):

            return None


requester = CrawlRequester()