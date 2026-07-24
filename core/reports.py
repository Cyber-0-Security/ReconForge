"""
core/report.py

Central report object used by ReconForge.

Every tool can add its results here.

Later this class will support exporting to:
    - JSON
    - HTML
    - PDF
"""

from __future__ import annotations

from typing import Any


class Report:
    """
    Store results collected during a scan.
    """

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

    def display(self) -> None:
        """
        Display all collected sections.
        """

        if not self._sections:

            print("No report data available.")

            return

        print("\n" + "=" * 60)
        print("RECON REPORT")
        print("=" * 60)

        for title, data in self._sections.items():

            print(f"\n[{title}]")

            if isinstance(data, dict):

                for key, value in data.items():

                    print(f"{key:<20}: {value}")

            elif isinstance(data, list):

                for item in data:

                    print(f"- {item}")

            else:

                print(data)

        print()

report = Report()