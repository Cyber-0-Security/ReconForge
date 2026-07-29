"""
Worker

Processes a single scan target.
"""

from __future__ import annotations

from .filters import filters
from .models import (
    ScanConfig,
    ScanResult,
    ScanTarget,
    WildcardSignature,
)
from .requester import requester


class ScanWorker:
    """
    Processes a single ScanTarget.
    """

    def process(
        self,
        target: ScanTarget,
        config: ScanConfig,
        wildcard: WildcardSignature | None = None,
    ) -> ScanResult | None:
        """
        Scan a single target.
        """

        result = requester.request(
            target,
            config,
        )

        if result is None:
            return None

        # Ignore wildcard responses
        if (
            wildcard is not None
            and result.status == wildcard.status
            and result.length == wildcard.length
            and result.words == wildcard.words
            and result.lines == wildcard.lines
        ):
            return None

        if not filters.is_valid(
            result,
            config,
        ):
            return None

        return result


worker = ScanWorker()