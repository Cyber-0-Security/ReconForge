"""
Fingerprint Engine

Coordinates the complete technology detection pipeline.
"""

from __future__ import annotations

from .loader import loader
from .relationship import relationship
from .normalizer import normalizer
from .matcher import matcher
from .models import (
    DetectionContext,
    DetectionResult,
    Fingerprint,
    Technology,
)
from .version_detector import version_detector


class FingerprintEngine:
    """
    Main technology fingerprint engine.
    """

    _database_cache: list[Technology] | None = None

    def __init__(self) -> None:

        if FingerprintEngine._database_cache is None:

            FingerprintEngine._database_cache = self._load_database()

        self.technologies = FingerprintEngine._database_cache

    def detect(
        self,
        context: DetectionContext,
    ) -> list[DetectionResult]:
        """
        Run the complete detection pipeline.
        """
        context = normalizer.normalize(context)
        results = matcher.match(
            self.technologies,
            context,
        )

        results = version_detector.detect(
            results,
            context,
        )

        results = relationship.resolve(results,self.technologies)

        results.sort(
            key=lambda x: x.confidence,
            reverse=True,
        )

        return results

    # ---------------------------------------------------------

    def _load_database(
        self,
    ) -> list[Technology]:
        """
        Load every technology from every JSON file.
        """

        technologies: list[Technology] = []

        for item in loader.load():

            fingerprints = item.get(
                "fingerprints",
                {},
            )

            #
            # The JSON schema stores a single "category" string,
            # not a "categories" list. Support both, in case a
            # future file uses the plural form directly.
            #

            raw_category = item.get("category")

            categories = (
                [raw_category]
                if raw_category
                else item.get("categories", [])
            )

            #
            # The JSON schema stores version patterns as a nested
            # dict, e.g. {"scripts": ["re:...", ...]}, not as a
            # flat "versions" list. Flatten every list found inside
            # it into one combined list of patterns.
            #

            raw_version = item.get("version", {})

            if isinstance(raw_version, dict):

                versions: list[str] = []

                for pattern_list in raw_version.values():
                    versions.extend(pattern_list)

            elif isinstance(raw_version, list):

                versions = raw_version

            else:

                versions = []

            technology = Technology(

                name=item.get(
                    "name",
                    "",
                ),

                categories=categories,

                confidence=item.get(
                    "confidence",
                    60,
                ),

                website=item.get(
                    "website",
                    "",
                ),

                description=item.get(
                    "description",
                    "",
                ),

                implies=item.get(
                    "implies",
                    [],
                ),

                requires=item.get(
                "requires",
                [],
                ),

                excludes=item.get(
                    "excludes",
                    [],
                ),

                versions=versions,

                fingerprint=Fingerprint(

                    headers=fingerprints.get(
                        "headers",
                        [],
                    ),

                    html=fingerprints.get(
                        "html",
                        [],
                    ),

                    scripts=fingerprints.get(
                        "scripts",
                        [],
                    ),

                    css=fingerprints.get(
                        "css",
                        [],
                    ),

                    meta=fingerprints.get(
                        "meta",
                        [],
                    ),

                    cookies=fingerprints.get(
                        "cookies",
                        [],
                    ),

                    javascript=fingerprints.get(
                        "javascript",
                        [],
                    ),

                    text=fingerprints.get(
                        "text",
                        [],
                    ),

                ),

            )

            technologies.append(
                technology
            )

        return technologies

engine = FingerprintEngine()