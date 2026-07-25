"""
modules/information_gathering/tools/subdomain_enum.py

Passive Subdomain Enumeration Tool.

Queries multiple passive sources and merges
the results into a deduplicated subdomain list.
"""

from __future__ import annotations

import csv
import io
import re
from typing import Any

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.utils import separator
from core.validator import validator


class SubdomainEnumerationTool(BaseTool):
    """
    Discover subdomains using passive sources.
    """

    REQUEST_HEADERS = {
        "User-Agent": "ReconForge/1.0",
    }

    HOSTNAME_RE = re.compile(
        r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
        r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        super().__init__("Subdomain Enumeration")

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> list[str]:
        """
        Enumerate subdomains from multiple passive sources.
        """

        self.start(silent)

        if target is None:
            target = validator.get_domain()

        target = self._normalize_domain(target)

        if not silent:
            logger.info(f"Searching passive sources for {target}")

        source_results: dict[str, set[str]] = {
            "AlienVault": set(),
            "BufferOver": set(),
            "HackerTarget": set(),
        }

        source_status: dict[str, str] = {
            "AlienVault": "Pending",
            "BufferOver": "Pending",
            "HackerTarget": "Pending",
        }

        fetchers = (
            ("AlienVault", self.fetch_alienvault),
            ("BufferOver", self.fetch_bufferover),
            ("HackerTarget", self.fetch_hackertarget),
        )

        merged: dict[str, set[str]] = {}

        for source_name, fetcher in fetchers:

            try:
                found = fetcher(target, silent=silent)
                source_results[source_name] = found
                source_status[source_name] = "OK"

                for subdomain in found:
                    merged.setdefault(subdomain, set()).add(source_name)

            except Exception as error:
                source_results[source_name] = set()
                source_status[source_name] = "Failed"

                if not silent:
                    logger.warning(
                        f"{source_name} lookup failed for {target}: {error}"
                    )

        results = sorted(merged)

        if display:
            print()
            print(separator())
            print("SUBDOMAIN ENUMERATION")
            print(separator())
            print(f"Target : {target}")
            print()

            print(f"{'Source':<20}{'Status':<10}{'Found'}")
            print(f"{'-' * 20}{'-' * 10}{'-' * 5}")

            for source_name in ("AlienVault", "BufferOver", "HackerTarget"):
                print(
                    f"{source_name:<20}"
                    f"{source_status[source_name]:<10}"
                    f"{len(source_results[source_name])}"
                )

            print(f"{'Unique':<20}{'':<10}{len(results)}")
            print()

            if results:
                for index, subdomain in enumerate(results, start=1):
                    print(f"{index}. {subdomain}")
            else:
                print("No subdomains found.")

            print()

        self.finish(silent)

        return results

    def fetch_alienvault(
        self,
        target: str,
        silent: bool = False,
    ) -> set[str]:
        """
        Fetch subdomains from AlienVault OTX passive DNS.
        """

        url = (
            "https://otx.alienvault.com/api/v1/indicators/"
            f"domain/{target}/passive_dns"
        )

        response = requests.get(
            url,
            headers=self.REQUEST_HEADERS,
            timeout=20,
        )
        response.raise_for_status()

        payload = response.json()
        return self._extract_subdomains(payload, target)

    def fetch_bufferover(
        self,
        target: str,
        silent: bool = False,
    ) -> set[str]:
        """
        Fetch subdomains from BufferOver passive DNS.
        """

        url = f"https://dns.bufferover.run/dns?q=.{target}"

        response = requests.get(
            url,
            headers=self.REQUEST_HEADERS,
            timeout=20,
        )
        response.raise_for_status()

        payload = response.json()
        return self._extract_subdomains(payload, target)

    def fetch_hackertarget(
        self,
        target: str,
        silent: bool = False,
    ) -> set[str]:
        """
        Fetch subdomains from HackerTarget hostsearch.
        """

        url = f"https://api.hackertarget.com/hostsearch/?q={target}"

        response = requests.get(
            url,
            headers=self.REQUEST_HEADERS,
            timeout=20,
        )
        response.raise_for_status()

        text = response.text.strip()

        if not text:
            return set()

        if text.lower().startswith(("error", "api count", "invalid")):
            raise RuntimeError(text)

        results: set[str] = set()

        reader = csv.reader(io.StringIO(text))

        for row in reader:
            for cell in row:
                candidate = self._normalize_candidate(cell, target)
                if candidate:
                    results.add(candidate)

        return results

    def _extract_subdomains(
        self,
        payload: Any,
        target: str,
    ) -> set[str]:
        """
        Recursively extract hostname-like strings from a JSON payload.
        """

        results: set[str] = set()
        self._walk_payload(payload, target, results)
        return results

    def _walk_payload(
        self,
        value: Any,
        target: str,
        results: set[str],
    ) -> None:
        """
        Walk nested JSON-like data and collect matching hostnames.
        """

        if isinstance(value, dict):

            for item in value.values():
                self._walk_payload(item, target, results)

        elif isinstance(value, (list, tuple, set)):

            for item in value:
                self._walk_payload(item, target, results)

        elif isinstance(value, str):

            for line in value.splitlines():
                candidate = self._normalize_candidate(line, target)
                if candidate:
                    results.add(candidate)

    def _normalize_domain(self, domain: str) -> str:
        """
        Normalise a domain name.
        """

        domain = domain.strip().lower()

        if "://" in domain:
            domain = domain.split("://", 1)[1]

        domain = domain.split("/", 1)[0]
        domain = domain.split(":", 1)[0]
        domain = domain.rstrip(".")

        return domain

    def _normalize_candidate(
        self,
        candidate: str,
        target: str,
    ) -> str | None:
        """
        Convert a raw string into a normalised subdomain if possible.
        """

        candidate = candidate.strip().strip('"').strip("'")

        if not candidate:
            return None

        target = self._normalize_domain(target)

        for part in candidate.split(","):

            part = part.strip().lower()
            part = part.rstrip(".")
            part = part.strip("[](){}<>")

            if part.startswith("*."):
                part = part[2:]

            part = part.strip()

            if not part:
                continue

            if part == target:
                continue

            if not part.endswith(target):
                continue

            if not self._looks_like_hostname(part):
                continue

            return part

        return None

    def _looks_like_hostname(self, value: str) -> bool:
        """
        Check whether a string looks like a hostname.
        """

        return bool(self.HOSTNAME_RE.fullmatch(value))