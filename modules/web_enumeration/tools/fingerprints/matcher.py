"""
Fingerprint Matcher

Matches technologies against the collected detection context
and assigns confidence scores.
"""

from __future__ import annotations

from .models import (
    DetectionContext,
    DetectionResult,
    Technology,
)


class FingerprintMatcher:
    """
    Match technologies against a detection context.
    """

    WEIGHTS = {
        "headers": 35,
        "cookies": 20,
        "html": 20,
        "scripts": 30,
        "css": 10,
        "meta": 15,
        "javascript": 40,
    }

    def match(
        self,
        technologies: list[Technology],
        context: DetectionContext,
    ) -> list[DetectionResult]:
        """
        Match every technology.
        """

        results: list[DetectionResult] = []

        for technology in technologies:

            confidence = 0
            evidence: list[str] = []

            confidence += self._match_headers(
                technology,
                context,
                evidence,
            )

            confidence += self._match_cookies(
                technology,
                context,
                evidence,
            )

            confidence += self._match_html(
                technology,
                context,
                evidence,
            )

            confidence += self._match_scripts(
                technology,
                context,
                evidence,
            )

            confidence += self._match_css(
                technology,
                context,
                evidence,
            )

            confidence += self._match_meta(
                technology,
                context,
                evidence,
            )

            confidence += self._match_javascript(
                technology,
                context,
                evidence,
            )

            if confidence >= technology.confidence:

                results.append(
                    DetectionResult(
                        technology=technology,
                        confidence=confidence,
                        evidence=evidence,
                    )
                )

        return sorted(
            results,
            key=lambda x: x.confidence,
            reverse=True,
        )

    # ---------------------------------------------------------

    def _match_headers(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_list(
            technology.fingerprint.headers,
            context.headers.values(),
            self.WEIGHTS["headers"],
            evidence,
            "Header",
        )

    def _match_cookies(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        cookie_string = [
            c.name + "=" + c.value
            for c in context.cookies
        ]

        return self._match_list(
            technology.fingerprint.cookies,
            cookie_string,
            self.WEIGHTS["cookies"],
            evidence,
            "Cookie",
        )

    def _match_html(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_string(
            technology.fingerprint.html,
            context.html,
            self.WEIGHTS["html"],
            evidence,
            "HTML",
        )

    def _match_scripts(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_list(
            technology.fingerprint.scripts,
            context.scripts,
            self.WEIGHTS["scripts"],
            evidence,
            "Script",
        )

    def _match_css(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_list(
            technology.fingerprint.css,
            context.css,
            self.WEIGHTS["css"],
            evidence,
            "CSS",
        )

    def _match_meta(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_list(
            technology.fingerprint.meta,
            context.meta,
            self.WEIGHTS["meta"],
            evidence,
            "Meta",
        )

    def _match_javascript(
        self,
        technology: Technology,
        context: DetectionContext,
        evidence: list[str],
    ) -> int:

        return self._match_string(
            technology.fingerprint.javascript,
            context.body,
            self.WEIGHTS["javascript"],
            evidence,
            "JavaScript",
        )

    # ---------------------------------------------------------

    def _match_string(
        self,
        fingerprints: list[str],
        source: str,
        weight: int,
        evidence: list[str],
        source_name: str,
    ) -> int:

        score = 0

        source = source.lower()

        for fingerprint in fingerprints:

            if fingerprint.lower() in source:

                score += weight

                evidence.append(
                    f"{source_name}: {fingerprint}"
                )

        return score

    def _match_list(
        self,
        fingerprints: list[str],
        source: list,
        weight: int,
        evidence: list[str],
        source_name: str,
    ) -> int:

        score = 0

        values = [
            str(item).lower()
            for item in source
        ]

        for fingerprint in fingerprints:

            fp = fingerprint.lower()

            for value in values:

                if fp in value:

                    score += weight

                    evidence.append(
                        f"{source_name}: {fingerprint}"
                    )

                    break

        return score


matcher = FingerprintMatcher()