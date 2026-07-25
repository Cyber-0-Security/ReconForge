"""
Fingerprint Loader

Loads every fingerprint JSON file automatically.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FingerprintLoader:
    """
    Loads all fingerprint JSON databases.
    """

    def __init__(self) -> None:

        self.base_path = (
        Path(__file__).parent / "fingerprint_jsons"
        )

        self.database: list[dict[str, Any]] = []

    def load(self) -> list[dict[str, Any]]:
        """
        Load every JSON fingerprint database.
        """

        self.database.clear()

        if not self.base_path.exists():
            raise FileNotFoundError(
                f"Fingerprint directory not found: {self.base_path}"
            )

        for json_file in sorted(self.base_path.glob("*.json")):

            self.database.extend(
                self._load_file(json_file)
            )

        return self.database

    def _load_file(
        self,
        filepath: Path,
    ) -> list[dict[str, Any]]:
        """
        Load one fingerprint JSON file.
        """

        with filepath.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        technologies = data.get("technologies", [])

        if not isinstance(technologies, list):
            return []

        return technologies


loader = FingerprintLoader()