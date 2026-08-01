"""
Crawler Filters

Filters extracted URLs before they are added to the crawl queue.
"""

from __future__ import annotations

from urllib.parse import (
    parse_qsl,
    urlencode,
    urlparse,
    urlunparse,
)

from .models import (
    CrawlConfig,
    Link,
)


class CrawlFilters:
    """
    Filters discovered links.
    """

    STATIC_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp",
    ".css", ".js", ".map",
    ".pdf", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz",
    ".7z", ".rar",
    ".mp3", ".wav", ".ogg",
    ".mp4", ".avi", ".mov", ".wmv", ".mkv", ".webm",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".exe", ".dll", ".iso", ".dmg", ".pkg", ".msi",
    ".apk", ".ipa",
    ".bin", ".img",
    }

    TRACKING_PARAMETERS = {
        "fbclid",
        "gclid",
        "msclkid",
        "mc_cid",
        "mc_eid",
    }
    SESSION_PARAMETERS = {
    "phpsessid",
    "jsessionid",
    "aspsessionid",
    "sid",
    "sessionid",
    }
    LOGOUT_KEYWORDS = (
    "logout",
    "signout",
    "logoff",
    )
    # ---------------------------------------------------------
    @staticmethod
    def _is_data(url: str) -> bool:

        return url.lower().startswith("data:")
    @classmethod
    def _is_logout(
        cls,
        url: str,
    ) -> bool:

        lowered = url.lower()

        return any(
            keyword in lowered
            for keyword in cls.LOGOUT_KEYWORDS
        )
    @staticmethod
    def _is_blob(url: str) -> bool:

        return url.lower().startswith("blob:")
    @staticmethod
    def _is_calendar(url: str) -> bool:

        lowered = url.lower()

        return (
            "/calendar/" in lowered
            or "/archive/" in lowered
            or "year=" in lowered
            or "month=" in lowered
            or "day=" in lowered
            or "date=" in lowered
        )
    def is_valid(
        self,
        link: Link,
        config: CrawlConfig,
    ) -> tuple[bool, str]:
        """
        Validate a discovered URL.

        Returns:
            (True, "ok")
            (False, "<reason>")
        """
        
        # Normalize before validation
        link.url = self.normalize(link.url)

        url = link.url

        if not url:
            return False, "empty"

        if self._is_fragment(url):
            return False, "fragment"

        if self._is_mail(url):
            return False, "mailto"

        if self._is_tel(url):
            return False, "telephone"

        if self._is_javascript(url):
            return False, "javascript"
        
        if self._is_data(url):
            return False, "data"
        
        if self._is_template(url):
            return False, "template"

        if self._is_external(url, config):
            return False, "external"

        if self._is_static_file(url):
            return False, "static"
        if self._is_logout(url):
            return False, "logout"
        if self._is_calendar(url):
            return False, "calendar"
        if self._is_blob(url):
            return False, "blob"
        return True, "ok"

    # ---------------------------------------------------------

    def normalize(self, url: str) -> str:
        """
        Normalize URLs before duplicate detection.

        This intentionally performs only safe normalization.
        """

        url = url.strip()

        if not url:
            return ""

        parsed = urlparse(url)

        # Normalize scheme and hostname
        scheme = parsed.scheme.lower()

        hostname = parsed.hostname.lower() if parsed.hostname else ""

        port = parsed.port

        # Remove default ports
        if (
            scheme == "http" and port == 80
        ) or (
            scheme == "https" and port == 443
        ):
            port = None

        netloc = hostname if port is None else f"{hostname}:{port}"

        # Remove fragment
        fragment = ""

        # Remove tracking/session parameters
        cleaned_query = []

        for key, value in parse_qsl(parsed.query, keep_blank_values=True):

            key_lower = key.lower()

            if key_lower.lower().startswith("utm_"):
                continue

            if (
                key_lower in self.TRACKING_PARAMETERS
                or key_lower in self.SESSION_PARAMETERS
            ):
                continue

            cleaned_query.append((key, value))

        query = urlencode(cleaned_query, doseq=True)

        # Normalize path
        path = parsed.path

        if path != "/":
            path = path.rstrip("/")

        while "//" in path:
            path = path.replace("//", "/")

        return urlunparse(
            (
                scheme,
                netloc,
                path,
                parsed.params,
                query,
                fragment,
            )
        )

    # ---------------------------------------------------------

    @staticmethod
    def _is_template(url: str) -> bool:
        """
        Reject wildcard/template URLs.
        """

        lowered = url.lower()

        markers = (
            "*",
            "{",
            "}",
            "<",
            ">",
            ":id",
            "${",
        )

        return any(marker in lowered for marker in markers)

    # ---------------------------------------------------------

    @staticmethod
    def _is_fragment(
        url: str,
    ) -> bool:

        return url.lower().startswith("#")

    # ---------------------------------------------------------

    @staticmethod
    def _is_mail(
        url: str,
    ) -> bool:

        return url.lower().lower().startswith("mailto:")

    # ---------------------------------------------------------

    @staticmethod
    def _is_tel(
        url: str,
    ) -> bool:

        return url.lower().startswith("tel:")

    # ---------------------------------------------------------

    @staticmethod
    def _is_javascript(
        url: str,
    ) -> bool:

        return url.lower().startswith("javascript:")

    # ---------------------------------------------------------

    def _is_external(
        self,
        url: str,
        config: CrawlConfig,
    ) -> bool:
        """
        Return True only if the URL is outside the allowed scope.
        """

        target = urlparse(config.url)
        parsed = urlparse(url)

        if not parsed.netloc:
            return False

        target_host = self._strip_www(target.netloc.lower())
        host = self._strip_www(parsed.netloc.lower())

        if host == target_host:
            return False

        if config.include_subdomains:
            if host.endswith("." + target_host):
                return False

        return True

    # ---------------------------------------------------------

    @staticmethod
    def _strip_www(host: str) -> str:

        if host.lower().startswith("www."):
            return host[4:]

        return host

    # ---------------------------------------------------------

    def _is_static_file(
        self,
        url: str,
    ) -> bool:

        path = urlparse(url).path.lower()

        for extension in self.STATIC_EXTENSIONS:

            if path.endswith(extension):
                return True

        return False


filters = CrawlFilters()