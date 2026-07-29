"""
Crawler Formatter

Pretty prints crawler results.
"""

from __future__ import annotations

from collections import Counter

from .models import (
    CrawlStatistics,
    Page,
)


def print_results(
    pages: list[Page],
    statistics: CrawlStatistics,
) -> None:
    """
    Print crawler results.
    """

    print()

    print("=" * 60)
    print("CRAWLER RESULTS")
    print("=" * 60)

    if not pages:

        print("No pages discovered.")
        print()
        return

    status_counter = Counter()

    total_scripts = 0
    total_forms = 0

    for page in pages:

        status_counter[page.status] += 1

        total_scripts += len(page.scripts)

        total_forms += len(page.forms)

    # -------------------------------------------------

    print(f"Pages Crawled      : {statistics.pages_crawled}")
    print(f"Links Discovered   : {statistics.links_discovered}")
    print(f"URLs Queued        : {statistics.urls_queued}")
    print(f"Duplicates Skipped : {statistics.duplicates_skipped}")
    print(f"Filtered URLs      : {statistics.invalid_skipped}")
    print(f"Scripts Found      : {total_scripts}")
    print(f"Forms Found        : {total_forms}")

    print()

    print("Status Codes")
    print("-" * 60)

    for status, count in sorted(status_counter.items()):

        print(f"{status:<5} {count}")

    print()

    print("Pages")
    print("-" * 60)

    for page in pages:

        print(f"[{page.status}] {page.url}")

        if page.title:

            print(f"    Title   : {page.title}")

        print(f"    Depth   : {page.depth}")

        print(f"    Links   : {len(page.links)}")

        print(f"    Scripts : {len(page.scripts)}")

        print(f"    Forms   : {len(page.forms)}")

        print()