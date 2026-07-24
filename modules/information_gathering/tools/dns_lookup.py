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

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> dict[str, list[str]]:
        """
        Execute DNS enumeration.
        """

        self.start(silent)

        if target is None:
            target = validator.get_domain()

        if display:
            print()

        results: dict[str, list[str]] = {}

        for record_type in self.RECORD_TYPES:

            results[record_type] = self.lookup_record(
                target,
                record_type,
                silent,
                display,
            )

        self.finish(silent)

        return results

    def lookup_record(
        self,
        domain: str,
        record_type: str,
        silent: bool = False,
        display: bool = True,
    ) -> list[str]:
        """
        Resolve a single DNS record type.
        """

        records: list[str] = []

        if display:
            print(f"========== {record_type} Records ==========")

        try:

            answers = dns.resolver.resolve(domain, record_type)

            for answer in answers:

                value = answer.to_text()

                records.append(value)

                if display:
                    print(value)

        except dns.resolver.NoAnswer:

            if display:
                print("No records found.")

        except dns.resolver.NXDOMAIN:

            if display:
                print("Domain does not exist.")

        except dns.resolver.NoNameservers:

            if display:
                print("No nameservers responded.")

        except dns.exception.Timeout:

            if display:
                print("DNS request timed out.")

        except Exception as error:

            if not silent:
                logger.error(
                    f"{record_type} lookup failed for {domain}: {error}"
                )

            if display:
                print(f"Error: {error}")

        if display:
            print()

        return records