"""
Crawler Models

Shared models used throughout the crawler.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------
# Crawl Configuration
# ---------------------------------------------------------


@dataclass(slots=True)
class CrawlConfig:
    """
    Crawl configuration.
    """

    url: str

    max_depth: int = 2

    threads: int = 20

    timeout: int = 10

    follow_redirects: bool = True

    verify_ssl: bool = True

    include_subdomains: bool = False

    verbosity: int = 1

    user_agent: str = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0.0.0 "
        "Safari/537.36"
    )


# ---------------------------------------------------------
# Crawl Target
# ---------------------------------------------------------


@dataclass(slots=True)
class CrawlTarget:
    """
    Queue item.
    """

    url: str

    depth: int


# ---------------------------------------------------------
# Link
# ---------------------------------------------------------


@dataclass(slots=True)
class Link:
    """
    Hyperlink.
    """

    url: str

    text: str

    source: str


# ---------------------------------------------------------
# Script
# ---------------------------------------------------------


@dataclass(slots=True)
class Script:
    """
    JavaScript file.
    """

    url: str


# ---------------------------------------------------------
# Form
# ---------------------------------------------------------


@dataclass(slots=True)
class Form:
    """
    HTML Form.
    """

    action: str

    method: str

    inputs: list[str] = field(default_factory=list)


# ---------------------------------------------------------
# Page
# ---------------------------------------------------------


@dataclass(slots=True)
class Page:
    """
    Crawled page.
    """

    url: str

    status: int

    title: str

    depth: int

    content_type: str

    server: str = ""

    canonical: str | None = None

    favicon: str | None = None

    meta_refresh: str | None = None

    links: list[Link] = field(default_factory=list)

    scripts: list[Script] = field(default_factory=list)

    forms: list[Form] = field(default_factory=list)

    images: list[str] = field(default_factory=list)

    stylesheets: list[str] = field(default_factory=list)

    iframes: list[str] = field(default_factory=list)

    videos: list[str] = field(default_factory=list)

    audio: list[str] = field(default_factory=list)

    technologies: list[str] = field(default_factory=list)
# ---------------------------------------------------------
# Crawl Statistics
# ---------------------------------------------------------


@dataclass(slots=True)
class CrawlStatistics:
    """
    Crawl statistics.
    """

    # Overall
    pages_crawled: int = 0

    links_discovered: int = 0

    urls_queued: int = 0

    duplicates_skipped: int = 0

    # Filtered
    invalid_skipped: int = 0

    external_skipped: int = 0

    static_skipped: int = 0

    javascript_skipped: int = 0

    mailto_skipped: int = 0

    telephone_skipped: int = 0

    fragment_skipped: int = 0

    empty_skipped: int = 0

    # Resources
    scripts_found: int = 0

    forms_found: int = 0

    images_found: int = 0

    css_found: int = 0

    iframes_found: int = 0