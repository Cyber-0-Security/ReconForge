"""
modules/information_gathering/tools/reverse_dns.py

Reverse DNS Lookup Tool

Performs PTR lookup (IP -> Hostname).
"""

from __future__ import annotations

import dns.reversename
import dns.resolver

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator


class ReverseDNSTool(BaseTool):
    """
    Perform Reverse DNS lookup using PTR records.
    """

    def __init__(self) -> None:
        super().__init__("Reverse DNS Lookup")

    def run(
        self,
        ip: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> dict[str, list[str]]:

        self.start(silent)

        if ip is None:
            ip = validator.get_ip()

        if display:
            print()

        results: dict[str, list[str]] = {
            "PTR": [],
        }

        try:

            reverse_name = dns.reversename.from_address(ip)

            answers = dns.resolver.resolve(reverse_name, "PTR")

            if display:
                print("========== PTR Record ==========\n")

            for answer in answers:

                value = answer.to_text()

                results["PTR"].append(value)

                if display:
                    print(value)

        except dns.resolver.NXDOMAIN:

            if display:
                print("No PTR record found.")

        except dns.resolver.NoAnswer:

            if display:
                print("No PTR record found.")

        except dns.resolver.NoNameservers:

            if display:
                print("Nameserver did not respond.")

        except dns.exception.Timeout:

            if display:
                print("DNS request timed out.")

        except Exception as error:

            logger.error(f"Reverse DNS lookup failed for {ip}: {error}")

            if display:
                print(f"Error: {error}")

        if display:
            print()

        self.finish(silent)

        return results