"""
Crawler CSV Exporter

Exports crawler results to CSV.
"""

from __future__ import annotations

import csv
from pathlib import Path

from ..models import Page


class CsvExporter:
    """
    Export crawl results to CSV.
    """

    def export(
        self,
        target: str,
        pages: list[Page],
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
            f"{filename}.csv"
        )

        with output_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:

            writer = csv.writer(fp)

            writer.writerow([
                "URL",
                "Status",
                "Title",
                "Depth",
                "Content Type",
                "Server",
                "Canonical",
                "Links",
                "Scripts",
                "Images",
                "CSS",
                "Iframes",
                "Forms",
            ])

            for page in pages:

                writer.writerow([
                    page.url,
                    page.status,
                    page.title,
                    page.depth,
                    page.content_type,
                    page.server,
                    page.canonical,
                    len(page.links),
                    len(page.scripts),
                    len(page.images),
                    len(page.stylesheets),
                    len(page.iframes),
                    len(page.forms),
                ])

        return str(output_file)


csv_exporter = CsvExporter()