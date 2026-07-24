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
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4


class Report:
    """
    Store and display scan results.
    """

    WIDTH = 70

    def __init__(self) -> None:

        self._sections: dict[str, Any] = {}
        self.generated_at = datetime.now()
        self.report_id = str(uuid4())

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
        Display all collected sections.
        """

        if not self._sections:

            print("No report data available.")

            return

        print("\n" + "=" * 70)
        print("RECONFORGE REPORT")
        print("=" * 70)
        print(f"Generated : {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        for section, data in self._sections.items():

            print(f"\n[{section}]")
            print("-" * 70)

            if isinstance(data, dict):

                for key, value in data.items():

                    if isinstance(value, list):

                        if not value:

                            print(f"{key:<20}: N/A")

                        else:

                            print(f"{key:<20}: {value[0]}")

                            for item in value[1:]:

                                print(f"{'':<20}  {item}")

                    else:

                        print(f"{key:<20}: {value}")

            else:

                print(data)

        print("\n" + "=" * 70)
    def export_json(self) -> None:
        """
        Export report as JSON.
        """

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        filename = (f"recon_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json")

        output = reports_dir / filename

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                {
                    "report_id": self.report_id,
                    "generated_at": self.generated_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "sections": self._sections,
                },
                file,
                indent=4,
                default=str,
            )

        print(f"\nReport saved to: {output}")
report = Report()