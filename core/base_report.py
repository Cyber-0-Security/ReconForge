"""
core/base_report.py

Base class for all report objects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseReport(ABC):
    """
    Base class for report objects.
    """

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Return report data as a dictionary.
        """
        pass