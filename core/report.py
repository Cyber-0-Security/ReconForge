"""
core/report.py

Central report object used by ReconForge.

Stores reconnaissance results and renders
them in a clean CLI format.

Future versions can export to:
    - JSON
    - HTML
    - PDF
"""

from __future__ import annotations

from typing import Any

from config.constants import Colors


class Report:
    """
    Store and display scan results.
    """

    WIDTH = 70

    def __init__(self) -> None:

        self._sections: dict[str, Any] = {}

    def add_section(self, name: str, data: Any) -> None:
        """
        Add or replace a report section.
        """

        self._sections[name] = data

    def get_section(self, name: str) -> Any:
        """
        Return one report section.
        """

        return self._sections.get(name)

    def clear(self) -> None:
        """
        Remove all collected data.
        """

        self._sections.clear()

    @staticmethod
    def title(text: str) -> None:
        """
        Display a report title.
        """

        print()
        print("═" * Report.WIDTH)
        print(f"{Colors.BOLD}{text.center(Report.WIDTH)}{Colors.RESET}")
        print("═" * Report.WIDTH)

    @staticmethod
    def section(text: str) -> None:
        """
        Display a section heading.
        """

        print()
        print(f"{Colors.CYAN}{text}{Colors.RESET}")
        print("─" * Report.WIDTH)

    @staticmethod
    def field(name: str, value: Any) -> None:
        """
        Display one field.
        """

        if value is None:
            value = "N/A"

        print(f"{name:<20}: {value}")

    @staticmethod
    def list_field(name: str, values: Any) -> None:
        """
        Display a list neatly.
        """

        if not values:

            Report.field(name, "N/A")

            return

        if not isinstance(values, list):

            values = [values]

        Report.field(name, values[0])

        for item in values[1:]:

            print(f"{'':<20}  {item}")

    @staticmethod
    def success(message: str) -> None:
        """
        Display a success footer.
        """

        print()
        print("═" * Report.WIDTH)
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")
        print("═" * Report.WIDTH)

    def display(self) -> None:
        """
        Display every stored report section.
        """

        if not self._sections:

            print("No report data available.")

            return

        self.title("RECON REPORT")

        for title, data in self._sections.items():

            self.section(title)

            if isinstance(data, dict):

                for key, value in data.items():

                    if isinstance(value, list):

                        self.list_field(key, value)

                    else:

                        self.field(key, value)

            elif isinstance(data, list):

                self.list_field("Values", data)

            else:

                self.field("Value", data)

        self.success("Report Generated")


report = Report()