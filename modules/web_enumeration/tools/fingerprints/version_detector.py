"""
Version Detector

Extracts version numbers for detected technologies
using regex patterns defined in the fingerprint database.
"""

from __future__ import annotations

import re

from .models import (
    DetectionContext,
    DetectionResult,
)


class VersionDetector:
    """
    Extract version numbers from a detection context.
    """

    def detect(
        self,
        results: list[DetectionResult],
        context: DetectionContext,
    ) -> list[DetectionResult]:
        """
        Populate version information for every detected technology.
        """

        searchable_sources = [
            context.html,
            context.body,
            context.text,
            "\n".join(context.scripts),
            "\n".join(context.css),
            "\n".join(context.meta),
            "\n".join(
                f"{key}: {value}"
                for key, value in context.headers.items()
            ),
        ]

        searchable_text = "\n".join(searchable_sources)

        for result in results:

            result.version = self._extract_version(
                result.technology.versions,
                searchable_text,
            )

        return results

    def _extract_version(
        self,
        patterns: list[str],
        text: str,
    ) -> str | None:
        """
        Try every version regex until one succeeds.
        """

        if not patterns:
            return None

        for pattern in patterns:

            try:

                #
                # Patterns are stored with a "re:" prefix to mark
                # them as regular expressions in the JSON database.
                # That prefix itself isn't part of the pattern.
                #

                if pattern.startswith("re:"):
                    pattern = pattern[3:]

                match = re.search(
                    pattern,
                    text,
                    flags=re.IGNORECASE,
                )

                if not match:
                    continue

                #
                # If the regex contains a capturing group,
                # return the first captured value.
                #

                if match.groups():

                    return match.group(1).strip()

                #
                # Otherwise return the entire match.
                #

                return match.group(0).strip()

            except re.error:

                #
                # Ignore invalid regex patterns
                #

                continue

        return None


version_detector = VersionDetector()