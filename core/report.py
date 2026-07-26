"""
core/report.py

Report Generation Module – Enhanced with beautiful formatting,
timestamped JSON exports, smart truncation, and technology grouping.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

# ---- ANSI color codes (fallback) ----
class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class Report:
    def __init__(self) -> None:
        self._sections: list[tuple[str, Any]] = []

    def clear(self) -> None:
        self._sections = []

    def add_section(self, title: str, data: Any) -> None:
        self._sections.append((title, data))

    def display(self) -> None:
        """Print the entire report with beautiful formatting."""
        for title, data in self._sections:
            # Section header
            print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
            print(f"{Colors.BOLD}{title.upper()}{Colors.RESET}")
            print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")

            # ---- TECHNOLOGY DETECTION: group by category ----
            if (isinstance(data, list) and 
                all(isinstance(item, dict) and 'category' in item for item in data)):
                categorized = {}
                for item in data:
                    cat = item.get('category', 'Unknown')
                    categorized.setdefault(cat, []).append(item)
                for category, items in sorted(categorized.items()):
                    print(f"\n{category}")
                    print('-' * 40)
                    for item in items:
                        name = item.get('name', 'Unknown')
                        conf = item.get('confidence', 0)
                        ver = item.get('version')
                        if ver:
                            print(f"  • {name} {ver} (confidence: {conf}%)")
                        else:
                            print(f"  • {name} (confidence: {conf}%)")
                continue

            # ---- OTHER LISTS / DICTS ----
            if isinstance(data, dict):
                self._print_dict(data)
            elif isinstance(data, list):
                self._print_list(data, title)
            else:
                print(f"  {data}")

    def _print_dict(self, data: dict, indent: int = 0) -> None:
        """Print a dictionary with nice formatting."""
        prefix = "  " * indent
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{prefix}{Colors.CYAN}{key}:{Colors.RESET}")
                self._print_dict(value, indent + 1)
            elif isinstance(value, list):
                # If it's a list of simple values, print inline
                if all(not isinstance(v, (dict, list)) for v in value):
                    print(f"{prefix}{Colors.YELLOW}{key}:{Colors.RESET} {', '.join(str(v) for v in value)}")
                else:
                    print(f"{prefix}{Colors.CYAN}{key}:{Colors.RESET}")
                    for item in value:
                        if isinstance(item, dict):
                            self._print_dict(item, indent + 1)
                        else:
                            print(f"{'  ' * (indent+1)}• {item}")
            else:
                print(f"{prefix}{Colors.YELLOW}{key}:{Colors.RESET} {value}")

    def _print_list(self, data: list, title: str) -> None:
        """Print a list – show all subdomains, truncate other long lists."""
        total = len(data)
        if total == 0:
            print("  (none)")
            return

        # Show all subdomains
        if "SUBDOMAINS" in title.upper():
            for item in data:
                print(f"  • {item}")
            return

        # For other lists, truncate if too long
        if total > 15:
            for item in data[:10]:
                print(f"  • {item}")
            print(f"  {Colors.MAGENTA}... and {total - 10} more{Colors.RESET}")
        else:
            for item in data:
                print(f"  • {item}")

    def to_dict(self) -> dict[str, Any]:
        return dict(self._sections)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self._sections, indent=indent, default=str)

    def export_json(self, filename: str = None) -> None:
        """
        Export the report to a JSON file.
        If filename is not given, save to reports/report_<timestamp>.json.
        """
        if filename is None:
            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/report_{timestamp}.json"
        with open(filename, "w") as f:
            f.write(self.to_json())
        from core.logger import logger
        logger.info(f"Report exported to {filename}")


# Global singleton for backward compatibility
report = Report()