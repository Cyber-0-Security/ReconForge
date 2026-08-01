"""
Crawler Formatter

Pretty terminal output for ReconForge crawler.
"""

from __future__ import annotations

from collections import Counter

from config.constants import Colors

from .logger import logger
from .models import CrawlStatistics, Page


class CrawlFormatter:
    """
    Formats crawler output.
    """

    def display(
        self,
        pages: list[Page],
        statistics: CrawlStatistics,
    ) -> None:

        print()
        print("=" * 70)
        print(f"{Colors.BOLD}CRAWLER SUMMARY{Colors.RESET}")
        print("=" * 70)

        print(
            f"{Colors.GREEN}Pages Crawled     :{Colors.RESET} {statistics.pages_crawled}"
        )
        print(
            f"{Colors.GREEN}URLs Queued       :{Colors.RESET} {statistics.urls_queued}"
        )
        print(
            f"{Colors.GREEN}Links Found       :{Colors.RESET} {statistics.links_discovered}"
        )
        print(
            f"{Colors.YELLOW}Duplicates        :{Colors.RESET} {statistics.duplicates_skipped}"
        )
        print(
            f"{Colors.YELLOW}External Skipped  :{Colors.RESET} {statistics.external_skipped}"
        )
        print(
            f"{Colors.YELLOW}Static Skipped    :{Colors.RESET} {statistics.static_skipped}"
        )
        print(
            f"{Colors.YELLOW}Invalid Skipped   :{Colors.RESET} {statistics.invalid_skipped}"
        )

        status_counter = Counter(page.status for page in pages)

        print()
        print("=" * 70)
        print(f"{Colors.BOLD}STATUS CODES{Colors.RESET}")
        print("=" * 70)

        for status in sorted(status_counter):
            print(
                f"{status:<5} : {status_counter[status]}"
            )

        # Only print page details in verbose/debug mode
        if logger.level not in ("verbose", "debug"):
            return

        print()
        print("=" * 70)
        print(f"{Colors.BOLD}DISCOVERED PAGES{Colors.RESET}")
        print("=" * 70)

        for page in sorted(
            pages,
            key=lambda p: (p.depth, p.url),
        ):

            print()
            print(f"[{page.status}] {page.url}")
            print(f"    Title        : {page.title}")
            print(f"    Depth        : {page.depth}")
            print(f"    Links        : {len(page.links)}")
            print(f"    Scripts      : {len(page.scripts)}")
            print(f"    Images       : {len(page.images)}")
            print(f"    CSS          : {len(page.stylesheets)}")
            print(f"    Iframes      : {len(page.iframes)}")
            print(f"    Forms        : {len(page.forms)}")

            if page.server:
                print(f"    Server       : {page.server}")

            if page.canonical:
                print(f"    Canonical    : {page.canonical}")

            if page.favicon:
                print(f"    Favicon      : {page.favicon}")

            if page.meta_refresh:
                print(f"    MetaRefresh  : {page.meta_refresh}")

            if page.technologies:
                print(
                    "    Technologies: "
                    + ", ".join(sorted(page.technologies))
                )


formatter = CrawlFormatter()