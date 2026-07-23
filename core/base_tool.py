"""
core/base_tool.py

Shared base class for all ReconForge tools.

Every tool (WHOIS, Nmap, Subfinder, Nuclei, etc.)
inherits from this class to obtain common functionality.

Responsibilities
----------------
- Store tool metadata
- Record execution time
- Log tool lifecycle
- Define the interface every tool must implement
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from core.logger import logger


class BaseTool(ABC):
    """
    Abstract base class for every ReconForge tool.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize common tool attributes.
        """

        self.name = name
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None

    @abstractmethod
    def run(self) -> None:
        """
        Execute the tool.

        Every child class MUST implement this method.
        """
        pass

    def start(self) -> None:
        """
        Record the start time and log execution.
        """

        self.start_time = datetime.now()

        logger.info(f"Starting {self.name}...")

    def finish(self) -> None:
        """
        Record completion time and log duration.
        """

        self.end_time = datetime.now()

        duration = self.end_time - self.start_time

        logger.success(
            f"{self.name} completed in {duration}"
        )