"""
Wordlist Loader

Loads and prepares wordlists for directory enumeration.
"""

from __future__ import annotations

from pathlib import Path


class WordlistLoader:
    """
    Loads directory enumeration wordlists.
    """

    def __init__(self) -> None:

        self.default_directory = (
            Path(__file__).parent / "wordlists"
        )

    def load(
        self,
        wordlist: str,
        extensions: list[str] | None = None,
    ) -> list[str]:
        """
        Load a wordlist and optionally expand extensions.
        """

        path = Path(wordlist)

        if not path.is_file():

            path = self.default_directory / wordlist

        if not path.is_file():

            raise FileNotFoundError(
                f"Wordlist not found: {wordlist}"
            )

        entries: list[str] = []

        seen: set[str] = set()

        with path.open(
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            for line in file:

                entry = line.strip()

                if (
                    not entry
                    or entry.startswith("#")
                ):
                    continue

                if entry not in seen:

                    seen.add(entry)

                    entries.append(entry)

        if extensions:

            entries = self._expand_extensions(
                entries,
                extensions,
            )

        return entries

    # ---------------------------------------------------------

    def _expand_extensions(
        self,
        entries: list[str],
        extensions: list[str],
    ) -> list[str]:
        """
        Expand paths using file extensions.

        Example

        admin

        ->
        admin
        admin.php
        admin.txt
        admin.bak
        """

        expanded: list[str] = []

        seen: set[str] = set()

        for entry in entries:

            if entry not in seen:

                seen.add(entry)

                expanded.append(entry)

            for extension in extensions:

                extension = extension.lstrip(".")

                candidate = f"{entry}.{extension}"

                if candidate not in seen:

                    seen.add(candidate)

                    expanded.append(candidate)

        return expanded


wordlists = WordlistLoader()