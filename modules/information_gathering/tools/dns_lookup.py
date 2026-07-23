"""
modules/information_gathering/tools/dns_lookup.py

DNS Lookup Tool

Performs DNS enumeration using dnspython.
"""

from __future__ import annotations

import dns.resolver

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator


class DNSLookupTool(BaseTool):
    """
    Retrieve common DNS records for a domain.
    """

    RECORD_TYPES = (
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME",
        "SOA",
    )

    def __init__(self) -> None:
        super().__init__("DNS Lookup")

    def run(self) -> None:

        self.start()

        target = validator.get_domain("Enter domain: ")

        print()

        for record_type in self.RECORD_TYPES:

            self.lookup_record(target, record_type)

        self.finish()

    def lookup_record(self, domain: str, record_type: str) -> None:
        """
        Resolve one DNS record type.
        """

        print(f"========== {record_type} Records ==========")

        try:

            answers = dns.resolver.resolve(domain, record_type)

            found = False

            for answer in answers:

                print(answer.to_text())

                found = True

            if not found:
                print("No records found.")

        except dns.resolver.NoAnswer:

            print("No records found.")

        except dns.resolver.NXDOMAIN:

            print("Domain does not exist.")

        except dns.resolver.NoNameservers:

            print("No nameservers responded.")

        except Exception as error:

            logger.error(str(error))

            print(f"Error: {error}")

        print()