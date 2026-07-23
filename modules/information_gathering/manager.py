"""
modules/information_gathering/manager.py

Information Gathering module manager.

Responsibilities
----------------
- Display the Information Gathering submenu.
- Route user selections to the appropriate tool.
- Never implement reconnaissance logic directly.
"""

from __future__ import annotations

from core.logger import logger
from core.utils import separator, wait_for_enter
from config.constants import Colors

from modules.information_gathering.tools.dns_lookup import DNSLookupTool
from modules.information_gathering.tools.whois import WhoisTool


TOOLS = [
    ("WHOIS Lookup", WhoisTool),
    ("DNS Lookup", DNSLookupTool),
]


class InformationGatheringManager:
    """
    Handles the Information Gathering submenu.
    """

    def __init__(self) -> None:

        self.running = True

    def display_menu(self) -> None:
        """
        Display the Information Gathering submenu.
        """

        print()
        print(separator())
        print(f"{Colors.BOLD}Information Gathering{Colors.RESET}")
        print(separator())

        for index, (name, _) in enumerate(TOOLS, start=1):
            print(f"{index}. {name}")

        print("\n0. Back")
        print(separator())

    def get_choice(self) -> int:
        """
        Read a valid submenu option.
        """

        while True:

            try:

                choice = int(
                    input(
                        f"{Colors.CYAN}Select an option: {Colors.RESET}"
                    )
                )

                if 0 <= choice <= len(TOOLS):
                    return choice

                print(
                    f"{Colors.RED}"
                    "Invalid option."
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
        Execute the selected tool.
        """

        if choice == 0:

            self.running = False

            return

        tool_class = TOOLS[choice - 1][1]

        logger.info(f"Executing {tool_class.__name__}")

        tool = tool_class()

        tool.run()

        wait_for_enter()

    def execute(self) -> None:
        """
        Start the submenu loop.
        """

        self.running = True

        while self.running:

            self.display_menu()

            choice = self.get_choice()

            self.process_choice(choice)


manager = InformationGatheringManager()


def execute() -> None:
    """
    Entry point called by the Runner.
    """

    manager.execute()