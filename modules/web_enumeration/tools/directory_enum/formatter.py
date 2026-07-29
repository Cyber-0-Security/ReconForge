"""
Directory Enumeration Formatter

Pretty-print directory enumeration results.
"""

from __future__ import annotations

from .models import ScanResult


def print_results(
    results: list[ScanResult],
) -> None:
    """
    Print scan results.
    """

    print()
    print("=" * 60)
    print("DIRECTORY ENUMERATION")
    print("=" * 60)

    if not results:

        print("No directories or files found.")
        return

    print(
        f"{'Status':<8}"
        f"{'Size':<10}"
        f"{'Type':<25}"
        f"Path"
    )

    print("-" * 60)

    for result in results:

        print(

            f"{result.status:<8}"

            f"{_human_size(result.length):<10}"

            f"{result.content_type[:24]:<25}"

            f"/{result.path}"

        )

    print("-" * 60)

    print(f"Found: {len(results)}")


# ---------------------------------------------------------


def _human_size(
    size: int,
) -> str:
    """
    Convert bytes into human readable format.
    """

    units = [
        "B",
        "KB",
        "MB",
        "GB",
    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return f"{value:.1f}{unit}"

        value /= 1024

    return f"{value:.1f}TB"