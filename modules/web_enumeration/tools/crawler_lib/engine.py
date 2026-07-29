"""
Crawler Engine

Coordinates the crawling process.
"""

from __future__ import annotations

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

        while not queue.empty():

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

            # ---------------------------------------------

            for link in page.links:

                valid, reason = filters.is_valid(

                    link,

                    config,

                )

                if not valid:

                    statistics.invalid_skipped += 1

                    # Debug output (temporary)
                    print(f"[SKIP:{reason}] {link.url}")

                    continue

                parsed = urlparse(

                    link.url,

                )

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