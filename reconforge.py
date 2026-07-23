"""
reconforge.py

Entry point for ReconForge.

Responsibilities
----------------
- Load configuration
- Display banner
- Start the main application loop
"""

from __future__ import annotations

from core.logger import logger
from core.menu import menu


def main() -> None:
    """
    Start the ReconForge application.
    """

    logger.info("Starting ReconForge")

    menu.start()

    logger.info("ReconForge terminated")


if __name__ == "__main__":
    main()