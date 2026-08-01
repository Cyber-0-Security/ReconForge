"""
Parameter Intelligence

Maps discovered URL parameters to potential security relevance.
"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlparse

from .models import ParameterFinding
from .parameter_database import PARAMETER_DATABASE


class ParameterIntelligence:
    """
    Classifies interesting URL parameters.
    """

    def analyze(
        self,
        url: str,
    ) -> list[ParameterFinding]:
        """
        Extract and classify URL parameters.
        """

        findings: list[ParameterFinding] = []

        parsed = urlparse(url)

        for name, value in parse_qsl(
            parsed.query,
            keep_blank_values=True,
        ):

            info = PARAMETER_DATABASE.get(
                name.lower(),
            )

            if not info:
                continue

            for category in info["categories"]:

                findings.append(

                    ParameterFinding(

                        name=name,

                        value=value,

                        severity=info["severity"],

                        category=category,

                        source=url,

                    )

                )

        return findings

    # ---------------------------------------------------------

    def is_interesting(
        self,
        parameter: str,
    ) -> bool:
        """
        Return True if the parameter exists in the intelligence database.
        """

        return parameter.lower() in PARAMETER_DATABASE

    # ---------------------------------------------------------

    def get_categories(
        self,
        parameter: str,
    ) -> list[str]:
        """
        Return all categories associated with a parameter.
        """

        info = PARAMETER_DATABASE.get(
            parameter.lower(),
        )

        if not info:

            return []

        return info["categories"]

    # ---------------------------------------------------------

    def get_severity(
        self,
        parameter: str,
    ) -> str | None:
        """
        Return the severity of a parameter.
        """

        info = PARAMETER_DATABASE.get(
            parameter.lower(),
        )

        if not info:

            return None

        return info["severity"]


parameter_intelligence = ParameterIntelligence()