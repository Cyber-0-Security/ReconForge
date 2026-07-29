"""
Response Filters

Applies all filtering logic to scan results.
"""

from __future__ import annotations

from .models import (
    ScanConfig,
    ScanResult,
)


class ResponseFilter:
    """
    Filters directory enumeration results.
    """

    def is_valid(
        self,
        result: ScanResult,
        config: ScanConfig,
    ) -> bool:
        """
        Determine whether a response should be shown.
        """

        if not self._status_allowed(
            result.status,
            config,
        ):
            return False

        return True

    # ---------------------------------------------------------

    def _status_allowed(
        self,
        status: int,
        config: ScanConfig,
    ) -> bool:
        """
        Check status-code filters.
        """

        if config.include_status:

            if status not in config.include_status:

                return False

        if config.exclude_status:

            if status in config.exclude_status:

                return False

        return True


filters = ResponseFilter()