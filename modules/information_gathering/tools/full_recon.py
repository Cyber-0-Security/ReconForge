"""
modules/information_gathering/tools/full_recon.py

Full Recon Tool

Runs multiple information gathering tools
against a single target and stores the
results inside the central report object.
"""

from __future__ import annotations

from core.base_tool import BaseTool
from core.logger import logger
from core.report import report
from core.validator import validator

from modules.information_gathering.tools.whois import WhoisTool
from modules.information_gathering.tools.dns_lookup import DNSLookupTool
from modules.information_gathering.tools.reverse_dns import ReverseDNSTool
from modules.information_gathering.tools.ip_info import IPInfoTool
from modules.information_gathering.tools.subdomain_enum import SubdomainEnumerationTool


class FullReconTool(BaseTool):
    """
    Execute a complete information gathering workflow.
    """

    def __init__(self) -> None:

        super().__init__("Full Recon")

    def run(self) -> None:

        self.start()

        target = validator.get_domain("Enter target domain: ")

        report.clear()

        whois_tool = WhoisTool()
        dns_tool = DNSLookupTool()
        reverse_dns_tool = ReverseDNSTool()
        ip_info_tool = IPInfoTool()
        subdomain_tool = SubdomainEnumerationTool()

        #
        # WHOIS
        #

        logger.info("Running WHOIS lookup...")

        whois_data = whois_tool.run(
            target,
            silent=True,
            display=False,
        )

        report.add_section(
            "WHOIS",
            whois_data,
        )

        #
        # DNS
        #

        subdomains = subdomain_tool.run(
            target,
            silent=True,
            display=False,
        )

        report.add_section("Subdomains", subdomains)

        logger.info("Running DNS lookup...")

        dns_data = dns_tool.run(
            target,
            silent=True,
            display=False,
        )

        report.add_section(
            "DNS",
            dns_data,
        )

        #
        # Reverse DNS
        #

        ipv4_records = dns_data.get("A", [])

        if ipv4_records:

            ip = ipv4_records[0]

            logger.info("Running Reverse DNS lookup...")

            reverse_data = reverse_dns_tool.run(
                ip,
                silent=True,
                display=False,
            )

            report.add_section(
                "Reverse DNS",
                reverse_data,
            )

            #
            # IP Information
            #

            logger.info("Running IP Information lookup...")

            ip_data = ip_info_tool.run(
                ip,
                silent=True,
                display=False,
            )

            report.add_section(
                "IP Information",
                ip_data,
            )

        else:

            logger.warning(
                "No IPv4 address found. Reverse DNS and IP Information skipped."
            )

        #
        # Display report
        #

        report.display()
        report.export_json()

        self.finish()