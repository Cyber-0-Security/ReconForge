"""
modules/information_gathering/tools/whois.py

WHOIS lookup tool for ReconForge.
"""

from __future__ import annotations

import whois

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator
from core.utils import separator


class WhoisTool(BaseTool):
    """
    Perform a WHOIS lookup against a domain.
    """

    def __init__(self) -> None:

        super().__init__("WHOIS Lookup")

    def run(self, target: str | None = None, silent: bool = False, display: bool = True) -> dict[str, object]:
        """
        Execute the WHOIS lookup.
        """

        self.start(silent)

        if target is None:
            target = validator.get_domain()

        results: dict[str, object] = {}

        try:

            if not silent:
                logger.info(f"Looking up {target}")

            result = whois.whois(target)

            if display:
                print()
                print(separator())
                print("WHOIS RESULTS")
                print(separator())

            results = self.display_result(result,display)

        except Exception as error:

            logger.error(f"WHOIS lookup failed: {error}")

        finally:

            self.finish(silent)

        return results

    def display_result(self, result, display: bool = True) -> dict[str, object]:
        """
        Display important WHOIS fields.
        """

        results: dict[str, object] = {}

        fields = [
            ("Domain Name", "domain_name"),
            ("Registrar", "registrar"),
            ("Creation Date", "creation_date"),
            ("Expiration Date", "expiration_date"),
            ("Updated Date", "updated_date"),
            ("Name Servers", "name_servers"),
            ("Status", "status"),
            ("Emails", "emails"),
            ("DNSSEC", "dnssec"),
        ]

        for title, attribute in fields:

            value = getattr(result, attribute, None)

            if value:
                results[title] = value

                if display:
                    print(f"{title:<20}: {value}")

        return results