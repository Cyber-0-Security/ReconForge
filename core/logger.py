"""
core/logger.py

Central logging system for ReconForge.

Responsibilities
----------------
- Display colored log messages in the terminal.
- Save all log messages to logs/reconforge.log.
- Provide a single logger instance for the entire application.
- Keep logging consistent across every module.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config.constants import (
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
    Colors,
)
from config.settings import settings
from core.utils import ensure_directory


class ConsoleFormatter(logging.Formatter):
    """
    Custom formatter used only for terminal output.

    Every log level gets its own color while the log file
    remains plain text.
    """

    LEVEL_COLORS = {
        logging.DEBUG: Colors.MAGENTA,
        logging.INFO: Colors.CYAN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a single console log record.
        """

        color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)

        message = super().format(record)

        return f"{color}{message}{Colors.RESET}"


class ReconLogger:
    """
    Wrapper around Python's logging module.

    Every module imports the same logger instance instead
    of creating its own logger.
    """

    def __init__(self) -> None:

        ensure_directory(Path(LOG_FILE).parent)

        self._logger = logging.getLogger("ReconForge")

        if self._logger.handlers:
            return

        self._logger.setLevel(settings.log_level)

        self._logger.propagate = False

        self._configure_console_handler()

        self._configure_file_handler()

    def _configure_console_handler(self) -> None:
        """
        Configure colored terminal logging.
        """

        console_handler = logging.StreamHandler()

        console_handler.setLevel(settings.log_level)

        console_formatter = ConsoleFormatter(
            "[%(levelname)s] %(message)s"
        )

        console_handler.setFormatter(console_formatter)

        self._logger.addHandler(console_handler)

    def _configure_file_handler(self) -> None:
        """
        Configure file logging.
        """

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )

        file_handler.setLevel(settings.log_level)

        file_formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=LOG_DATE_FORMAT,
        )

        file_handler.setFormatter(file_formatter)

        self._logger.addHandler(file_handler)
        
    def debug(self, message: str) -> None:
        """
        Log a debug message.
        """

        self._logger.debug(message)

    def info(self, message: str) -> None:
        """
        Log an informational message.
        """

        self._logger.info(message)

    def success(self, message: str) -> None:
        """
        Log a success message.

        Python's logging module does not provide a SUCCESS level,
        so successful operations are logged as INFO with a prefix.
        """

        self._logger.info(f"[SUCCESS] {message}")

    def warning(self, message: str) -> None:
        """
        Log a warning message.
        """

        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        Log an error message.
        """

        self._logger.error(message)

    def critical(self, message: str) -> None:
        """
        Log a critical error.
        """

        self._logger.critical(message)

    def exception(self, message: str) -> None:
        """
        Log an exception together with its traceback.

        This should only be called from inside an except block.
        """

        self._logger.exception(message)


# --------------------------------------------------------------------------
# Global logger instance
# --------------------------------------------------------------------------

logger = ReconLogger()