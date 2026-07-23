"""
core/validator.py

Validation helpers used throughout ReconForge.

Responsibilities
----------------
- Validate domains
- Validate IPv4 addresses
- Validate URLs
- Validate file paths
- Prompt the user until valid input is received

All modules should use this file instead of implementing
their own validation logic.
"""

from __future__ import annotations

import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse


class Validator:
    """
    Collection of reusable validation methods.
    """

    DOMAIN_REGEX = re.compile(
        r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
        r"(\.[A-Za-z0-9-]{1,63})+$"
    )

    def is_domain(self, domain: str) -> bool:
        """
        Check whether the supplied string is a valid domain.
        """

        domain = domain.strip().lower()

        if not domain:
            return False

        return bool(self.DOMAIN_REGEX.fullmatch(domain))

    def is_ip(self, ip: str) -> bool:
        """
        Validate an IPv4 or IPv6 address.
        """

        try:
            ipaddress.ip_address(ip.strip())
            return True

        except ValueError:
            return False

    def is_url(self, url: str) -> bool:
        """
        Validate a URL.
        """

        parsed = urlparse(url.strip())

        return bool(parsed.scheme and parsed.netloc)

    def file_exists(self, path: str) -> bool:
        """
        Check whether a file exists.
        """

        return Path(path).is_file()

    def get_domain(self, prompt: str = "Enter domain: ") -> str:
        """
        Prompt until a valid domain is entered.
        """

        while True:

            domain = input(prompt).strip()

            if self.is_domain(domain):
                return domain

            print("Invalid domain. Please try again.")

    def get_ip(self, prompt: str = "Enter IP Address: ") -> str:
        """
        Prompt until a valid IP address is entered.
        """

        while True:

            ip = input(prompt).strip()

            if self.is_ip(ip):
                return ip

            print("Invalid IP address. Please try again.")

    def get_url(self, prompt: str = "Enter URL: ") -> str:
        """
        Prompt until a valid URL is entered.
        """

        while True:

            url = input(prompt).strip()

            if self.is_url(url):
                return url

            print("Invalid URL. Please try again.")

    def get_existing_file(
        self,
        prompt: str = "Enter file path: ",
    ) -> Path:
        """
        Prompt until an existing file is supplied.
        """

        while True:

            path = Path(input(prompt).strip())

            if path.is_file():
                return path

            print("File not found. Please try again.")


validator = Validator()