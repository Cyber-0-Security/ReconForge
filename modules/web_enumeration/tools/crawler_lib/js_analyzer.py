"""
JavaScript Analyzer

Downloads and analyzes JavaScript resources for recon intelligence.
"""

from __future__ import annotations

import re
from urllib.parse import urljoin

import requests
from .models import JavaScriptAnalysis

class JavaScriptAnalyzer:
    """
    Analyze JavaScript files for endpoints, secrets and other
    reconnaissance artifacts.
    """

    TIMEOUT = 8

    MAX_FILE_SIZE = 1024 * 1024  # 1 MB

    ENDPOINT_PATTERNS = (

        #
        # fetch()
        #
        r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]',

        #
        # axios.get/post/etc.
        #
        r'axios\.(?:get|post|put|patch|delete|head|options)\s*\(\s*[\'"]([^\'"]+)[\'"]',

        #
        # axios({...})
        #
        r'axios\s*\(\s*\{[^}]*url\s*:\s*[\'"]([^\'"]+)[\'"]',

        #
        # $.ajax()
        #
        r'\$\.ajax\s*\(\s*\{[^}]*url\s*:\s*[\'"]([^\'"]+)[\'"]',

        #
        # XMLHttpRequest.open()
        #
        r'\.open\s*\(\s*[\'"][A-Z]+[\'"]\s*,\s*[\'"]([^\'"]+)[\'"]',

        #
        # Generic URL assignments
        #
        r'\burl\s*[:=]\s*[\'"]([^\'"]+)[\'"]',

        r'\bendpoint\s*[:=]\s*[\'"]([^\'"]+)[\'"]',

        r'\bapi(?:Url|URL)?\s*[:=]\s*[\'"]([^\'"]+)[\'"]',

        r'\bbaseUrl\s*[:=]\s*[\'"]([^\'"]+)[\'"]',

        #
        # React Router
        #
        r'path\s*:\s*[\'"]([^\'"]+)[\'"]',

        #
        # Express routes
        #
        r'app\.(?:get|post|put|delete|patch|use)\s*\(\s*[\'"]([^\'"]+)[\'"]',

        #
        # Router routes
        #
        r'router\.(?:get|post|put|delete|patch|use)\s*\(\s*[\'"]([^\'"]+)[\'"]',

        #
        # Fastify
        #
        r'fastify\.(?:get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',

        #
        # Next.js rewrites
        #
        r'destination\s*:\s*[\'"]([^\'"]+)[\'"]',

        #
        # Absolute REST endpoints
        #
        r'https?://[^\'"]+/api[^\'"]*',

        #
        # Relative API paths
        #
        r'([\'"])(/api/[^\'"]+)\1',

        r'([\'"])(/v[0-9]+/[^\'"]+)\1',

        r'([\'"])(/graphql)\1',

        r'([\'"])(/rest/[^\'"]+)\1',

    )

    GRAPHQL_PATTERNS = (
        r"/graphql",
        r"graphql",
    )

    WEBSOCKET_PATTERNS = (
        r"wss://[^\s\"']+",
        r"ws://[^\s\"']+",
    )

    BUCKET_PATTERNS = (
        r"https://[A-Za-z0-9.-]+\.s3\.amazonaws\.com[^\s\"']*",
        r"https://storage\.googleapis\.com/[^\s\"']+",
        r"https://[A-Za-z0-9.-]+\.blob\.core\.windows\.net[^\s\"']*",
    )

    SECRET_PATTERNS = (

        #
        # Google
        #
        r"AIza[0-9A-Za-z\-_]{35}",

        #
        # AWS
        #
        r"AKIA[0-9A-Z]{16}",
        r"ASIA[0-9A-Z]{16}",

        #
        # GitHub
        #
        r"ghp_[A-Za-z0-9]{36}",
        r"github_pat_[A-Za-z0-9_]+",

        #
        # Stripe
        #
        r"sk_live_[A-Za-z0-9]+",
        r"pk_live_[A-Za-z0-9]+",

        #
        # Slack
        #
        r"xox[baprs]-[A-Za-z0-9-]+",

        #
        # Twilio
        #
        r"SK[0-9a-fA-F]{32}",

        #
        # Firebase
        #
        r"AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}",

        #
        # JWT
        #
        r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9._-]+\.[A-Za-z0-9._-]+",

        #
        # Bearer
        #
        r"Bearer\s+[A-Za-z0-9\-._~+/]+=*",

        #
        # Basic Auth
        #
        r"Basic\s+[A-Za-z0-9+/]+=*",

    )

    COMMENT_PATTERNS = (
        r"TODO",
        r"FIXME",
        r"HACK",
        r"BUG",
    )

    # ---------------------------------------------------------

    def fetch(
        self,
        url: str,
        verify_ssl: bool = True,
        user_agent: str | None = None,
    ) -> str | None:
        """
        Download a JavaScript file.
        """

        headers = {}

        if user_agent:
            headers["User-Agent"] = user_agent

        try:

            response = requests.get(
                url,
                timeout=self.TIMEOUT,
                verify=verify_ssl,
                headers=headers,
            )

            if response.status_code != 200:
                return None

            if len(response.content) > self.MAX_FILE_SIZE:
                return None

            return response.text

        except requests.RequestException:

            return None

    # ---------------------------------------------------------

    def analyze(
        self,
        javascript: str,
        base_url: str = "",
    ) -> JavaScriptAnalysis:
        """
        Analyze JavaScript source.
        """

        return JavaScriptAnalysis(

            endpoints=self.extract_endpoints(
                javascript,
                base_url,
            ),

            graphql=self.extract_graphql(
                javascript,
            ),

            websockets=self.extract_websockets(
                javascript,
            ),

            secrets=self.extract_secrets(
                javascript,
            ),

            cloud_buckets=self.extract_buckets(
                javascript,
            ),

            comments=self.extract_comments(
                javascript,
            ),

        )

    # ---------------------------------------------------------

    def extract_endpoints(
        self,
        javascript: str,
        base_url: str = "",
    ) -> list[str]:
        """
        Extract API endpoints.
        """

        endpoints = set()

        for pattern in self.ENDPOINT_PATTERNS:

            for match in re.findall(
                pattern,
                javascript,
                re.DOTALL,
            ):

                if isinstance(match, tuple):

                    match = next(
                        (m for m in match if m),
                        "",
                    )

                match = match.strip()

                if not match:
                    continue

                #
                # Ignore obvious non-endpoints
                #

                if match.startswith(("javascript:", "mailto:", "#")):
                    continue

                #
                # Ignore static assets
                #

                if match.endswith((
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".svg",
                    ".css",
                    ".woff",
                    ".woff2",
                    ".ttf",
                )):
                    continue

                endpoints.add(
                    urljoin(
                        base_url,
                        match,
                    )
                )

        return sorted(

            endpoints,

            key=lambda endpoint: (

                "/api/" not in endpoint,

                "/graphql" not in endpoint,

                endpoint,

            ),

        )

    # ---------------------------------------------------------

    def extract_graphql(
        self,
        javascript: str,
    ) -> list[str]:
        """
        Detect GraphQL usage.
        """

        findings = set()

        for pattern in self.GRAPHQL_PATTERNS:

            for match in re.findall(
                pattern,
                javascript,
                re.IGNORECASE,
            ):

                findings.add(match)

        return sorted(findings)

    # ---------------------------------------------------------

    def extract_websockets(
        self,
        javascript: str,
    ) -> list[str]:
        """
        Extract WebSocket endpoints.
        """

        findings = set()

        for pattern in self.WEBSOCKET_PATTERNS:

            findings.update(
                re.findall(
                    pattern,
                    javascript,
                )
            )

        return sorted(findings)

    # ---------------------------------------------------------

    def extract_buckets(
        self,
        javascript: str,
    ) -> list[str]:
        """
        Extract cloud storage bucket URLs.
        """

        findings = set()

        for pattern in self.BUCKET_PATTERNS:

            findings.update(
                re.findall(
                    pattern,
                    javascript,
                )
            )

        return sorted(findings)

    # ---------------------------------------------------------

    def extract_secrets(
        self,
        javascript: str,
    ) -> list[str]:
        """
        Detect secrets.
        """

        findings = []

        mapping = {

            "AIza": "Google API Key",

            "AKIA": "AWS Access Key",

            "ASIA": "AWS Temporary Key",

            "ghp_": "GitHub Token",

            "github_pat_": "GitHub PAT",

            "sk_live_": "Stripe Secret",

            "pk_live_": "Stripe Public",

            "xox": "Slack Token",

            "SK": "Twilio",

            "AAAA": "Firebase",

            "eyJ": "JWT",

            "Bearer": "Bearer Token",

            "Basic": "Basic Auth",

        }

        for pattern in self.SECRET_PATTERNS:

            for match in re.findall(pattern, javascript):

                secret_type = "Unknown"

                for prefix, label in mapping.items():

                    if match.startswith(prefix):

                        secret_type = label

                        break

                findings.append(
                    f"{secret_type}: {match}"
                )

        return sorted(set(findings))

    # ---------------------------------------------------------

    def extract_comments(
        self,
        javascript: str,
    ) -> list[str]:
        """
        Detect interesting developer comments.
        """

        findings = []

        comments = re.findall(
            r"/\*.*?\*/|//.*?$",
            javascript,
            re.MULTILINE | re.DOTALL,
        )

        for comment in comments:

            upper = comment.upper()

            if any(
                keyword in upper
                for keyword in self.COMMENT_PATTERNS
            ):
                findings.append(comment.strip())

        return findings


javascript_analyzer = JavaScriptAnalyzer()