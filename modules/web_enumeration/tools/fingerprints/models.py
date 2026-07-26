"""
Data models used by the fingerprint engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ------------------------------------------------------------------
# Fingerprint Database Model
# ------------------------------------------------------------------


@dataclass(slots=True)
class Fingerprint:
    """
    Fingerprint patterns for one technology.
    """

    headers: list[str] = field(default_factory=list)
    html: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    css: list[str] = field(default_factory=list)
    meta: list[str] = field(default_factory=list)
    cookies: list[str] = field(default_factory=list)
    javascript: list[str] = field(default_factory=list)
    text: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Technology:
    """
    One technology loaded from the fingerprint database.
    """

    name: str
    categories: list[str]

    confidence: int = 60

    website: str = ""
    description: str = ""

    implies: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)

    versions: list[str] = field(default_factory=list)

    fingerprint: Fingerprint = field(default_factory=Fingerprint)

    requires: list[str] = field(default_factory=list)

# ------------------------------------------------------------------
# Runtime Models
# ------------------------------------------------------------------


@dataclass(slots=True)
class DetectionContext:
    """
    Everything collected from a target website.
    """

    url: str

    html: str

    headers: dict[str, Any]

    cookies: Any

    scripts: list[str]

    css: list[str]

    meta: list[str]

    text: str

    body: str


@dataclass(slots=True)
class DetectionResult:
    """
    Result returned after a successful match.
    """

    technology: Technology

    confidence: int

    version: str | None = None

    evidence: list[str] = field(default_factory=list)