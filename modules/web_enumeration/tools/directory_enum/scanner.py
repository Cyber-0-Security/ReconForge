"""
Scanner

Generates scan targets from a base URL and a wordlist.
"""

from __future__ import annotations

from .models import (
    ScanConfig,
    ScanTarget,
)
from .wordlists import wordlists


class Scanner:
    """
    Generates ScanTarget objects.
    """

    def generate(
        self,
        config: ScanConfig,
    ) -> list[ScanTarget]:
        """
        Generate scan targets from the configured wordlist.
        """

        entries = wordlists.load(
            config.wordlist,
            config.extensions,
        )

        base_url = config.url.rstrip("/")

        targets: list[ScanTarget] = []

        for entry in entries:

            entry = entry.lstrip("/")

            targets.append(

                ScanTarget(

                    path=entry,

                    url=f"{base_url}/{entry}",

                )

            )

        return targets


scanner = Scanner()