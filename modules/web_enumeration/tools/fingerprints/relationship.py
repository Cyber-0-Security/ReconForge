"""
Technology Relationship Resolver

Handles:

- implies
- requires
- excludes

for detected technologies.
"""

from __future__ import annotations

from .models import (
    DetectionResult,
    Technology,
)


class RelationshipResolver:
    """
    Resolve relationships between technologies.
    """

    def resolve(
        self,
        results: list[DetectionResult],
        technologies: list[Technology],
    ) -> list[DetectionResult]:

        results = self._apply_implications(
            results,
            technologies,
        )

        results = self._apply_requirements(
            results,
        )

        results = self._apply_exclusions(
            results,
        )

        return results

    # ---------------------------------------------------------

    def _apply_implications(
        self,
        results: list[DetectionResult],
        technologies: list[Technology],
    ) -> list[DetectionResult]:

        names = {
            r.technology.name
            for r in results
        }

        additions: list[DetectionResult] = []

        for result in results:

            for implied in result.technology.implies:

                if implied in names:
                    continue

                tech = self._find(
                    technologies,
                    implied,
                )

                if tech is None:
                    continue

                additions.append(

                    DetectionResult(
                        technology=tech,
                        confidence=max(
                            50,
                            result.confidence - 20,
                        ),
                        evidence=[
                            f"Implied by {result.technology.name}"
                        ],
                    )

                )

                names.add(implied)

        results.extend(additions)

        return results

    # ---------------------------------------------------------

    def _apply_requirements(
        self,
        results: list[DetectionResult],
    ) -> list[DetectionResult]:

        names = {
            r.technology.name
            for r in results
        }

        filtered: list[DetectionResult] = []

        for result in results:

            requirements = getattr(
                result.technology,
                "requires",
                [],
            )

            if not requirements:

                filtered.append(result)

                continue

            if all(
                requirement in names
                for requirement in requirements
            ):

                filtered.append(result)

        return filtered

    # ---------------------------------------------------------

    def _apply_exclusions(
        self,
        results: list[DetectionResult],
    ) -> list[DetectionResult]:

        excluded = set()

        for result in results:

            excluded.update(
                result.technology.excludes
            )

        return [

            result

            for result in results

            if result.technology.name not in excluded

        ]

    # ---------------------------------------------------------

    @staticmethod
    def _find(
        technologies: list[Technology],
        name: str,
    ) -> Technology | None:

        for technology in technologies:

            if technology.name == name:

                return technology

        return None


relationship = RelationshipResolver()