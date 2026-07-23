"""
config/constants.py

Central location for all application-wide constants used by ReconForge.

This module contains only static values such as:
    - Application metadata
    - Filesystem paths
    - Banner text
    - Menu configuration
    - ANSI colors
    - Logging configuration

No application logic should exist in this file.
"""

from pathlib import Path

# =============================================================================
# Application Metadata
# =============================================================================

APP_NAME = "ReconForge"
APP_VERSION = "0.0.1-dev"
APP_AUTHOR = "Avinash Patel"
APP_DESCRIPTION = "Modular Reconnaissance and VAPT Automation Framework"

# =============================================================================
# Project Paths
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
CORE_DIR = BASE_DIR / "core"
MODULES_DIR = BASE_DIR / "modules"

LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

CONFIG_FILE = CONFIG_DIR / "settings.json"
LOG_FILE = LOG_DIR / "reconforge.log"

# =============================================================================
# Banner
# =============================================================================

BANNER = r"""
   ____                      _____
  |  _ \ ___  ___ ___  _ __ |  ___|__  _ __ __ _  ___
  | |_) / _ \/ __/ _ \| '_ \| |_ / _ \| '__/ _` |/ _ \
  |  _ <  __/ (_| (_) | | | |  _| (_) | | | (_| |  __/
  |_| \_\___|\___\___/|_| |_|_|  \___/|_|  \__, |\___|
                                            |___/
"""

BANNER_SUBTITLE = f"{APP_NAME} v{APP_VERSION}"
BANNER_DESCRIPTION = APP_DESCRIPTION

# =============================================================================
# Main Menu Configuration
# =============================================================================

MENU_OPTIONS = (
    ("Information Gathering", "information_gathering"),
    ("Network Enumeration", "network_enumeration"),
    ("Web Enumeration", "web_enumeration"),
    ("Vulnerability Assessment", "vulnerability"),
    ("Reporting", "reporting"),
    ("Full Recon", "full_recon"),
    ("Settings", "settings"),
)

# =============================================================================
# Module Registry
# =============================================================================

MODULES = {
    "information_gathering": "Information Gathering",
    "network_enumeration": "Network Enumeration",
    "web_enumeration": "Web Enumeration",
    "vulnerability": "Vulnerability Assessment",
    "reporting": "Reporting",
}

# =============================================================================
# Runtime Configuration
# =============================================================================

SUPPORTED_OPERATING_SYSTEMS = (
    "Linux",
)

SUPPORTED_PROTOCOLS = (
    "http",
    "https",
)

# =============================================================================
# ANSI Terminal Colors
# =============================================================================


class Colors:
    """ANSI escape sequences for colored terminal output."""

    RESET = "\033[0m"

    BOLD = "\033[1m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

# =============================================================================
# Logging
# =============================================================================

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"