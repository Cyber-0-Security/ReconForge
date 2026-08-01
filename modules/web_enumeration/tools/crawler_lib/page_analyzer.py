"""
Page Analyzer

Collects all page analysis in one place.
"""

from __future__ import annotations

from bs4 import BeautifulSoup

from .resource_extractor import resource_extractor
from .technology_detector import technology_detector


class PageAnalyzer:
    """
    Performs analysis on a parsed page.
    """

    def analyze(
        self,
        page,
        soup: BeautifulSoup,
        response,
    ) -> None:

        page.server = response.headers.get(
            "Server",
            "",
        )

        page.images = resource_extractor.images(
            soup,
            page.url,
        )

        page.stylesheets = (
            resource_extractor.stylesheets(
                soup,
                page.url,
            )
        )

        page.iframes = resource_extractor.iframes(
            soup,
            page.url,
        )

        page.audio = resource_extractor.audio(
            soup,
            page.url,
        )

        page.videos = resource_extractor.videos(
            soup,
            page.url,
        )

        page.favicon = resource_extractor.favicon(
            soup,
            page.url,
        )

        page.canonical = resource_extractor.canonical(
            soup,
            page.url,
        )

        page.meta_refresh = (
            resource_extractor.meta_refresh(
                soup,
            )
        )

        page.technologies = (
            technology_detector.detect(
                response,
                soup,
            )
        )


analyzer = PageAnalyzer()