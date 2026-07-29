"""
Crawler Queue

Manages crawl targets and prevents duplicate crawling.
"""

from __future__ import annotations

from collections import deque

from .models import CrawlTarget


class CrawlQueue:
    """
    FIFO queue for crawl targets.
    """

    def __init__(self) -> None:

        self._queue: deque[CrawlTarget] = deque()

        self._visited: set[str] = set()

    # ---------------------------------------------------------

    def add(
        self,
        target: CrawlTarget,
    ) -> bool:
        """
        Add a new crawl target.

        Returns True if added.
        Returns False if already visited.
        """

        url = self._normalize(
            target.url,
        )

        if url in self._visited:

            return False

        self._visited.add(
            url,
        )

        self._queue.append(
            CrawlTarget(
                url=url,
                depth=target.depth,
            )
        )

        return True

    # ---------------------------------------------------------

    def get(
        self,
    ) -> CrawlTarget | None:
        """
        Get the next crawl target.
        """

        if not self._queue:

            return None

        return self._queue.popleft()

    # ---------------------------------------------------------

    def empty(
        self,
    ) -> bool:
        """
        True if the queue is empty.
        """

        return len(
            self._queue
        ) == 0

    # ---------------------------------------------------------

    def size(
        self,
    ) -> int:
        """
        Number of pending targets.
        """

        return len(
            self._queue
        )

    # ---------------------------------------------------------

    def visited_count(
        self,
    ) -> int:
        """
        Number of discovered URLs.
        """

        return len(
            self._visited
        )

    # ---------------------------------------------------------

    @staticmethod
    def _normalize(
        url: str,
    ) -> str:
        """
        Normalize URLs for duplicate detection.
        """

        return url.rstrip("/")


queue = CrawlQueue()