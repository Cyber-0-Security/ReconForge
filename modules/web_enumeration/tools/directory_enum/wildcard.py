"""
Wildcard Detection

Detects wildcard responses from web servers.
"""

from __future__ import annotations

import random
import string

from .models import (
    ScanConfig,
    WildcardSignature,
)
from .requester import requester
from .models import ScanTarget


class WildcardDetector:
    """
    Detect wildcard responses.
    """

    def detect(
        self,
        config: ScanConfig,
    ) -> WildcardSignature | None:
        """
        Determine whether the server returns
        identical responses for non-existent paths.
        """

        random_path = self._random_string()

        target = ScanTarget(

            path=random_path,

            url=f"{config.url}/{random_path}",

        )

        result = requester.request(
            target,
            config,
        )

        if result is None:

            return None

        return WildcardSignature(

            status=result.status,

            length=result.length,

            words=result.words,

            lines=result.lines,

        )

    # -----------------------------------------------------

    @staticmethod
    def _random_string(
        length: int = 24,
    ) -> str:

        alphabet = string.ascii_letters + string.digits

        return "".join(

            random.choice(alphabet)

            for _ in range(length)

        )


wildcard = WildcardDetector()