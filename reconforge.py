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

from core.banner import display_banner
from core.logger import logger
from core.runner import Runner


def main() -> None:
    """
    Start the ReconForge application.
    """

    logger.info("Starting ReconForge")

    display_banner()

    runner = Runner()

    runner.start()

    logger.info("ReconForge terminated")


if __name__ == "__main__":
    main()