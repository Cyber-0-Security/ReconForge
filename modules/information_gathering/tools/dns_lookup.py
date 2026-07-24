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

    def run(self, target: str | None = None) -> dict[str, list[str]]:

        self.start()

        if target is None:
            target = validator.get_domain()

        print()

        results: dict[str, list[str]] = {}

        for record_type in self.RECORD_TYPES:

            results[record_type] = self.lookup_record(
                target,
                record_type,
            )

        self.finish()

        return results

    def lookup_record(
        self,
        domain: str,
        record_type: str,
    ) -> list[str]:
        """
        Resolve one DNS record type.
        """

        records: list[str] = []

        print(f"========== {record_type} Records ==========")

        try:

            answers = dns.resolver.resolve(domain, record_type)

            for answer in answers:

                value = answer.to_text()

                records.append(value)

                print(value)

        except dns.resolver.NoAnswer:

            print("No records found.")

        except dns.resolver.NXDOMAIN:

            print("Domain does not exist.")

        except dns.resolver.NoNameservers:

            print("No nameservers responded.")

        except Exception as error:

            logger.error(
                f"{record_type} lookup failed for {domain}: {error}"
            )

            print(f"Error: {error}")

        print()

        return records