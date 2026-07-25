"""
modules/information_gathering/tools/http_headers.py

HTTP Headers Tool

Fetches and displays HTTP response headers for a target URL.
"""

from __future__ import annotations

from typing import Any

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator


class HTTPHeadersTool(BaseTool):
    """
    Retrieve HTTP headers for a URL.
    """

    def __init__(self) -> None:
        super().__init__("HTTP Headers")

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> dict[str, Any]:

        self.start(silent)

        if target is None:
            target = validator.get_domain()

        url = self._normalize_url(target)
        results: dict[str, Any] = {}

        try:

            if not silent:
                logger.info(f"Fetching headers for {url}")

            response = requests.get(
                url,
                timeout=15,
                allow_redirects=True,
                headers={
                    "User-Agent": "ReconForge/1.0",
                },
            )

            results = {
                "Status Code": response.status_code,
                "Final URL": response.url,
                "Headers": dict(response.headers),
            }

            if display:
                print()
                print("=" * 60)
                print("HTTP HEADERS")
                print("=" * 60)
                print(f"Status Code : {response.status_code}")
                print(f"Final URL   : {response.url}")
                print()
                print("Response Headers")
                print("-" * 60)

                for key, value in response.headers.items():
                    print(f"{key:<20}: {value}")

                print()

        except requests.exceptions.Timeout:

            if display:
                print("Request timed out.")

        except requests.exceptions.ConnectionError:

            if display:
                print("Unable to connect to target.")

        except requests.exceptions.HTTPError as error:

            if display:
                print(f"HTTP Error: {error}")

        except Exception as error:

            if not silent:
                logger.error(f"HTTP headers lookup failed for {url}: {error}")

            if display:
                print(f"Error: {error}")

        self.finish(silent)

        return results

    @staticmethod
    def _normalize_url(target: str) -> str:
        target = target.strip()

        if target.startswith(("http://", "https://")):
            return target

        return f"https://{target}"