"""
Directory Enumeration Engine

Coordinates the complete directory enumeration pipeline.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from .models import (
    ScanConfig,
    ScanResult,
)
from .scanner import scanner
from .worker import worker
from .wildcard import wildcard


class DirectoryEnumerationEngine:
    """
    Coordinates the complete directory enumeration process.
    """

    def scan(
        self,
        config: ScanConfig,
    ) -> list[ScanResult]:
        """
        Execute a directory enumeration scan.
        """

        # Generate all scan targets
        targets = scanner.generate(config)

        # Detect wildcard responses before scanning
        wildcard_signature = wildcard.detect(config)

        results: list[ScanResult] = []

        with ThreadPoolExecutor(
            max_workers=config.threads,
        ) as executor:

            futures = [
                executor.submit(
                    worker.process,
                    target,
                    config,
                    wildcard_signature,
                )
                for target in targets
            ]

            for future in as_completed(futures):

                try:

                    result = future.result()

                except Exception:
                    continue

                if result is not None:

                    results.append(result)

        results.sort(
            key=lambda item: (
                item.status,
                item.path.lower(),
            )
        )

        return results


engine = DirectoryEnumerationEngine()