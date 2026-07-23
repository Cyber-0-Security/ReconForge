"""
core/runner.py

Execution engine for ReconForge.

The Runner class is responsible for loading and executing
module managers dynamically. It acts as the bridge between
the user interface (menu) and the individual ReconForge modules.

The menu only decides *what* the user selected.
The runner decides *how* that module is executed.
"""

from __future__ import annotations

import importlib
from typing import Any

from config.constants import MODULES
from core.logger import logger


class Runner:
    """
    Execute ReconForge modules dynamically.

    Every functional module (Information Gathering,
    Network Enumeration, etc.) exposes a manager.py
    file with an execute() function.

    Runner imports that manager automatically and
    executes it.
    """

    def __init__(self) -> None:
        """
        Initialize the execution engine.
        """

        self.loaded_modules: dict[str, Any] = {}

    def run(self, module_key: str) -> bool:
        """
        Execute a module.

        Parameters
        ----------
        module_key : str
            Internal module name.

        Returns
        -------
        bool
            True if execution succeeds.
            False otherwise.
        """

        if module_key not in MODULES:

            logger.error(f"Unknown module: {module_key}")

            return False

        logger.info(f"Loading module: {module_key}")

        try:

            manager = self._load_manager(module_key)

            logger.success(f"{module_key} loaded successfully.")

            manager.execute()

            return True

        except Exception as error:

            logger.exception(f"Failed to execute module '{module_key}': {error}")

            return False

    def _load_manager(self, module_path: str) -> Any:
        """
        Import a module manager dynamically.

        If already imported, return the cached copy.
        """

        if module_path in self.loaded_modules:

            return self.loaded_modules[module_path]

        manager = importlib.import_module(
            f"modules.{module_path}.manager"
        )

        self.loaded_modules[module_path] = manager

        return manager


runner = Runner()