"""
Crawler Progress

Simple terminal progress bar.
"""

from __future__ import annotations

import shutil


class CrawlProgress:
    """
    Displays crawler progress.
    """

    BAR_WIDTH = 30

    @classmethod
    def update(
        cls,
        current: int,
        total: int,
        url: str,
        status: int,
    ) -> None:

        if total <= 0:
            total = 1

        ratio = min(current / total, 1.0)

        filled = int(cls.BAR_WIDTH * ratio)

        bar = (
            "█" * filled
            + "░" * (cls.BAR_WIDTH - filled)
        )

        width = shutil.get_terminal_size(
            fallback=(120, 20)
        ).columns

        line = (
            f"\r[{bar}] "
            f"{current}/{total} "
            f"{status} "
            f"{url}"
        )

        print(
            line[: width - 1],
            end="",
            flush=True,
        )

    @staticmethod
    def finish() -> None:
        print()