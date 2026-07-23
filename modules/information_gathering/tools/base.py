"""
modules/information_gathering/tools/base.py

Base class for all Information Gathering tools.

Every tool should inherit from BaseTool and implement
its own run() method.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from core.logger import logger


class BaseTool(ABC):
    """
    Abstract base class for every reconnaissance tool.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize common tool attributes.
        """

        self.name = name
        self.start_time = None
        self.end_time = None

    @abstractmethod
    def run(self) -> None:
        """
        Execute the tool.

        Every child class MUST implement this method.
        """
        pass

    def start(self) -> None:
        """
        Record tool start time.
        """

        self.start_time = datetime.now()

        logger.info(f"Starting {self.name}")

    def finish(self) -> None:
        """
        Record tool completion time.
        """

        self.end_time = datetime.now()

        duration = self.end_time - self.start_time

        logger.success(
            f"{self.name} completed in {duration}"
        )