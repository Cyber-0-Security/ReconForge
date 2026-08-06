"""
Crawler Engine

Coordinates the crawling process.
"""

from __future__ import annotations

import time

from .filters import filters
from .models import (
    CrawlConfig,
    CrawlStatistics,
    CrawlTarget,
    Page,
)
from .parser import parser
from .queue import CrawlQueue
from .requester import requester
from .robots import robots
from .sitemap import sitemap
from .progress import CrawlProgress

class CrawlEngine:
    """
    Main crawler engine.
    """
    # ---------------------------------------------------------

    @staticmethod
    def _enqueue_target(
        queue: CrawlQueue,
        statistics: CrawlStatistics,
        target: CrawlTarget,
    ) -> bool:
        """
        Queue a crawl target and update statistics.
        """

        added = queue.add(target)

        if added:
            statistics.urls_queued += 1
        else:
            statistics.duplicates_skipped += 1

        return added
    def crawl(
        self,
        config: CrawlConfig,
    ) -> tuple[list[Page], CrawlStatistics]:
        """
        Crawl a website.
        """

        queue = CrawlQueue()

        statistics = CrawlStatistics()

        results: list[Page] = []

        # -------------------------------------------------
        # Seed Queue
        # -------------------------------------------------

        self._enqueue_target(

            queue,

            statistics,

            CrawlTarget(

                url=config.url,

                depth=0,

            ),

        )

        # -------------------------------------------------
        # robots.txt
        # -------------------------------------------------

        robots_content = robots.fetch(

            config.url,

            timeout=config.timeout,

            verify_ssl=config.verify_ssl,

        )

        if robots_content:

            for path in robots.parse(
                robots_content,
            ):

                self._enqueue_target(

                queue,

                statistics,

                CrawlTarget(

                    url=config.url.rstrip("/") + path,

                    depth=1,

                ),

            )

        # -------------------------------------------------
        # sitemap.xml
        # -------------------------------------------------

        sitemap_content = sitemap.fetch(

            config.url,

            timeout=config.timeout,

            verify_ssl=config.verify_ssl,

        )

        if sitemap_content:

            for url in sitemap.parse(
                sitemap_content,
                timeout=config.timeout,
                verify_ssl=config.verify_ssl,
            ):

                self._enqueue_target(

                queue,

                statistics,

                CrawlTarget(

                    url=url,

                    depth=1,

                ),

            )

        # -------------------------------------------------
        # Crawl Loop
        # -------------------------------------------------

        start_time = time.monotonic()

        while not queue.empty():

            if statistics.pages_crawled >= config.max_pages:

                statistics.stop_reason = (
                    f"stopped: reached max_pages limit ({config.max_pages})"
                )

                break

            if time.monotonic() - start_time >= config.max_duration:

                statistics.stop_reason = (
                    f"stopped: reached max_duration limit ({config.max_duration}s)"
                )

                break

            target = queue.get()

            if target is None:

                break

            if target.depth > config.max_depth:

                continue

            response = requester.request(

                target,

                config,

            )

            if config.delay > 0:
                time.sleep(config.delay)

            if response is None:

                continue

            page = parser.parse(

                response,

                target,

            )

            results.append(page)

            statistics.pages_crawled += 1

            statistics.links_discovered += len(page.links)

            #
            # Deduplicate and record parameter-intelligence findings.
            #

            existing = {
                (p.name, p.source)
                for p in statistics.parameter_findings
            }

            for finding in page.parameters:

                key = (finding.name, finding.source)

                if key not in existing:

                    statistics.parameter_findings.append(finding)

                    existing.add(key)

                    icon = {
                        "HIGH": "🔴",
                        "MEDIUM": "🟡",
                        "LOW": "⚪",
                    }.get(finding.severity, "⚪")

                    print(
                        f"        {icon} [{finding.severity}] "
                        f"{finding.name} → {finding.category}"
                    )

            #
            # Everything below must run for every page regardless
            # of whether it had any parameter findings - previously
            # all of this (including link queueing!) was nested
            # inside the loop above, so a page with zero parameter
            # matches would never have any of its links followed.
            #

            statistics.parameters.update(
                parameter.name
                for parameter in page.parameters
            )

            statistics.api_endpoints.update(
                page.api_endpoints
            )
            statistics.javascript_endpoints.update(
                page.javascript_endpoints
            )
            statistics.emails.update(
                page.emails
            )

            statistics.interesting_files.update(
                page.interesting_files
            )

            statistics.technologies.update(
                page.technologies
            )

            CrawlProgress.update(
                current=statistics.pages_crawled,
                total=config.max_pages,
                url=page.url,
                status=page.status,
            )

            # ---------------------------------------------
            # Notable links (matching suspicious keywords like
            # admin/backup/.git/config/etc.) are always recorded
            # for the report, regardless of whether they end up
            # being crawled - so nothing interesting is silently
            # lost just because a page had thousands of routine
            # links ahead of it.
            # ---------------------------------------------

            for link in page.links:

                if link.notable:

                    statistics.notable_links.append(link.url)

            # Collect external domains discovered on this page.
            # These are useful later for reporting and OSINT.

            if page.external_domains:

                statistics.external_domains.update(
                    page.external_domains
                )

            # ---------------------------------------------
            # A single page can contain far more links than we
            # can reasonably crawl (pypi.org/simple/ has 861,000+).
            # Rather than just queuing whatever order they happened
            # to appear in the HTML, put notable-looking links
            # first so a capped crawl still prioritizes the things
            # most worth following.
            # ---------------------------------------------

            candidate_links = sorted(
                page.links,
                key=lambda link: not link.notable,
            )

            queued_from_page = 0

            if len(page.links) > config.max_links_to_queue_per_page:

                print(
                    f"        (page had {len(page.links)} links - "
                    f"only queuing top {config.max_links_to_queue_per_page}, "
                    "prioritizing notable ones; all still scanned above)"
                )

            for link in candidate_links:

                if queued_from_page >= config.max_links_to_queue_per_page:

                    break

                valid, reason = filters.is_valid(

                    link,

                    config,

                )

                if not valid:

                    statistics.invalid_skipped += 1

                    continue

                queued_from_page += 1

                self._enqueue_target(

                    queue,

                    statistics,

                    CrawlTarget(

                        url=link.url,

                        depth=target.depth + 1,

                    ),

                )
        CrawlProgress.finish()

        if not statistics.stop_reason:
            statistics.stop_reason = "crawl complete"

        return (
            results,
            statistics,
        )


engine = CrawlEngine()