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

        return page

    # ---------------------------------------------------------

    @staticmethod
    def _extract_title(
        soup: BeautifulSoup,
    ) -> str:
        """
        Extract page title.
        """

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
        """
        Extract hyperlinks.
        """

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
        """
        Extract JavaScript files.
        """

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
        """
        Extract HTML forms.
        """

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