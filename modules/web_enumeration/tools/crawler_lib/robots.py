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
        Download robots.txt.
        """

        robots_url = urljoin(
            url,
            "/robots.txt",
        )

        try:

            response = self._session.get(

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
        Extract interesting paths from robots.txt.
        """

        paths: set[str] = set()

        for line in content.splitlines():

            line = line.strip()

            if not line:

                continue

            if line.startswith("#"):

                continue

            #
            # Remove inline comments.
            #

            line = line.split(
                "#",
                1,
            )[0].strip()

            if not line:

                continue

            key, separator, value = line.partition(":")

            if not separator:

                continue

            key = key.strip().lower()

            value = value.strip()

            if not value:

                continue

            #
            # Ignore wildcard-only entries, and truncate any path
            # containing a wildcard down to its literal prefix -
            # e.g. "/wp-content/*" becomes "/wp-content/", a real
            # path worth checking, rather than a literal URL with
            # an asterisk in it (which robots.txt entries like this
            # were producing before this fix).
            #

            if value == "*":

                continue

            if "*" in value:

                value = value.split("*", 1)[0]

                if not value or value == "/":

                    continue

            if key in (
                "disallow",
                "allow",
            ):

                paths.add(value)

        return sorted(paths)


robots = RobotsParser()