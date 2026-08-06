"""
HTTP Security Misconfiguration Analyzer

Analyzes HTTP response headers and identifies common
security misconfigurations.
"""

from __future__ import annotations

from .models import Misconfiguration


class MisconfigurationAnalyzer:
    """
    Analyze HTTP response headers for common
    security misconfigurations.
    """

    REQUIRED_HEADERS = {

        "Content-Security-Policy": (
            "HIGH",
            "Missing Content Security Policy (CSP). "
            "May increase the risk of XSS attacks.",
        ),

        "Strict-Transport-Security": (
            "MEDIUM",
            "Missing HSTS header. HTTPS downgrade attacks may be possible.",
        ),

        "X-Frame-Options": (
            "MEDIUM",
            "Missing X-Frame-Options. Page may be vulnerable to clickjacking.",
        ),

        "X-Content-Type-Options": (
            "LOW",
            "Missing X-Content-Type-Options. Browsers may MIME-sniff responses.",
        ),

        "Referrer-Policy": (
            "LOW",
            "Missing Referrer-Policy. Sensitive URLs may leak via Referer header.",
        ),

        "Permissions-Policy": (
            "LOW",
            "Missing Permissions-Policy header.",
        ),

        "Cross-Origin-Resource-Policy": (
            "LOW",
            "Missing Cross-Origin-Resource-Policy header.",
        ),

        "Cross-Origin-Embedder-Policy": (
            "LOW",
            "Missing Cross-Origin-Embedder-Policy header.",
        ),

        "Cross-Origin-Opener-Policy": (
            "LOW",
            "Missing Cross-Origin-Opener-Policy header.",
        ),
    }

    # ---------------------------------------------------------

    def analyze(self, response):
        """
        Analyze a HTTP response.
        """

        findings = []

        headers = response.headers

        #
        # Missing security headers
        #

        for header, (severity, description) in self.REQUIRED_HEADERS.items():

            if header not in headers:

                findings.append(

                    Misconfiguration(

                        name=header,

                        severity=severity,

                        description=description,

                    )

                )

        #
        # Information disclosure
        #

        if "Server" in headers:

            findings.append(

                Misconfiguration(

                    name="Server",

                    severity="INFO",

                    description=f"Server discloses '{headers['Server']}'",

                )

            )

        if "X-Powered-By" in headers:

            findings.append(

                Misconfiguration(

                    name="X-Powered-By",

                    severity="INFO",

                    description=f"Technology disclosure: {headers['X-Powered-By']}",

                )

            )

        if "X-AspNet-Version" in headers:

            findings.append(

                Misconfiguration(

                    name="X-AspNet-Version",

                    severity="INFO",

                    description=f"ASP.NET Version: {headers['X-AspNet-Version']}",

                )

            )

        if "X-AspNetMvc-Version" in headers:

            findings.append(

                Misconfiguration(

                    name="X-AspNetMvc-Version",

                    severity="INFO",

                    description=f"ASP.NET MVC Version: {headers['X-AspNetMvc-Version']}",

                )

            )

        #
        # CORS
        #

        cors = headers.get("Access-Control-Allow-Origin")

        if cors == "*":

            findings.append(

                Misconfiguration(

                    name="CORS",

                    severity="MEDIUM",

                    description="Wildcard Access-Control-Allow-Origin (*) detected.",

                )

            )

        #
        # Cookies
        #

        cookies = headers.get("Set-Cookie", "")

        if cookies:

            lower = cookies.lower()

            if "secure" not in lower:

                findings.append(

                    Misconfiguration(

                        name="Cookie",

                        severity="MEDIUM",

                        description="Cookie missing Secure attribute.",

                    )

                )

            if "httponly" not in lower:

                findings.append(

                    Misconfiguration(

                        name="Cookie",

                        severity="MEDIUM",

                        description="Cookie missing HttpOnly attribute.",

                    )

                )

            if "samesite" not in lower:

                findings.append(

                    Misconfiguration(

                        name="Cookie",

                        severity="LOW",

                        description="Cookie missing SameSite attribute.",

                    )

                )

        #
        # Cache-Control
        #

        cache = headers.get("Cache-Control", "").lower()

        if cache:

            if "no-store" not in cache and "private" not in cache:

                findings.append(

                    Misconfiguration(

                        name="Cache-Control",

                        severity="LOW",

                        description="Sensitive responses may be cached.",

                    )

                )

        #
        # Duplicate findings
        #

        unique = {}

        for finding in findings:

            key = (
                finding.name,
                finding.description,
            )

            unique[key] = finding

        return sorted(

            unique.values(),

            key=lambda item: (
                {
                    "HIGH": 0,
                    "MEDIUM": 1,
                    "LOW": 2,
                    "INFO": 3,
                }.get(item.severity, 99),
                item.name,
            ),

        )


misconfiguration_analyzer = MisconfigurationAnalyzer()