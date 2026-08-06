"""
Crawler Parser

Parses HTML pages into ReconForge models.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .models import (
    CrawlTarget,
    Form,
    Link,
    Page,
    Script,
    ParameterFinding,
)

from .parameter_intelligence import parameter_intelligence
from .js_analyzer import javascript_analyzer

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
        # Only parse HTML.
        #

        if "html" not in content_type.lower():
            return page

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        #
        # Basic extraction
        #

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

        page.parameters = self._extract_parameters(
            page.links,
        )

        #
        # APIs discovered directly from HTML links
        #

        page.api_endpoints.extend(
            self._extract_api_endpoints(
                page.links,
            )
        )

        #
        # APIs/endpoints discovered inside inline JavaScript
        #

        page.javascript_endpoints.extend(
            self._extract_js_endpoints(
                soup,
                response.url,
            )
        )

        #
        # Analyze external JavaScript files
        #

        for script in page.scripts:

            source = javascript_analyzer.fetch(
                script.url,
            )

            if not source:
                continue

            result = javascript_analyzer.analyze(
                source,
                script.url,
            )

            #
            # JavaScript-discovered endpoints
            #

            page.javascript_endpoints.extend(
                result.endpoints
            )

            page.api_endpoints.extend(
                result.graphql
            )

            page.interesting_files.extend(
                result.cloud_buckets
            )

        #
        # Remaining extraction
        #

        page.iframes = self._extract_iframes(
            soup,
            response.url,
        )

        page.emails = self._extract_emails(
            response.text,
        )

        page.interesting_files.extend(
            self._extract_interesting_files(
                page.links,
            )
        )

        page.external_domains = self._extract_external_domains(
            page.links,
            response.url,
        )

        #
        # Remove duplicates
        #

        page.api_endpoints = sorted(
            set(page.api_endpoints)
        )

        page.javascript_endpoints = sorted(
            set(page.javascript_endpoints)
        )

        page.interesting_files = sorted(
            set(page.interesting_files)
        )

        page.external_domains = sorted(
            set(page.external_domains)
        )

        page.emails = sorted(
            set(page.emails)
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
    API_KEYWORDS = (
        "/api/",
        "/graphql",
        "/rest/",
        "/v1/",
        "/v2/",
        "/v3/",
    )

    INTERESTING_EXTENSIONS = (
        ".zip",
        ".bak",
        ".sql",
        ".env",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".conf",
        ".config",
        ".log",
    )

    EMAIL_REGEX = re.compile(
        r"(?<![\w/.-])"
        r"[A-Za-z0-9._%+-]+"
        r"@"
        r"(?:[A-Za-z0-9-]+\.)+"
        r"[A-Za-z]{2,}"
        r"(?![\w.-])"
    )

    JS_ENDPOINT_PATTERNS = (

        r'fetch\(\s*[\'"]([^\'"]+)',

        r'axios\.(?:get|post|put|delete|patch)\(\s*[\'"]([^\'"]+)',

        r'url\s*:\s*[\'"]([^\'"]+)',

        r'XMLHttpRequest.*?open\([^,]+,\s*[\'"]([^\'"]+)',

        r'\$\.ajax\(\{[^}]*url\s*:\s*[\'"]([^\'"]+)',

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
        seen_urls: set[str] = set()

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
            if url in seen_urls:
                continue

            seen_urls.add(url)
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

        forms: list[Form] = []

        for form in soup.find_all("form"):

            inputs = []
            hidden = []
            textareas = []
            selects = []
            has_file = False

            for field in form.find_all("input"):

                name = field.get("name")

                if not name:
                    continue

                inputs.append(name)

                if field.get("type", "").lower() == "hidden":
                    hidden.append(name)

                if field.get("type", "").lower() == "file":
                    has_file = True

            for textarea in form.find_all("textarea"):

                name = textarea.get("name")

                if name:
                    textareas.append(name)

            for select in form.find_all("select"):

                name = select.get("name")

                if name:
                    selects.append(name)

            forms.append(

                Form(

                    action=urljoin(
                        base_url,
                        form.get("action", ""),
                    ),

                    method=form.get(
                        "method",
                        "GET",
                    ).upper(),

                    inputs=inputs,

                    hidden_inputs=hidden,

                    textareas=textareas,

                    selects=selects,

                    has_file_upload=has_file,

                )

            )

        return forms
    
    @staticmethod
    def _extract_parameters(
        links: list[Link],
    ) -> list[ParameterFinding]:
        """
        Analyze parameters found in discovered links.
        """

        findings: list[ParameterFinding] = []

        seen: set[tuple[str, str, str]] = set()

        for link in links:

            for finding in parameter_intelligence.analyze(link.url):

                key = (
                    finding.name.lower(),
                    finding.category,
                    finding.source,
                )

                if key in seen:
                    continue

                seen.add(key)

                findings.append(finding)

        return findings
    @classmethod
    def _extract_api_endpoints(
        cls,
        links: list[Link],
    ) -> list[str]:

        return sorted({

            link.url

            for link in links

            if any(
                keyword in link.url.lower()
                for keyword in cls.API_KEYWORDS
            )

        })
    @classmethod
    def _extract_js_endpoints(
        cls,
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:
        """
        Extract API endpoints referenced inside JavaScript.
        """

        endpoints = set()

        #
        # Inline JavaScript
        #

        for script in soup.find_all("script"):

            code = script.string

            if not code:
                continue

            for pattern in cls.JS_ENDPOINT_PATTERNS:

                for match in re.findall(
                    pattern,
                    code,
                    re.DOTALL,
                ):

                    endpoints.add(
                        urljoin(
                            base_url,
                            match,
                        )
                    )

        return sorted(endpoints)
    @classmethod
    def _extract_emails(
        cls,
        text: str,
    ) -> list[str]:

        emails = set()

        bad_domains = {
            "2x.png",
            "2x.jpg",
            "2x.jpeg",
            "2x.webp",
            "2x.gif",
            "2x.svg",
            "3x.png",
            "3x.jpg",
            "3x.jpeg",
            "3x.webp",
            "3x.gif",
            "3x.svg",
        }

        for email in cls.EMAIL_REGEX.findall(text):
            print(repr(email))
            domain = email.split("@", 1)[1].lower()

            if domain in bad_domains:
                continue

            emails.add(email)

        return sorted(emails)
    @staticmethod
    def _extract_iframes(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        return [

            urljoin(base_url, frame["src"])

            for frame in soup.find_all("iframe", src=True)

        ]
    
    @classmethod
    def _extract_interesting_files(
        cls,
        links: list[Link],
    ) -> list[str]:

        return [

            link.url

            for link in links

            if link.url.lower().endswith(

                cls.INTERESTING_EXTENSIONS

            )

        ]

    @staticmethod
    def _extract_external_domains(
        links: list[Link],
        base_url: str,
    ) -> list[str]:

        base_host = urlparse(base_url).hostname

        domains = set()

        for link in links:

            host = urlparse(link.url).hostname

            if host and host != base_host:

                domains.add(host)

        return sorted(domains)
    
parser = CrawlParser()