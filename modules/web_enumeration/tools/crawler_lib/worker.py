"""
Crawler Worker

Processes a single crawl target.
"""

from __future__ import annotations

from urllib.parse import urlparse

from .filters import filters
from .logger import logger
from .models import (
    CrawlConfig,
    CrawlTarget,
    Page,
)
from .normalizer import normalizer
from .parser import parser
from .requester import requester


class CrawlWorker:
    """
    Worker responsible for crawling one page.
    """

    def process(
        self,
        target: CrawlTarget,
        config: CrawlConfig,
    ) -> tuple[Page | None, list[CrawlTarget]]:

        logger.verbose(f"[{target.depth}] {target.url}")

        response = requester.get(
            url=target.url,
            timeout=config.timeout,
            follow_redirects=config.follow_redirects,
            verify_ssl=config.verify_ssl,
            user_agent=config.user_agent,
        )

        if response is None:

            logger.error(
                f"Failed request: {target.url}"
            )

            return None, []

        try:

            page = parser.parse(
                response,
                target,
            )

        except Exception as exc:

            import traceback

            traceback.print_exc()

            logger.error(
                f"Parser crashed on {target.url}"
            )

            return None, []

        logger.debug(
            f"{page.status} {page.url}"
        )

        discovered: list[CrawlTarget] = []

        current_host = urlparse(config.url).hostname or ""

        for link in page.links:

            url = normalizer.normalize(link.url)

            if not url:
                continue

            if filters.is_static(url):
                continue

            if filters.is_invalid(url):
                continue

            if not filters.is_same_scope(
                url=url,
                root=current_host,
                include_subdomains=config.include_subdomains,
            ):
                continue

            discovered.append(
                CrawlTarget(
                    url=url,
                    depth=target.depth + 1,
                )
            )

        return (
            page,
            discovered,
        )


worker = CrawlWorker()