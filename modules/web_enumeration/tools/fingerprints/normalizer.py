"""
Normalizer

Normalizes collected webpage data before fingerprint matching.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import DetectionContext


class ContextNormalizer:
    """
    Normalize DetectionContext for reliable matching.
    """

    def normalize(
        self,
        context: DetectionContext,
    ) -> DetectionContext:

        context.headers = self._normalize_headers(
            context.headers
        )

        context.scripts = self._normalize_urls(
            context.scripts
        )

        context.css = self._normalize_urls(
            context.css
        )

        context.meta = [
            self._clean(x)
            for x in context.meta
        ]

        context.html = self._clean_html(
            context.html
        )

        context.body = self._clean_html(
            context.body
        )

        context.text = self._clean(
            context.text
        )

        return context

    # ---------------------------------------------------------

    def _normalize_headers(
        self,
        headers: dict,
    ) -> dict:

        normalized = {}

        for key, value in headers.items():

            normalized[
                key.lower().strip()
            ] = str(value).strip()

        return normalized

    # ---------------------------------------------------------

    def _normalize_urls(
        self,
        urls: list[str],
    ) -> list[str]:

        cleaned = []

        for url in urls:

            url = url.strip()

            parsed = urlparse(url)

            path = parsed.path.lower()

            cleaned.append(path)

        return cleaned

    # ---------------------------------------------------------

    def _clean(
        self,
        text: str,
    ) -> str:

        text = text.lower()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    # ---------------------------------------------------------

    def _clean_html(
        self,
        html: str,
    ) -> str:

        html = html.lower()

        html = html.replace(
            "\n",
            " ",
        )

        html = re.sub(
            r"\s+",
            " ",
            html,
        )

        return html


normalizer = ContextNormalizer()