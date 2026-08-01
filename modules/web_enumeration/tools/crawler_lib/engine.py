"""
Crawler Engine

Coordinates the crawling process.
"""

from __future__ import annotations

import time
from urllib.parse import urlparse

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


class CrawlEngine:
    """
    Main crawler engine.
    """

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

        if queue.add(

            CrawlTarget(

                url=config.url,

                depth=0,

            )

        ):

            statistics.urls_queued += 1

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

                if queue.add(

                    CrawlTarget(

                        url=config.url.rstrip("/") + path,

                        depth=1,

                    )

                ):

                    statistics.urls_queued += 1

                else:

                    statistics.duplicates_skipped += 1

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

                if queue.add(

                    CrawlTarget(

                        url=url,

                        depth=1,

                    )

                ):

                    statistics.urls_queued += 1

                else:

                    statistics.duplicates_skipped += 1

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

            if response is None:

                continue

            page = parser.parse(

                response,

                target,

            )

            results.append(page)

            statistics.pages_crawled += 1

            statistics.links_discovered += len(page.links)

            print(
                f"    [{statistics.pages_crawled}/{config.max_pages}] "
                f"[{page.status}] {page.url} "
                f"({len(page.links)} links, queue: {queue.size()})"
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

                parsed = urlparse(

                    link.url,

                )

                queued_from_page += 1

                if queue.add(

                    CrawlTarget(

                        url=parsed.geturl(),

                        depth=target.depth + 1,

                    )

                ):

                    statistics.urls_queued += 1

                else:

                    statistics.duplicates_skipped += 1

        return (

            results,

            statistics,

        )


engine = CrawlEngine()