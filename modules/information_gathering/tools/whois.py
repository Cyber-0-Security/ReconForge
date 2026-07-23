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

    def run(self) -> None:
        """
        Execute the WHOIS lookup.
        """

        self.start()

        domain = validator.get_domain()

        try:

            logger.info(f"Looking up {domain}")

            result = whois.whois(domain)

            print()
            print(separator())
            print("WHOIS RESULTS")
            print(separator())

            self.display_result(result)

        except Exception as error:

            logger.error(f"WHOIS lookup failed: {error}")

        finally:

            self.finish()

    def display_result(self, result) -> None:
        """
        Display important WHOIS fields.
        """

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

                print(f"{title:<20}: {value}")