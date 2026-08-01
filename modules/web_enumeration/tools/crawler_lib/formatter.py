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

def _print_parameter_intelligence(
    statistics: CrawlStatistics,
) -> None:
    """
    Print classified URL parameters.
    """

    if not statistics.parameter_findings:
        return

    print()
    print("=" * 60)
    print("PARAMETER INTELLIGENCE")
    print("=" * 60)

    grouped: dict[
        tuple[str, str],
        dict[str, object],
    ] = {}

    for finding in statistics.parameter_findings:

        key = (
            finding.name.lower(),
            finding.category,
        )

        if key not in grouped:

            grouped[key] = {

                "severity": finding.severity,

                "urls": set(),

            }

        grouped[key]["urls"].add(
            finding.source,
        )

    severity_order = (
        "HIGH",
        "MEDIUM",
        "LOW",
    )

    icons = {

        "HIGH": "🔴",

        "MEDIUM": "🟡",

        "LOW": "🟢",

    }

    for severity in severity_order:

        entries = [

            (key, value)

            for key, value in grouped.items()

            if value["severity"] == severity

        ]

        if not entries:

            continue

        print()
        print(f"{icons[severity]} {severity}")
        print()

        for (parameter, category), value in sorted(entries):

            urls = sorted(value["urls"])

            print(parameter)

            print(f"    Category    : {category}")

            print(f"    Occurrences : {len(urls)}")

            print("    URLs")

            for url in urls:

                print(f"        {url}")

            print()
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
    print(f"Stop Reason        : {statistics.stop_reason}")

    print()

    print("Status Codes")
    print("-" * 60)

    for status, count in sorted(status_counter.items()):

        print(f"{status:<5} {count}")

    print()

    #
    # Forms are the most actionable recon detail here (login forms,
    # search forms, anything accepting input is worth a pentester's
    # attention) - show them in full rather than only as a count.
    #

    forms_with_pages = [
        (page, form)
        for page in pages
        for form in page.forms
    ]

    if forms_with_pages:

        print("Forms")
        print("-" * 60)

        for page, form in forms_with_pages:

            print(f"[{page.url}]")
            print(f"    Action : {form.action or '(same page)'}")
            print(f"    Method : {form.method}")
            print(f"    Inputs : {', '.join(form.inputs) if form.inputs else '(none named)'}")
            print()

    #
    # Scripts are useful for spotting third-party JS / outdated
    # libraries, but can be numerous - deduplicate across pages.
    #

    unique_scripts = sorted({
        script.url
        for page in pages
        for script in page.scripts
    })
    unique_parameters = sorted(statistics.parameters)

    if unique_parameters:

        print("Parameters")
        print("-" * 60)

        for parameter in unique_parameters:

            print(f"  {parameter}")

        print()
    unique_api = sorted(statistics.api_endpoints)

    if unique_api:

        print("API Endpoints")
        print("-" * 60)

        for endpoint in unique_api:

            print(f"  {endpoint}")

        print()
    unique_emails = sorted(statistics.emails)

    if unique_emails:

        print("Emails")
        print("-" * 60)

        for email in unique_emails:

            print(f"  {email}")

        print()
    interesting = sorted(statistics.interesting_files)

    if interesting:

        print("Interesting Files")
        print("-" * 60)

        for file in interesting:

            print(f"  {file}")

        print()
    if unique_scripts:

        print("Unique Scripts")
        print("-" * 60)

        for script_url in unique_scripts:

            print(f"  {script_url}")

        print()

    #
    # Notable links matched a suspicious keyword (admin, backup,
    # .git, config, etc.) - always shown here regardless of
    # whether the crawler actually had budget left to visit them,
    # so a capped crawl can never silently drop something like
    # this from the report.
    #

    unique_notable = sorted(set(statistics.notable_links))

    if unique_notable:

        print("Notable Links (not necessarily crawled)")
        print("-" * 60)

        for link_url in unique_notable:

            print(f"  {link_url}")

        print()
    _print_parameter_intelligence(statistics,)
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

        if page.parameters:
            print(f"    Parameters : {len(page.parameters)}")

        if page.api_endpoints:
            print(f"    APIs       : {len(page.api_endpoints)}")

        if page.emails:
            print(f"    Emails     : {len(page.emails)}")

        if page.iframes:
            print(f"    Iframes    : {len(page.iframes)}")

        print()