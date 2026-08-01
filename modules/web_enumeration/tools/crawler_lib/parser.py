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

        content_type = response.headers.get("Content-Type", "")

        page = Page(
            url=response.url,
            status=response.status_code,
            title="",
            depth=target.depth,
            content_type=content_type,
        )

        #
        # Only parse actual HTML - running an HTML parser against
        # XML/JSON/binary responses produces nothing useful (and,
        # for XML, a BeautifulSoup warning on every single page).
        #

        if "html" not in content_type.lower():
            return page

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        page.title = self._extract_title(soup)

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

    #
    # A single page (a package index, search results listing, huge
    # sitemap-style page, etc.) can contain an enormous number of
    # links - real-world example: pypi.org/simple/ alone contains
    # over 860,000 links. This limit exists purely to stop memory/
    # CPU blowing up while parsing such a page - it is NOT the
    # limit on how many links get followed (that happens later,
    # in the engine, where it can prioritize which links matter).
    #
    MAX_LINKS_PER_PAGE = 2000

    #
    # Keywords that make a discovered link worth flagging to the
    # user even if the crawler never actually visits it. Matching
    # is intentionally kept broad and simple (substring match) -
    # false positives here just mean an extra line in the report,
    # not a missed page.
    #
    NOTABLE_KEYWORDS = (
        "admin", "login", "signin", "backup", "config",
        "secret", "internal", "staging", "debug", "dashboard",
        "console", "phpmyadmin", "wp-admin",
        ".git", ".env", ".sql", ".bak", "swagger",
        "api-docs", "actuator", "phpinfo",
    )

    @classmethod
    def _is_notable(cls, url: str) -> bool:
        """
        Flag a URL as worth surfacing in the report, regardless of
        whether it actually gets crawled.
        """

        lowered = url.lower()

        return any(
            keyword in lowered
            for keyword in cls.NOTABLE_KEYWORDS
        )

    @classmethod
    def _extract_links(
        cls,
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

            if len(links) >= cls.MAX_LINKS_PER_PAGE:
                break

            url = urljoin(
                base_url,
                tag["href"],
            )

            links.append(

                Link(

                    url=url,

                    text=tag.get_text(
                        strip=True,
                    ),

                    source=base_url,

                    notable=cls._is_notable(url),

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