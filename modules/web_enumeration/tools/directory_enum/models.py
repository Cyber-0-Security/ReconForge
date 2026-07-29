"""
Directory Enumeration Models

Shared data models used throughout the directory enumeration engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------
# Scan Configuration
# ---------------------------------------------------------


@dataclass(slots=True)
class ScanConfig:
    """
    Configuration for a directory enumeration scan.
    """

    url: str

    wordlist: str = "common.txt"

    threads: int = 50

    timeout: int = 10

    follow_redirects: bool = False

    verify_ssl: bool = True

    user_agent: str = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0.0.0 "
        "Safari/537.36"
    )

    extensions: list[str] = field(default_factory=list)

    include_status: list[int] = field(
        default_factory=lambda: [
            200,
            201,
            202,
            204,
            301,
            302,
            307,
            308,
            401,
            403,
        ]
    )

    exclude_status: list[int] = field(default_factory=list)

    retries: int = 2

    delay: float = 0.0

    recursive: bool = False

    max_depth: int = 1


# ---------------------------------------------------------
# Queue Item
# ---------------------------------------------------------


@dataclass(slots=True)
class ScanTarget:
    """
    Single path to scan.
    """

    path: str

    url: str


# ---------------------------------------------------------
# Scan Result
# ---------------------------------------------------------


@dataclass(slots=True)
class ScanResult:
    """
    Result returned from a request.
    """

    url: str

    path: str

    status: int

    length: int

    words: int

    lines: int

    content_type: str

    redirect: str | None = None

    response_time: float = 0.0


# ---------------------------------------------------------
# Wildcard Signature
# ---------------------------------------------------------


@dataclass(slots=True)
class WildcardSignature:
    """
    Signature of wildcard responses.
    """

    status: int

    length: int

    words: int

    lines: int