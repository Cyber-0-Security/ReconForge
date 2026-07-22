"""
core/utils.py

Shared utility functions used throughout ReconForge.

This module contains reusable helper functions that are not tied to any
specific module. Keeping them here avoids code duplication and makes the
project easier to maintain as it grows.
"""

from __future__ import annotations

import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def clear_screen() -> None:
    """
    Clear the terminal screen.

    Works on Windows, Linux and macOS.
    """

    command = "cls" if platform.system() == "Windows" else "clear"

    subprocess.run(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def current_timestamp() -> str:
    """
    Return the current local date and time.

    Example:
        2026-07-23 14:38:15
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(path: str | Path) -> None:
    """
    Create a directory if it does not already exist.
    """

    Path(path).mkdir(parents=True, exist_ok=True)


def command_exists(command: str) -> bool:
    """
    Check whether a command is available in the system PATH.

    Example:
        command_exists("whois")
        command_exists("nmap")
    """

    return shutil.which(command) is not None


def run_command(command: list[str]) -> tuple[bool, str]:
    """
    Execute a system command safely.

    Parameters
    ----------
    command:
        Command represented as a list.

    Returns
    -------
    tuple[bool, str]

        (True, output)   -> Command executed successfully.

        (False, error)   -> Command failed.
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return True, result.stdout.strip()

    except FileNotFoundError:
        return False, "Command not found."

    except subprocess.CalledProcessError as error:

        message = error.stderr.strip()

        if not message:
            message = "Command execution failed."

        return False, message


def separator(length: int = 70, character: str = "-") -> str:
    """
    Return a separator line for terminal output.

    Example:
    ------------------------------------------------------
    """

    return character * length