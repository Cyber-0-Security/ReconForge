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
from .parser import CrawlParser

# ---------------------------------------------------------
# Helper printing functions
# ---------------------------------------------------------

def _print_header(title: str) -> None:

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def _print_subheader(title: str) -> None:

    print()
    print(title)
    print("-" * 60)

def _print_summary(
    pages: list[Page],
    statistics: CrawlStatistics,
) -> None:

    total_scripts = sum(
        len(page.scripts)
        for page in pages
    )

    total_forms = sum(
        len(page.forms)
        for page in pages
    )

    total_parameters = sum(
        len(page.parameters)
        for page in pages
    )

    total_emails = len({
        email
        for page in pages
        for email in page.emails
    })

    total_api = len({
        api
        for page in pages
        for api in page.api_endpoints
    })

    total_files = len({
        file
        for page in pages
        for file in page.interesting_files
    })

    _print_header("CRAWLER SUMMARY")

    print(f"✓ Pages Crawled      : {statistics.pages_crawled}")
    print(f"✓ Links Discovered   : {statistics.links_discovered}")
    print(f"✓ URLs Queued        : {statistics.urls_queued}")
    print(f"✓ Forms             : {total_forms}")
    print(f"✓ Parameters        : {total_parameters}")
    print(f"✓ Emails            : {total_emails}")
    print(f"✓ API Endpoints     : {total_api}")
    print(f"✓ Interesting Files : {total_files}")
    print(f"✓ Scripts           : {total_scripts}")
    print(f"✓ Stop Reason       : {statistics.stop_reason}")

def _print_high_priority(
    pages: list[Page],
    statistics: CrawlStatistics,
    ) -> None:
    """
    Print high-value discoveries.
    """

    admin = set()
    login = set()
    upload = set()
    api = set()
    config = set()

    for page in pages:

        for link in page.links:

            url = link.url.lower()

            if any(x in url for x in ("admin", "administrator")):
                admin.add(link.url)

            if any(x in url for x in ("login", "signin", "auth")):
                login.add(link.url)

            if "upload" in url:
                upload.add(link.url)

            if any(x in url for x in (
                ".env",
                ".git",
                "backup",
                ".bak",
                ".sql",
                "config",
            )):
                config.add(link.url)

        for endpoint in page.api_endpoints:
            api.add(endpoint)

    if not any((admin, login, upload, api, config)):
        return
    
    if statistics.javascript_endpoints:

        print("JavaScript Endpoints")
        print("-" * 60)

        for endpoint in sorted(statistics.javascript_endpoints):

            print(f"  {endpoint}")

        print()
    _print_header("HIGH PRIORITY FINDINGS")

    def print_group(title: str, values: set[str]) -> None:

        if not values:
            return

        print(f"[{title}]")

        for value in sorted(values):
            print(f"  {value}")

        print()

    print_group("ADMIN", admin)

    print_group("LOGIN", login)

    print_group("UPLOAD", upload)

    print_group("CONFIG", config)

    print_group("API", api)

def _print_page_overview(
    pages: list[Page],
) -> None:
    """
    Print a concise overview instead of every page.
    """

    from collections import Counter

    status_counter = Counter()

    forms = 0
    parameters = 0
    emails = 0
    apis = 0

    for page in pages:

        status_counter[page.status] += 1

        if page.forms:
            forms += 1

        if page.parameters:
            parameters += 1

        if page.emails:
            emails += 1

        if page.api_endpoints:
            apis += 1

    _print_header("PAGE OVERVIEW")

    print("Status Codes")

    print("-" * 60)

    for status, count in sorted(status_counter.items()):

        print(f"{status:<5} {count}")

    print()

    print(f"Pages with Forms      : {forms}")
    print(f"Pages with Parameters : {parameters}")
    print(f"Pages with Emails     : {emails}")
    print(f"Pages with APIs       : {apis}")

def _print_next_steps(
    pages: list[Page],
) -> None:
    """
    Recommend the next recon steps based on crawl findings.
    """

    login = set()
    admin = set()
    upload = set()
    apis = set()
    parameters = set()
    files = set()

    for page in pages:

        for link in page.links:

            lowered = link.url.lower()

            if "login" in lowered or "signin" in lowered:
                login.add(link.url)

            if "admin" in lowered:
                admin.add(link.url)

            if "upload" in lowered:
                upload.add(link.url)

        for endpoint in page.api_endpoints:
            apis.add(endpoint)

        for parameter in page.parameters:
            parameters.add(parameter.name)

        for file in page.interesting_files:
            files.add(file)

    _print_header("RECOMMENDED NEXT STEPS")

    if parameters:

        print("🎯 Test Parameters")

        for parameter in sorted(parameters):
            print(f"   • {parameter}")

        print()

    if login or admin:

        print("🔐 Review Authentication")

        for url in sorted(login):
            print(f"   • {url}")

        for url in sorted(admin):
            print(f"   • {url}")

        print()

    if upload:

        print("📤 Test Upload Functionality")

        for url in sorted(upload):
            print(f"   • {url}")

        print()

    if apis:

        print("🌐 Review API Endpoints")

        for api in sorted(apis):
            print(f"   • {api}")

        print()

    if files:

        print("📁 Inspect Interesting Files")

        for file in sorted(files):
            print(f"   • {file}")

        print()

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

    _print_header("CRAWLER RESULTS")

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

    _print_summary(
        pages,
        statistics,
    )

    _print_high_priority(
        pages,
        statistics,
    )

    _print_page_overview(
        pages,
    )
    _print_next_steps(
        pages,
    )
    #
    # If this looks like a JS-rendered app (Next.js, React, Vue...)
    # and we found zero forms, that's very likely because forms are
    # mounted client-side after the page loads - a plain HTTP fetch
    # never sees them, rather than the site genuinely having none.
    # Worth saying explicitly instead of silently showing "0".
    #

    js_framework_markers = (
        "_next/static",
        "/static/js/react",
        "vue.runtime",
        "__nuxt",
    )

    looks_js_rendered = any(
        marker in script.url
        for page in pages
        for script in page.scripts
        for marker in js_framework_markers
    )

    if looks_js_rendered and total_forms == 0:

        print(
            "Note: this site appears to be JavaScript-rendered "
            "(e.g. Next.js/React). Forms mounted client-side after "
            "the page loads won't appear in this scan - 0 forms "
            "found here does not necessarily mean the site has none."
        )


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

    #
    # Notable pages: non-200 status, an admin/suspicious-looking
    # path, or a page that actually has a form/email on it. Shown
    # first and separately, so they aren't buried among dozens of
    # ordinary pages further down.
    #

    notable_pages = [
        page
        for page in pages
        if page.status != 200
        or CrawlParser._is_notable(page.url)
        or page.forms
        or page.emails
    ]

    if notable_pages:

        print("Notable Pages")
        print("-" * 60)

        for page in notable_pages:

            tags = []

            if page.status != 200:
                tags.append(f"status {page.status}")

            if CrawlParser._is_notable(page.url):
                tags.append("suspicious path")

            if page.forms:
                tags.append(f"{len(page.forms)} form(s)")

            if page.emails:
                tags.append(f"{len(page.emails)} email(s)")

            print(f"  [{page.status}] {page.url}")
            print(f"      {page.title or '(no title)'} — {', '.join(tags)}")

        print()

    #
    # Full page list: group pages that share an identical
    # title/link/script/form/iframe "shape" - a common pattern on
    # sites where a soft-404 or template page (e.g. WordPress'
    # "Post Not Found") gets served for many different URLs. These
    # are collapsed into a single entry with all matching URLs
    # listed underneath, instead of repeating the same stat block
    # once per page.
    #

    groups: dict[tuple, list[Page]] = {}

    for page in pages:

        signature = (
            page.title,
            len(page.links),
            len(page.scripts),
            len(page.forms),
            len(page.iframes),
        )

        groups.setdefault(signature, []).append(page)

    print("Pages")
    print("-" * 60)

    for signature, group_pages in groups.items():

        title, n_links, n_scripts, n_forms, n_iframes = signature

        representative = group_pages[0]

        if len(group_pages) == 1:

            print(f"[{representative.status}] {representative.url}")

        else:

            print(
                f"{len(group_pages)} pages with identical structure "
                f"(same title/link/script/form/iframe counts):"
            )

            for page in group_pages:

                print(f"    [{page.status}] {page.url}")

        if title:

            print(f"    Title   : {title}")

        print(f"    Links   : {n_links}")
        print(f"    Scripts : {n_scripts}")
        print(f"    Forms   : {n_forms}")

        if n_iframes:
            print(f"    Iframes : {n_iframes}")

        print()