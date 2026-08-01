"""
Crawler Logger

Handles crawler logging with verbosity levels.
"""

from __future__ import annotations

from config.constants import Colors


class CrawlLogger:
    """
    Lightweight logger for the crawler.
    """

    LEVELS = (
        "quiet",
        "normal",
        "verbose",
        "debug",
    )

    def __init__(self) -> None:

        self.level = "normal"

    # ---------------------------------------------------------

    def configure(
        self,
        level: str,
    ) -> None:

        level = level.lower()

        if level not in self.LEVELS:
            level = "normal"

        self.level = level

    # ---------------------------------------------------------

    def info(
        self,
        message: str,
    ) -> None:

        if self.level != "quiet":

            print(
                f"{Colors.CYAN}[INFO]{Colors.RESET} {message}"
            )

    # ---------------------------------------------------------

    def success(
        self,
        message: str,
    ) -> None:

        if self.level != "quiet":

            print(
                f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}"
            )

    # ---------------------------------------------------------

    def warning(
        self,
        message: str,
    ) -> None:

        if self.level != "quiet":

            print(
                f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}"
            )

    # ---------------------------------------------------------

    def error(
        self,
        message: str,
    ) -> None:

        print(
            f"{Colors.RED}[ERROR]{Colors.RESET} {message}"
        )

    # ---------------------------------------------------------

    def verbose(
        self,
        message: str,
    ) -> None:

        if self.level in (
            "verbose",
            "debug",
        ):

            print(message)

    # ---------------------------------------------------------

    def debug(
        self,
        message: str,
    ) -> None:

        if self.level == "debug":

            print(
                f"{Colors.MAGENTA}[DEBUG]{Colors.RESET} {message}"
            )


logger = CrawlLogger()