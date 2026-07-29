"""
Crawler Tool

Recursively crawls a website and extracts useful resources.
"""

from __future__ import annotations

from typing import Any

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator

from modules.web_enumeration.tools.crawler_lib.engine import engine
from modules.web_enumeration.tools.crawler_lib.formatter import print_results
from modules.web_enumeration.tools.crawler_lib.models import CrawlConfig


class CrawlerTool(BaseTool):
    """
    Website crawler.
    """

    def __init__(self) -> None:

        super().__init__(
            "Crawler",
        )

    # ---------------------------------------------------------

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Crawl a website.
        """

        self.start(
            silent,
        )

        if target is None:

            target = validator.get_domain()

        target = target.strip()

        if not target.startswith(
            (
                "http://",
                "https://",
            )
        ):

            target = "https://" + target

        logger.info(
            f"Crawling {target}"
        )

        config = CrawlConfig(

            url=target,

        )

        pages, statistics = engine.crawl(
            config,
        )

        if display:

            print_results(
                pages,
                statistics,
            )

        self.finish(
            silent,
        )

        return [

            {

                "url": page.url,

                "status": page.status,

                "title": page.title,

                "depth": page.depth,

                "links": len(page.links),

                "scripts": len(page.scripts),

                "forms": len(page.forms),

            }

            for page in pages

        ]


crawler = CrawlerTool()