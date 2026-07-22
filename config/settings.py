"""
config/settings.py

Configuration manager for ReconForge.

Responsibilities:
    - Create settings.json with default values if it does not exist.
    - Load settings from disk.
    - Validate settings.
    - Save updated settings.
    - Provide a simple interface for other modules.

Usage:
    from config.settings import settings

    print(settings.get("threads"))

    settings.set("threads", 20)
    settings.save()
"""

from __future__ import annotations

import json
from typing import Any

from config.constants import CONFIG_FILE


DEFAULT_SETTINGS = {
    "threads": 10,
    "timeout": 30,
    "log_level": "INFO",
    "color_output": True,
    "default_report": "html",
}


class SettingsManager:
    """Manage application configuration."""

    def __init__(self) -> None:
        self._settings: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """
        Load settings from disk.

        If the configuration file does not exist,
        create it using the default configuration.
        """

        if not CONFIG_FILE.exists():
            self._settings = DEFAULT_SETTINGS.copy()
            self.save()
            return

        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                self._settings = json.load(file)

        except (json.JSONDecodeError, OSError):
            self._settings = DEFAULT_SETTINGS.copy()
            self.save()

        self._validate()

    def save(self) -> None:
        """Save the current configuration to disk."""

        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        with CONFIG_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                self._settings,
                file,
                indent=4,
                sort_keys=True,
            )

    def _validate(self) -> None:
        """
        Ensure all required settings exist.

        Missing settings are automatically restored
        using their default values.
        """

        updated = False

        for key, value in DEFAULT_SETTINGS.items():
            if key not in self._settings:
                self._settings[key] = value
                updated = True

        if updated:
            self.save()

    def get(self, key: str, default: Any = None) -> Any:
        """Return a setting."""

        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Update a setting."""

        self._settings[key] = value

    @property
    def threads(self) -> int:
        return int(self.get("threads"))

    @threads.setter
    def threads(self, value: int) -> None:
        self.set("threads", value)

    @property
    def timeout(self) -> int:
        return int(self.get("timeout"))

    @timeout.setter
    def timeout(self, value: int) -> None:
        self.set("timeout", value)

    @property
    def log_level(self) -> str:
        return str(self.get("log_level"))

    @log_level.setter
    def log_level(self, value: str) -> None:
        self.set("log_level", value.upper())

    @property
    def color_output(self) -> bool:
        return bool(self.get("color_output"))

    @color_output.setter
    def color_output(self, value: bool) -> None:
        self.set("color_output", value)

    @property
    def default_report(self) -> str:
        return str(self.get("default_report"))

    @default_report.setter
    def default_report(self, value: str) -> None:
        self.set("default_report", value.lower())

    def reset(self) -> None:
        """Restore default configuration."""

        self._settings = DEFAULT_SETTINGS.copy()
        self.save()

    def to_dict(self) -> dict[str, Any]:
        """Return a copy of all settings."""

        return self._settings.copy()


settings = SettingsManager()