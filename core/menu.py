"""
core/menu.py

Interactive menu system for ReconForge.

Responsibilities
----------------
- Display the main menu.
- Read and validate user input.
- Route valid selections to the Runner.
- Continue running until the user exits.
"""

from __future__ import annotations

from config.constants import (
    APP_NAME,
    MENU_OPTIONS,
    Colors,
)

from core.banner import display_banner
from core.logger import logger
from core.runner import runner
from core.utils import (
    separator,
    wait_for_enter,
)


class Menu:
    """
    Interactive command-line menu.

    The menu never executes modules directly.
    It only determines what the user selected
    and delegates execution to the Runner.
    """

    def __init__(self) -> None:
        """Initialize the menu."""

        self.running = True

    def display(self) -> None:
        """
        Display the application banner
        followed by the available menu options.
        """

        display_banner()

        print(f"{Colors.BOLD}Main Menu{Colors.RESET}")
        print(separator())

        for index, (title, _) in enumerate(
            MENU_OPTIONS,
            start=1,
        ):
            print(f"{index}. {title}")

        print("\n0. Exit")
        print(separator())

    def get_choice(self) -> int:
        """
        Read the user's menu selection.

        Returns
        -------
        int
            Valid menu number.
        """

        while True:

            try:

                choice = int(
                    input(
                        f"{Colors.CYAN}Select an option: {Colors.RESET}"
                    )
                )

                if 0 <= choice <= len(MENU_OPTIONS):
                    return choice

                print(
                    f"{Colors.RED}"
                    "Invalid menu option."
                    f"{Colors.RESET}"
                )

            except ValueError:

                print(
                    f"{Colors.RED}"
                    "Please enter a number."
                    f"{Colors.RESET}"
                )

    def process_choice(self, choice: int) -> None:
        """
        Process the user's menu selection.
        """

        if choice == 0:

            logger.info("Exiting ReconForge...")

            self.running = False

            return

        module_key = MENU_OPTIONS[choice - 1][1]

        logger.info(f"Selected module: {module_key}")

        success = runner.run(module_key)

        if success:

            logger.success("Module execution completed.")

        else:

            logger.error("Module execution failed.")

        wait_for_enter()

    def start(self) -> None:
        """
        Start the interactive menu loop.
        """

        logger.info("Starting ReconForge menu.")

        while self.running:

            self.display()

            choice = self.get_choice()

            self.process_choice(choice)

        print(
            f"\n{Colors.GREEN}"
            f"Thank you for using {APP_NAME}!"
            f"{Colors.RESET}"
        )


menu = Menu()