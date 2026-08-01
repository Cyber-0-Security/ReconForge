"""
Crawler Queue

Thread-safe crawl queue.
"""

from __future__ import annotations

from queue import Empty, Queue

from .models import CrawlTarget


class CrawlQueue:
    """
    Thread-safe crawl queue.
    """

    def __init__(self) -> None:

        self._queue: Queue[CrawlTarget] = Queue()

        self._visited: set[str] = set()

    # ---------------------------------------------------------

    def add(
        self,
        target: CrawlTarget,
    ) -> bool:
        """
        Add a new target if it hasn't been visited.
        """

        if target.url in self._visited:
            return False

        self._visited.add(target.url)

        self._queue.put(target)

        return True

    # ---------------------------------------------------------

    def get(
        self,
    ) -> CrawlTarget | None:
        """
        Get next target.
        """

        try:

            return self._queue.get_nowait()

        except Empty:

            return None

    # ---------------------------------------------------------

    def task_done(
        self,
    ) -> None:
        """
        Mark a task complete.
        """

        self._queue.task_done()

    # ---------------------------------------------------------

    def join(
        self,
    ) -> None:
        """
        Wait until queue finishes.
        """

        self._queue.join()

    # ---------------------------------------------------------

    def empty(
        self,
    ) -> bool:

        return self._queue.empty()

    # ---------------------------------------------------------

    @property
    def visited(
        self,
    ) -> set[str]:

        return self._visited