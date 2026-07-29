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

    timeout: int = 10

    follow_redirects: bool = True

    verify_ssl: bool = True

    include_subdomains: bool = False

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

    links: list[Link] = field(default_factory=list)

    scripts: list[Script] = field(default_factory=list)

    forms: list[Form] = field(default_factory=list)


# ---------------------------------------------------------
# Crawl Statistics
# ---------------------------------------------------------


@dataclass(slots=True)
class CrawlStatistics:
    """
    Crawl statistics.
    """

    pages_crawled: int = 0

    links_discovered: int = 0

    urls_queued: int = 0

    duplicates_skipped: int = 0

    external_skipped: int = 0

    static_skipped: int = 0

    invalid_skipped: int = 0