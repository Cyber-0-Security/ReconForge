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

    def run(self) -> None:

        self.start()

        ip = validator.get_ip()

        print()

        try:

            response = requests.get(
                f"{self.API_URL}{ip}",
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("status") != "success":

                print(data.get("message", "Lookup failed."))

                self.finish()

                return

            print("=" * 45)
            print("           IP INFORMATION")
            print("=" * 45)

            self.print_field("IP Address", data.get("query"))
            self.print_field("Country", data.get("country"))
            self.print_field("Region", data.get("regionName"))
            self.print_field("City", data.get("city"))
            self.print_field("ISP", data.get("isp"))
            self.print_field("Organization", data.get("org"))
            self.print_field("ASN", data.get("as"))
            self.print_field("Timezone", data.get("timezone"))
            self.print_field("Latitude", data.get("lat"))
            self.print_field("Longitude", data.get("lon"))

        except requests.exceptions.Timeout:

            print("Request timed out.")

        except requests.exceptions.ConnectionError:

            print("Unable to connect to API.")

        except requests.exceptions.HTTPError as error:

            print(f"HTTP Error: {error}")

        except Exception as error:

            logger.error(f"IP lookup failed for {ip}: {error}")

            print(f"Error: {error}")

        print()

        self.finish()

    @staticmethod
    def print_field(name: str, value) -> None:

        print(f"{name:<15}: {value}")