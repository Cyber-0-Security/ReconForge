"""
core/banner.py

Display the ReconForge startup banner.

This module is responsible only for rendering the application's
banner and basic startup information. Keeping it separate from the
rest of the application makes it easy to change the appearance
without affecting any business logic.
"""

from config.constants import (
    APP_AUTHOR,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    BANNER,
    Colors,
)

from core.utils import clear_screen, separator


def display_banner() -> None:
    """
    Clear the terminal and display the application banner.
    """

    clear_screen()

    print(f"{Colors.CYAN}{BANNER}{Colors.RESET}")

    print(
        f"{Colors.BOLD}{APP_NAME}{Colors.RESET} "
        f"v{APP_VERSION}"
    )

    print(f"Author      : {APP_AUTHOR}")
    print(f"Description : {APP_DESCRIPTION}")

    print(separator())