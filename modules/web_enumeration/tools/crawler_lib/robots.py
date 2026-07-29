"""
Robots.txt Parser

Fetches and extracts paths from robots.txt.
"""

from __future__ import annotations

from urllib.parse import urljoin

import requests


class RobotsParser:
    """
    Handles robots.txt discovery.
    """

    def fetch(
        self,
        url: str,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> str | None:
        """
        Download robots.txt.
        """

        robots_url = urljoin(
            url,
            "/robots.txt",
        )

        try:

            response = requests.get(
                robots_url,
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
        content: str,
    ) -> list[str]:
        """
        Extract interesting paths.
        """

        paths: list[str] = []

        for line in content.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.lower().startswith(
                "disallow:"
            ):

                path = line.split(
                    ":",
                    1,
                )[1].strip()

                if path:
                    paths.append(path)

        return paths


robots = RobotsParser()