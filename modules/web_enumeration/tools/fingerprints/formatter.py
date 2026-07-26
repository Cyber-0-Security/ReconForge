"""
Formatting helpers for technology detection output.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import DetectionResult


DISPLAY_ORDER = [
    "Frontend",
    "CSS Framework",
    "Backend",
    "Web Servers",
    "CMS",
    "Analytics",
    "Infrastructure",
    "Security",
    "Payment",
    "Chat",
    "Fonts",
    "Other",
]


def group_detections(
    detections: Iterable[DetectionResult],
) -> dict[str, list[DetectionResult]]:
    """
    Group detection results by category.
    """

    grouped: dict[str, list[DetectionResult]] = defaultdict(list)

    for item in detections:
        categories = item.technology.categories
        category = categories[0] if categories else "Other"
        grouped[category].append(item)

    return dict(grouped)


def print_detections(
    detections: list[DetectionResult],
) -> None:
    """
    Print grouped detection output.
    """

    grouped = group_detections(detections)

    print()
    print("=" * 60)
    print("TECHNOLOGY DETECTION")
    print("=" * 60)

    if not detections:
        print("No technologies detected.")
        print()
        return

    for category in DISPLAY_ORDER:
        items = grouped.get(category)
        if not items:
            continue

        print()
        print(category)
        print("-" * len(category))

        for item in sorted(
            items,
            key=lambda x: (-x.confidence, x.technology.name.lower()),
        ):
            label = item.technology.name
            if item.version:
                label = f"{label} {item.version}"

            print(f"• {label}")