"""
Crawler Parser

Parses HTML pages into ReconForge models.
"""

from __future__ import annotations

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .models import (
    CrawlTarget,
    Form,
    Link,
    Page,
    Script,
)
from .resource_extractor import resource_extractor
from .technology_detector import technology_detector


class CrawlParser:
    """
    Parses HTML pages into structured models.
    """

    def parse(
        self,
        response: requests.Response,
        target: CrawlTarget,
    ) -> Page:
        """
        Parse a downloaded page.
        """

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        page = Page(
            url=response.url,
            status=response.status_code,
            title=self._extract_title(soup),
            depth=target.depth,
            content_type=response.headers.get(
                "Content-Type",
                "",
            ),
        )

        # -----------------------------------------
        # Basic Enumeration
        # -----------------------------------------

        page.links = self._extract_links(
            soup,
            response.url,
        )

        page.scripts = self._extract_scripts(
            soup,
            response.url,
        )

        page.forms = self._extract_forms(
            soup,
            response.url,
        )

        # -----------------------------------------
        # Resources
        # -----------------------------------------

        page.images = resource_extractor.images(
            soup,
            response.url,
        )

        page.stylesheets = resource_extractor.stylesheets(
            soup,
            response.url,
        )

        page.iframes = resource_extractor.iframes(
            soup,
            response.url,
        )

        page.videos = resource_extractor.videos(
            soup,
            response.url,
        )

        page.audio = resource_extractor.audio(
            soup,
            response.url,
        )

        # -----------------------------------------
        # Metadata
        # -----------------------------------------

        page.server = response.headers.get(
            "Server",
        )

        page.favicon = resource_extractor.favicon(
            soup,
            response.url,
        )

        page.canonical = resource_extractor.canonical(
            soup,
            response.url,
        )

        page.meta_refresh = resource_extractor.meta_refresh(
            soup,
        )

        # -----------------------------------------
        # Technology Detection
        # -----------------------------------------

        page.technologies = technology_detector.detect(
            soup,
            response,
        )

        return page

    # ---------------------------------------------------------

    @staticmethod
    def _extract_title(
        soup: BeautifulSoup,
    ) -> str:

        if soup.title:

            return soup.title.get_text(
                strip=True,
            )

        return ""

    # ---------------------------------------------------------

    @staticmethod
    def _extract_links(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[Link]:

        links: list[Link] = []

        for tag in soup.find_all(
            "a",
            href=True,
        ):

            links.append(

                Link(

                    url=urljoin(
                        base_url,
                        tag["href"],
                    ),

                    text=tag.get_text(
                        strip=True,
                    ),

                    source=base_url,

                )

            )

        return links

    # ---------------------------------------------------------

    @staticmethod
    def _extract_scripts(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[Script]:

        scripts: list[Script] = []

        for tag in soup.find_all(
            "script",
            src=True,
        ):

            scripts.append(

                Script(

                    url=urljoin(
                        base_url,
                        tag["src"],
                    )

                )

            )

        return scripts

    # ---------------------------------------------------------

    @staticmethod
    def _extract_forms(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[Form]:

        forms: list[Form] = []

        for form in soup.find_all("form"):

            inputs: list[str] = []

            for field in form.find_all("input"):

                name = field.get("name")

                if name:

                    inputs.append(name)

            forms.append(

                Form(

                    action=urljoin(
                        base_url,
                        form.get(
                            "action",
                            "",
                        ),
                    ),

                    method=form.get(
                        "method",
                        "GET",
                    ).upper(),

                    inputs=inputs,

                )

            )

        return forms


parser = CrawlParser()