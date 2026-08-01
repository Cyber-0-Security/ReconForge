"""
JavaScript Endpoint Extractor

Extracts interesting endpoints from inline and external JavaScript.
"""

from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup


class JavaScriptEndpointExtractor:
    """
    Extract endpoints from JavaScript.
    """

    # Common endpoint patterns
    ENDPOINT_PATTERN = re.compile(
        r"""
        (?:
            "(\/[^"]+)"|
            '(\/[^']+)'|
            "(https?:\/\/[^"]+)"|
            '(https?:\/\/[^']+)'
        )
        """,
        re.VERBOSE,
    )

    # ---------------------------------------------------------

    def extract(
        self,
        soup: BeautifulSoup,
        page_url: str,
        timeout: int,
        verify_ssl: bool,
    ) -> list[str]:

        endpoints: set[str] = set()

        # ---------------------------------------------
        # Inline JavaScript
        # ---------------------------------------------

        for script in soup.find_all("script"):

            if script.string:

                endpoints.update(
                    self._find(
                        script.string,
                    )
                )

        # ---------------------------------------------
        # External JavaScript
        # ---------------------------------------------

        for script in soup.find_all(
            "script",
            src=True,
        ):

            try:

                response = requests.get(
                    script["src"],
                    timeout=timeout,
                    verify=verify_ssl,
                )

                endpoints.update(
                    self._find(
                        response.text,
                    )
                )

            except Exception:
                continue

        return sorted(endpoints)

    # ---------------------------------------------------------

    def _find(
        self,
        text: str,
    ) -> set[str]:

        found = set()

        for match in self.ENDPOINT_PATTERN.findall(text):

            for item in match:

                if item:

                    found.add(item)

        return found


js_endpoint_extractor = JavaScriptEndpointExtractor()