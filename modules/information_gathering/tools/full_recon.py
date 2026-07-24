"""
modules/information_gathering/tools/full_recon.py

Full Recon Tool

Runs multiple information gathering tools
against a single target.
"""

from __future__ import annotations

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator

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

        logger.info("Starting Full Recon")

        whois_tool = WhoisTool()
        dns_tool = DNSLookupTool()
        reverse_dns_tool = ReverseDNSTool()
        ip_info_tool = IPInfoTool()

        print("\n========== WHOIS ==========\n")

        whois_data = whois_tool.run(target)

        print("\n========== DNS ==========\n")

        dns_data = dns_tool.run(target)

        ip = None

        if dns_data.get("A"):

            ip = dns_data["A"][0]

        if ip:

            print("\n========== REVERSE DNS ==========\n")

            reverse_dns_tool.run(ip)

            print("\n========== IP INFORMATION ==========\n")

            ip_info_tool.run(ip)

        else:

            logger.warning(
                "No IPv4 address found. Skipping Reverse DNS and IP Information."
            )

        logger.success("Full Recon completed successfully.")

        self.finish()