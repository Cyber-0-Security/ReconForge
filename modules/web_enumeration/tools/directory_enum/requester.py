"""
HTTP Requester

Shared HTTP client for directory enumeration.
"""

from __future__ import annotations

import time

import requests

from .models import (
    ScanConfig,
    ScanResult,
    ScanTarget,
)


class HTTPRequester:
    """
    Performs HTTP requests and converts responses
    into ScanResult objects.
    """

    def request(
        self,
        target: ScanTarget,
        config: ScanConfig,
    ) -> ScanResult | None:
        """
        Request a single target.
        """

        start = time.perf_counter()

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

        except requests.RequestException:

            return None

        elapsed = time.perf_counter() - start

        body = response.text

        redirect = None

        if response.is_redirect or response.is_permanent_redirect:

            redirect = response.headers.get(
                "Location"
            )

        return ScanResult(

            url=target.url,

            path=target.path,

            status=response.status_code,

            length=len(response.content),

            words=len(body.split()),

            lines=body.count("\n") + 1,

            content_type=response.headers.get(
                "Content-Type",
                "",
            ),

            redirect=redirect,

            response_time=elapsed,

        )


requester = HTTPRequester()