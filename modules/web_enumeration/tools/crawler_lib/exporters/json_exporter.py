"""
Crawler JSON Exporter

Exports crawler results to JSON.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..models import (
    CrawlStatistics,
    Page,
)


class JsonExporter:
    """
    Export crawl results to JSON.
    """

    def export(
        self,
        target: str,
        pages: list[Page],
        statistics: CrawlStatistics,
    ) -> str:
        """
        Export crawl results.

        Returns the output file path.
        """

        output_dir = Path(
            "output/crawler"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            target.replace(
                "https://",
                "",
            )
            .replace(
                "http://",
                "",
            )
            .replace(
                "/",
                "_",
            )
        )

        output_file = (
            output_dir /
            f"{filename}.json"
        )

        report = {

            "target": target,

            "statistics": asdict(
                statistics,
            ),

            "pages": [

                asdict(page)

                for page in pages

            ],

        }

        with output_file.open(

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                report,

                fp,

                indent=4,

                ensure_ascii=False,

            )

        return str(output_file)


json_exporter = JsonExporter()