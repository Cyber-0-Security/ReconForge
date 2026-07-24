"""
core/formatter.py

Utility functions for formatting ReconForge output.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class Formatter:
    """
    Helper class for formatting data returned
    by reconnaissance tools.
    """

    @staticmethod
    def format_value(value: Any) -> Any:
        """
        Format a value for display.
        """

        if value is None:
            return "N/A"

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")

        if isinstance(value, list):

            cleaned = []

            for item in value:

                item = Formatter.format_value(item)

                if item not in cleaned:
                    cleaned.append(item)

            return cleaned

        return value

    @staticmethod
    def first(value: Any) -> Any:
        """
        Return the first element of a list.
        """

        value = Formatter.format_value(value)

        if isinstance(value, list):

            if value:
                return value[0]

            return "N/A"

        return value