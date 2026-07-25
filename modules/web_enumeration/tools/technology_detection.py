"""
modules/web_enumeration/tools/technology_detection.py

Technology Detection Tool

Downloads a webpage once, builds a detection context,
and passes it through the fingerprint engine.
"""

from __future__ import annotations

import re
from typing import Any

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator

from modules.web_enumeration.tools.fingerprints.engine import FingerprintEngine
from modules.web_enumeration.tools.fingerprints.models import DetectionContext

from modules.web_enumeration.tools.fingerprints.formatter import print_detections


class TechnologyDetectionTool(BaseTool):
    """
    Detect technologies used by a website.
    """

    def __init__(self) -> None:
        super().__init__("Technology Detection")
        self.engine = FingerprintEngine()

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Download a website and detect technologies.
        """

        self.start(silent)

        if target is None:
            target = validator.get_domain()

        url = self._normalize_url(target)

        if not silent:
            logger.info(f"Downloading {url}")

        try:
            response = requests.get(
                url,
                timeout=20,
                allow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/138.0.0.0 Safari/537.36"
                    )
                },
            )
            response.raise_for_status()

        except requests.RequestException as error:
            logger.error(f"Technology detection failed: {error}")
            self.finish(silent)
            return []

        context = self._build_context(response, url)
        detections = self.engine.detect(context)

        if display:
            print_detections(detections)

        self.finish(silent)

        return [
            {
                "name": item.technology.name,
                "categories": item.technology.categories,
                "confidence": item.confidence,
                "version": item.version,
                "evidence": item.evidence,
            }
            for item in detections
        ]

    def _build_context(
        self,
        response: requests.Response,
        url: str,
        )   -> DetectionContext:
        """
        Build the detection context from the HTTP response.
        """

        html = response.text
        headers = dict(response.headers)
        cookies = response.cookies

        return DetectionContext(
            url=url,
            html=html,
            headers=headers,
            cookies=cookies,
            scripts=self._extract_script_sources(html),
            css=self._extract_css_sources(html),
            meta=self._extract_meta_content(html),
            text=self._strip_tags(html),
            body=html,
        )

    @staticmethod
    def _normalize_url(target: str) -> str:
        """
        Ensure the target has a scheme.
        """

        target = target.strip()

        if target.startswith(("http://", "https://")):
            return target

        return f"https://{target}"

    @staticmethod
    def _extract_script_sources(html: str) -> list[str]:
        """
        Extract script src URLs from HTML.
        """

        scripts = re.findall(
            r'<script[^>]+src=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )
        return [script.strip() for script in scripts if script.strip()]

    @staticmethod
    def _extract_css_sources(html: str) -> list[str]:
        """
        Extract stylesheet URLs from HTML.
        """

        stylesheets = re.findall(
            r'<link[^>]+href=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )
        return [sheet.strip() for sheet in stylesheets if sheet.strip()]

    @staticmethod
    def _extract_meta_content(html: str) -> list[str]:
        """
        Extract meta tag content values from HTML.
        """

        contents = re.findall(
            r'<meta[^>]+content=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )
        return [content.strip() for content in contents if content.strip()]

    @staticmethod
    def _strip_tags(html: str) -> str:
        """
        Remove HTML tags to create plain text for fingerprinting.
        """

        text = re.sub(r"<script.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()