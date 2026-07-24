"""
modules/information_gathering/tools/ip_info.py

IP Information Tool

Retrieves geolocation and ownership information
for an IP address using the ip-api service.
"""

from __future__ import annotations

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator


class IPInfoTool(BaseTool):
    """
    Retrieve information about an IP address.
    """

    API_URL = "http://ip-api.com/json/"

    def __init__(self) -> None:

        super().__init__("IP Information")

    def run(
        self,
        ip: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> dict[str, str]:
        """
        Retrieve IP information.
        """

        self.start(silent)

        if ip is None:
            ip = validator.get_ip()

        if display:
            print()

        results: dict[str, str] = {}

        try:

            response = requests.get(
                f"{self.API_URL}{ip}",
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("status") != "success":

                if display:
                    print(data.get("message", "Lookup failed."))

                self.finish(silent)

                return results

            results = {
                "IP Address": str(data.get("query", "")),
                "Country": str(data.get("country", "")),
                "Region": str(data.get("regionName", "")),
                "City": str(data.get("city", "")),
                "ISP": str(data.get("isp", "")),
                "Organization": str(data.get("org", "")),
                "ASN": str(data.get("as", "")),
                "Timezone": str(data.get("timezone", "")),
                "Latitude": str(data.get("lat", "")),
                "Longitude": str(data.get("lon", "")),
            }

            if display:

                print("=" * 45)
                print("           IP INFORMATION")
                print("=" * 45)

                for key, value in results.items():

                    self.print_field(key, value)

        except requests.exceptions.Timeout:

            if display:
                print("Request timed out.")

        except requests.exceptions.ConnectionError:

            if display:
                print("Unable to connect to API.")

        except requests.exceptions.HTTPError as error:

            if display:
                print(f"HTTP Error: {error}")

        except Exception as error:

            if not silent:
                logger.error(
                    f"IP lookup failed for {ip}: {error}"
                )

            if display:
                print(f"Error: {error}")

        if display:
            print()

        self.finish(silent)

        return results

    @staticmethod
    def print_field(
        name: str,
        value: str,
    ) -> None:
        """
        Print a formatted field.
        """

        print(f"{name:<15}: {value}")