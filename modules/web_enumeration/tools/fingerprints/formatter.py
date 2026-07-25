"""
Technology Detection output formatter.
"""

from __future__ import annotations

from collections import defaultdict

from .categories import CATEGORIES


def group_technologies(
    technologies: set[str],
) -> dict[str, list[str]]:
    """
    Group detected technologies by category.
    """

    grouped = defaultdict(list)

    for technology in sorted(technologies):

        category = CATEGORIES.get(
            technology,
            "Other",
        )

        grouped[category].append(technology)

    return dict(grouped)


def print_technologies(
    technologies: set[str],
) -> None:
    """
    Print technologies grouped by category.
    """

    grouped = group_technologies(
        technologies,
    )

    print()
    print("=" * 60)
    print("TECHNOLOGY DETECTION")
    print("=" * 60)

    if not grouped:

        print("No technologies detected.")
        return

    #
    # Desired display order
    #

    order = [

        "Frontend",
        "CSS Framework",
        "Backend",
        "CMS",
        "Analytics",
        "Infrastructure",
        "Security",
        "Payment",
        "Chat",
        "Fonts",
        "Other",
    ]

    for category in order:

        if category not in grouped:
            continue

        print()
        print(category)
        print("-" * len(category))

        for technology in grouped[category]:

            print(f"• {technology}")