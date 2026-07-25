"""
modules/web_enumeration/tools/technology_detection.py

Technology Detection Tool

Downloads a webpage once and passes the
response to multiple fingerprint detectors.
"""

from __future__ import annotations

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator

from modules.web_enumeration.tools.fingerprints.headers import detect_headers
from modules.web_enumeration.tools.fingerprints.html import detect_html
from modules.web_enumeration.tools.fingerprints.javascript import detect_javascript
from modules.web_enumeration.tools.fingerprints.cookies import detect_cookies
from modules.web_enumeration.tools.fingerprints.meta import detect_meta
from modules.web_enumeration.tools.fingerprints.css import detect_css

from modules.web_enumeration.tools.fingerprints.analytics import detect_analytics
from modules.web_enumeration.tools.fingerprints.cdn import detect_cdn
from modules.web_enumeration.tools.fingerprints.cms import detect_cms
from modules.web_enumeration.tools.fingerprints.framework import detect_frameworks
from modules.web_enumeration.tools.fingerprints.security import detect_security
from modules.web_enumeration.tools.fingerprints.hosting import detect_hosting
from modules.web_enumeration.tools.fingerprints.payment import detect_payment
from modules.web_enumeration.tools.fingerprints.chat import detect_chat
from modules.web_enumeration.tools.fingerprints.fonts import detect_fonts

from modules.web_enumeration.tools.fingerprints.formatter import print_technologies

class TechnologyDetectionTool(BaseTool):
    """
    Detect technologies used by a website.
    """

    def __init__(self) -> None:

        super().__init__("Technology Detection")

    def _run_detectors(
        self,
        response: requests.Response,
        ) -> set[str]:

        html = response.text

        technologies = set()

        technologies.update(
            detect_headers(response.headers)
        )

        technologies.update(
            detect_html(html)
        )

        technologies.update(
            detect_javascript(html)
        )

        technologies.update(
            detect_cookies(response.cookies)
        )

        technologies.update(
            detect_meta(html)
        )

        technologies.update(
            detect_css(html)
        )

        technologies.update(
            detect_analytics(html)
        )

        technologies.update(
            detect_cdn(
                response.headers,
                html,
            )
        )

        technologies.update(
            detect_cms(
                response.headers,
                html,
                response.cookies,
            )
        )

        technologies.update(
            detect_frameworks(
                response.headers,
                html,
            )
        )

        technologies.update(
            detect_security(
                response.headers,
                html,
            )
        )

        technologies.update(
            detect_hosting(
                response.headers,
                html,
            )
        )

        technologies.update(
            detect_payment(html)
        )

        technologies.update(
            detect_chat(html)
        )

        technologies.update(
            detect_fonts(html)
        )

        return technologies
    
    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> set[str]:

        self.start()

        if target is None:
            target = validator.get_domain("Enter domain: ")

        url = f"https://{target}"

        logger.info(f"Downloading {url}")

        technologies: set[str] = set()

        try:

            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/138.0.0.0 Safari/537.36"
                    )
                },
            )

            technologies = self._run_detectors(response)

        except requests.RequestException as error:

            logger.error(error)

            self.finish()

            return set()

        if display:

            print()
            print("=" * 60)
            print("TECHNOLOGY DETECTION")
            print("=" * 60)

            if technologies:

                print_technologies(technologies)

            else:

                print("No technologies detected.")

        self.finish()

        return technologies

    @staticmethod
    def normalize_url(target: str) -> str:

        if target.startswith(("http://", "https://")):

            return target

        return f"https://{target}"