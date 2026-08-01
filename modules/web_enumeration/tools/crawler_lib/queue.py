"""
Crawler Queue

Manages crawl targets and prevents duplicate crawling.
"""

from __future__ import annotations

from collections import deque
from urllib.parse import (
    parse_qsl,
    urlencode,
    urlparse,
    urlunparse,
)

from .models import CrawlTarget


class CrawlQueue:
    """
    FIFO queue for crawl targets.
    """

    TRACKING_PARAMS = {
        "fbclid",
        "gclid",
        "msclkid",
        "mc_cid",
        "mc_eid",
    }

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

        url = self._normalize(target.url)

        if url in self._visited:
            return False

        self._visited.add(url)

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

        return len(self._queue) == 0

    # ---------------------------------------------------------

    def size(
        self,
    ) -> int:
        """
        Number of pending targets.
        """

        return len(self._queue)

    # ---------------------------------------------------------

    def visited_count(
        self,
    ) -> int:
        """
        Number of discovered URLs.
        """

        return len(self._visited)

    # ---------------------------------------------------------

    @classmethod
    def _normalize(
        cls,
        url: str,
    ) -> str:
        """
        Normalize URLs for duplicate detection.

        This function intentionally performs only safe
        canonicalization. It never changes the meaning
        of a URL.
        """

        parsed = urlparse(url)

        scheme = parsed.scheme.lower()

        hostname = parsed.hostname.lower() if parsed.hostname else ""

        port = parsed.port

        if (
            (scheme == "http" and port == 80)
            or
            (scheme == "https" and port == 443)
        ):
            port = None

        netloc = hostname

        if port:
            netloc = f"{hostname}:{port}"

        path = parsed.path or "/"

        if path != "/":
            path = path.rstrip("/")

        query = []

        for key, value in parse_qsl(
            parsed.query,
            keep_blank_values=False,
        ):

            key_lower = key.lower()

            if key_lower.startswith("utm_"):
                continue

            if key_lower in cls.TRACKING_PARAMS:
                continue

            query.append((key, value))

        query_string = urlencode(query)

        return urlunparse(
            (
                scheme,
                netloc,
                path,
                "",
                query_string,
                "",
            )
        )


queue = CrawlQueue()