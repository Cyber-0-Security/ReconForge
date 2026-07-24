"""
modules/information_gathering/tools/full_recon.py

Full Recon Tool

Runs multiple information gathering tools
against a single target and presents the
results in a clean report.
"""

from __future__ import annotations

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator
from core.utils import separator

from modules.information_gathering.tools.whois import WhoisTool
from modules.information_gathering.tools.dns_lookup import DNSLookupTool
from modules.information_gathering.tools.reverse_dns import ReverseDNSTool
from modules.information_gathering.tools.ip_info import IPInfoTool


class FullReconTool(BaseTool):
    """
    Execute a complete information gathering workflow.
    """

    def __init__(self) -> None:

        super().__init__("Full Recon")

    def run(self) -> None:

        self.start()

        target = validator.get_domain("Enter target domain: ")

        print()

        print(separator())
        print("RECONFORGE - FULL RECON")
        print(separator())
        print(f"Target : {target}")
        print(separator())

        whois_tool = WhoisTool()
        dns_tool = DNSLookupTool()
        reverse_dns_tool = ReverseDNSTool()
        ip_info_tool = IPInfoTool()

        #
        # WHOIS
        #

        print("\n[1/4] WHOIS")
        print("-" * 60)

        whois_data = whois_tool.run(
            target,
            silent=True,
            display=False,
        )

        self.print_value("Registrar", whois_data.get("Registrar"))
        self.print_value("Creation Date", whois_data.get("Creation Date"))
        self.print_value("Expiration", whois_data.get("Expiration Date"))

        #
        # DNS
        #

        print("\n[2/4] DNS")
        print("-" * 60)

        dns_data = dns_tool.run(
            target,
            silent=True,
            display=False,
        )

        self.print_list("IPv4", dns_data.get("A"))
        self.print_list("IPv6", dns_data.get("AAAA"))
        self.print_list("MX", dns_data.get("MX"))
        self.print_list("NS", dns_data.get("NS"))

        #
        # Reverse DNS + IP Info
        #

        ipv4_records = dns_data.get("A", [])

        if ipv4_records:

            ip = ipv4_records[0]

            print("\n[3/4] Reverse DNS")
            print("-" * 60)

            reverse_data = reverse_dns_tool.run(
                ip,
                silent=True,
                display=False,
            )

            self.print_list("PTR", reverse_data.get("PTR"))

            print("\n[4/4] IP Information")
            print("-" * 60)

            ip_data = ip_info_tool.run(
                ip,
                silent=True,
                display=False,
            )

            self.print_value("IP Address", ip_data.get("IP Address"))
            self.print_value("Country", ip_data.get("Country"))
            self.print_value("Region", ip_data.get("Region"))
            self.print_value("City", ip_data.get("City"))
            self.print_value("ISP", ip_data.get("ISP"))
            self.print_value("Organization", ip_data.get("Organization"))
            self.print_value("ASN", ip_data.get("ASN"))
            self.print_value("Timezone", ip_data.get("Timezone"))

        else:

            logger.warning(
                "No IPv4 address found. Reverse DNS and IP Information skipped."
            )

        print()
        print(separator())
        logger.success("Full Recon completed successfully.")
        print(separator())

        self.finish()

    @staticmethod
    def print_value(title: str, value) -> None:
        """
        Print a single key/value pair.
        """

        if value is None:
            value = "N/A"

        if isinstance(value, list):

            if not value:
                value = "N/A"

            else:
                value = value[0]

        print(f"{title:<20}: {value}")

    @staticmethod
    def print_list(title: str, values) -> None:
        """
        Print a list of values.
        """

        if not values:

            print(f"{title:<20}: N/A")

            return

        if not isinstance(values, list):

            values = [values]

        print(f"{title:<20}: {values[0]}")

        for value in values[1:]:

            print(f"{'':<20}  {value}")