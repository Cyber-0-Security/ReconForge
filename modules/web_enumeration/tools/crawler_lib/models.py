"""
Crawler Models

Shared models used throughout the crawler.
"""

from __future__ import annotations

from dataclasses import dataclass, field

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

    max_pages: int = 40

    max_duration: int = 90

    max_links_to_queue_per_page: int = 200

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

    notable: bool = False

# ---------------------------------------------------------
# Parameter Finding
# ---------------------------------------------------------


@dataclass(slots=True)
class ParameterFinding:
    """
    Interesting URL parameter discovered during crawling.
    """

    name: str

    value: str

    severity: str

    category: str

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
# Parameter
# ---------------------------------------------------------


@dataclass(slots=True)
class Parameter:
    """
    URL query parameter discovered during crawling.
    """

    name: str

    value: str = ""

    source: str = ""

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

    hidden_inputs: list[str] = field(default_factory=list)

    textareas: list[str] = field(default_factory=list)

    selects: list[str] = field(default_factory=list)

    has_file_upload: bool = False

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

    parameters: list[ParameterFinding] = field(default_factory=list)

    scripts: list[Script] = field(default_factory=list)

    forms: list[Form] = field(default_factory=list)

    api_endpoints: list[str] = field(default_factory=list)

    iframes: list[str] = field(default_factory=list)

    emails: list[str] = field(default_factory=list)

    interesting_files: list[str] = field(default_factory=list)

    external_domains: list[str] = field(default_factory=list)

    technologies: list[str] = field(default_factory=list)
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

    stop_reason: str = "completed"

    notable_links: list[str] = field(default_factory=list)

    parameter_findings: list[ParameterFinding] = field(default_factory=list)

    parameters: set[str] = field(default_factory=set)

    api_endpoints: set[str] = field(default_factory=set)

    emails: set[str] = field(default_factory=set)

    technologies: set[str] = field(default_factory=set)

    interesting_files: set[str] = field(default_factory=set)

    external_domains: set[str] = field(default_factory=set)