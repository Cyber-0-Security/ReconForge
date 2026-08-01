"""
Crawler Tool

ReconForge Web Crawler
"""

from __future__ import annotations

from datetime import datetime

from config.constants import Colors

from modules.web_enumeration.tools.crawler_lib.engine import engine
from modules.web_enumeration.tools.crawler_lib.formatter import formatter
from modules.web_enumeration.tools.crawler_lib.logger import logger
from modules.web_enumeration.tools.crawler_lib.models import CrawlConfig


class CrawlerTool:
    """
    Web crawler tool.
    """

    name = "Crawler"

    description = "Crawl a website and enumerate pages."

    def run(self) -> None:
        """
        Execute crawler.
        """

        print()
        print("=" * 60)
        print(f"{Colors.BOLD}WEB CRAWLER{Colors.RESET}")
        print("=" * 60)

        url = input("Target URL: ").strip()

        if not url:
            logger.error("No URL provided.")
            return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            depth = input("Maximum Depth [2]: ").strip()
            max_depth = int(depth) if depth else 2
        except ValueError:
            max_depth = 2

        try:
            threads = input("Threads [20]: ").strip()
            thread_count = int(threads) if threads else 20
        except ValueError:
            thread_count = 20

        verbosity = (
            input(
                "Verbosity "
                "[quiet/normal/verbose/debug] (normal): "
            )
            .strip()
            .lower()
        )

        if not verbosity:
            verbosity = "normal"

        config = CrawlConfig(
            url=url,
            max_depth=max_depth,
            threads=thread_count,
            verbosity=verbosity,
        )

        logger.configure(config.verbosity)

        print()

        logger.info(f"Target      : {config.url}")
        logger.info(f"Depth       : {config.max_depth}")
        logger.info(f"Threads     : {config.threads}")
        logger.info(f"Verbosity   : {config.verbosity}")

        print()

        logger.info("Starting crawler...")

        start = datetime.now()

        pages, statistics = engine.crawl(config)

        end = datetime.now()

        formatter.display(
            pages,
            statistics,
        )

        print()

        logger.success(
            f"Crawler completed in {end - start}"
        )