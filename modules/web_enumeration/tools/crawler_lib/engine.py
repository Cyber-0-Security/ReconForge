"""
Crawler Engine

Coordinates the crawling process using worker threads.
"""

from __future__ import annotations

import sys
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime

from .logger import logger
from .models import (
    CrawlConfig,
    CrawlStatistics,
    CrawlTarget,
    Page,
)
from .queue import CrawlQueue
from .robots import robots
from .sitemap import sitemap
from .worker import worker


class CrawlEngine:
    """
    Main crawler engine.
    """

    def _progress(
        self,
        statistics: CrawlStatistics,
        queue: CrawlQueue,
        futures: dict,
        start: datetime,
        verbosity: str,
    ) -> None:

        if verbosity != "normal":
            return

        elapsed = datetime.now() - start

        line = (
            f"\rPages: {statistics.pages_crawled:<6}"
            f" Queue: {queue.qsize():<6}"
            f" Active: {len(futures):<3}"
            f" Found: {statistics.links_discovered:<6}"
            f" Time: {str(elapsed).split('.')[0]}"
        )

        sys.stdout.write(line)
        sys.stdout.flush()

    # ---------------------------------------------------------

    def crawl(
        self,
        config: CrawlConfig,
    ) -> tuple[list[Page], CrawlStatistics]:

        start = datetime.now()

        queue = CrawlQueue()

        statistics = CrawlStatistics()

        pages: list[Page] = []

        logger.configure(config.verbosity)

        logger.info(f"Starting crawl: {config.url}")

        # -------------------------------------------------
        # Seed
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

        logger.info("Fetching robots.txt...")

        robots_content = robots.fetch(
            config.url,
            timeout=config.timeout,
            verify_ssl=config.verify_ssl,
        )

        if robots_content:

            robot_urls = robots.parse(robots_content)

            logger.info(
                f"robots.txt: {len(robot_urls)} entries"
            )

            for path in robot_urls:

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

        logger.info("Fetching sitemap.xml...")

        sitemap_content = sitemap.fetch(
            config.url,
            timeout=config.timeout,
            verify_ssl=config.verify_ssl,
        )

        if sitemap_content:

            sitemap_urls = sitemap.parse(
                sitemap_content
            )

            logger.info(
                f"Sitemap: {len(sitemap_urls)} URLs"
            )

            for url in sitemap_urls:

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
        # Thread Pool
        # -------------------------------------------------

        with ThreadPoolExecutor(
            max_workers=config.threads,
        ) as executor:

            futures = {}

            while not queue.empty() or futures:

                while (
                    len(futures) < config.threads
                    and not queue.empty()
                ):

                    target = queue.get()

                    if target is None:
                        break

                    if target.depth > config.max_depth:

                        queue.task_done()

                        continue

                    future = executor.submit(
                        worker.process,
                        target,
                        config,
                    )

                    futures[future] = target

                if not futures:
                    continue

                done, _ = wait(
                    futures,
                    return_when=FIRST_COMPLETED,
                )

                for future in done:

                    target = futures.pop(future)

                    try:

                        page, discovered = future.result()

                    except Exception as exc:

                        logger.debug(
                            f"Worker failed: {target.url}: {exc}"
                        )

                        queue.task_done()

                        continue

                    if page:

                        pages.append(page)

                        statistics.pages_crawled += 1

                        statistics.links_discovered += len(
                            page.links
                        )

                    for new_target in discovered:

                        if queue.add(new_target):

                            statistics.urls_queued += 1

                        else:

                            statistics.duplicates_skipped += 1

                    queue.task_done()

                self._progress(
                    statistics,
                    queue,
                    futures,
                    start,
                    config.verbosity,
                )

        if config.verbosity == "normal":
            print()

        logger.success("Crawl finished")

        return (
            pages,
            statistics,
        )


engine = CrawlEngine()