"""
modules/web_enumeration/tools/technology_detection.py

Advanced Technology Detection Tool
Detects web technologies using multiple fingerprint sources.
"""

from __future__ import annotations

import json
import re
import glob
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import requests

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator
from core.report import Report
from modules.web_enumeration.tools.fingerprints.challenge import detect_challenge_page


#
# Bounds for fetching external script file contents. Wappalyzer-style
# tools get much of their JS-library detection from the *contents* of
# bundled JS files, not just their URLs/filenames - a hashed webpack
# chunk name tells you nothing, but the code inside it often does.
# These limits keep that from turning into an unbounded crawl.
#
MAX_SCRIPTS_TO_FETCH = 8
MAX_SCRIPT_BYTES = 300_000
SCRIPT_FETCH_TIMEOUT = 6


# ---- Only truly mutually exclusive categories ----
# (You can't run two different CMSs or two different e-commerce platforms)
STRICTLY_MUTUALLY_EXCLUSIVE = {
    "CMS": ["WordPress", "Shopify", "Magento", "Drupal", "Joomla", "Wix", "Squarespace", "Weebly", "Jimdo", "Blogger", "TYPO3", "Umbraco", "Craft CMS", "October CMS", "ExpressionEngine", "OpenCart", "PrestaShop", "MediaWiki", "DotNetNuke", "SilverStripe", "Adobe Experience Manager", "Tumblr", "Ghost CMS", "Webflow", "Strapi", "HubSpot CMS", "Concrete CMS", "Contentful", "Sanity"],
    "Ecommerce": ["Shopify", "Magento", "WooCommerce", "BigCommerce", "Salesforce Commerce Cloud"],
}


class TechnologyDetectionTool(BaseTool):
    """
    Detect web technologies (frameworks, libraries, servers, etc.)
    using fingerprint JSON files.
    """

    def __init__(self) -> None:
        super().__init__("Technology Detection")
        self.techs = self._load_fingerprints()
        self._precompile_patterns()

    def _load_fingerprints(self) -> List[Dict]:
        """Load all technology fingerprints from JSON files."""
        techs = []
        pattern = "modules/web_enumeration/tools/fingerprints/fingerprint_jsons/*.json"
        for json_file in glob.glob(pattern):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    techs.extend(data.get("technologies", []))
            except Exception as e:
                logger.error(f"Failed to load {json_file}: {e}")
        return techs

    def _precompile_patterns(self) -> None:
        """Convert regex strings (starting with 're:') into compiled regex objects."""
        for tech in self.techs:
            for f_type, patterns in tech.get("fingerprints", {}).items():
                compiled = []
                for p in patterns:
                    if p.startswith("re:"):
                        try:
                            compiled.append(re.compile(p[3:], re.IGNORECASE))
                        except re.error:
                            logger.warning(f"Invalid regex in {tech['name']}: {p}")
                            compiled.append(p)  # fallback to literal
                    else:
                        compiled.append(p)
                tech["fingerprints"][f_type] = compiled

            # Also compile version patterns
            version_config = tech.get("version", {})
            for source, patterns in version_config.items():
                compiled = []
                for p in patterns:
                    if p.startswith("re:"):
                        try:
                            compiled.append(re.compile(p[3:], re.IGNORECASE))
                        except re.error:
                            compiled.append(p)
                    else:
                        compiled.append(p)
                tech["version"][source] = compiled

    def _extract_data(
        self,
        html: str,
        headers: Dict,
        cookies: Dict,
        scripts: List[str],
        script_contents: List[str],
    ) -> Dict[str, List[str]]:
        """Extract all searchable content from the target."""
        data = {
            "html": [html],
            "scripts": scripts,   # list of script src URLs
            "script_content": script_contents,  # actual fetched JS bodies
            "meta": re.findall(r'<meta[^>]+>', html, re.IGNORECASE),
            "headers": [f"{k}: {v}" for k, v in headers.items()],
            "cookies": [f"{k}={v}" for k, v in cookies.items()],
            "css": re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="[^"]+"', html, re.IGNORECASE),
            "text": [self._strip_tags(html)],
        }
        return data

    @staticmethod
    def _strip_tags(html: str) -> str:
        """
        Reduce HTML to plain visible-ish text, so 'text' fingerprints
        (e.g. a brand name that only appears in body copy) actually
        have something to search against, instead of always being
        empty.
        """

        without_scripts = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        without_tags = re.sub(r"<[^>]+>", " ", without_scripts)

        return re.sub(r"\s+", " ", without_tags).strip()

    def _fetch_script_contents(
        self,
        base_url: str,
        script_srcs: List[str],
        headers: Dict[str, str],
    ) -> List[str]:
        """
        Download the actual contents of a bounded number of linked
        script files. This is what makes JS-library/framework
        detection possible for bundled production sites, where the
        filename itself (e.g. main.a1b2c3.js) carries no information
        but the code inside it does.
        """

        bodies: List[str] = []

        candidates = []

        for src in script_srcs:

            parsed = urlparse(src)

            if parsed.scheme in ("data", "blob"):
                continue

            absolute = urljoin(base_url, src)
            candidates.append(absolute)

        for script_url in candidates[:MAX_SCRIPTS_TO_FETCH]:

            try:

                resp = requests.get(
                    script_url,
                    timeout=SCRIPT_FETCH_TIMEOUT,
                    headers=headers,
                    stream=True,
                )

                chunk = resp.raw.read(
                    MAX_SCRIPT_BYTES,
                    decode_content=True,
                )

                bodies.append(
                    chunk.decode("utf-8", errors="ignore")
                )

            except requests.RequestException:

                #
                # A single unreachable/slow script shouldn't stop
                # the whole scan - just skip it.
                #

                continue

        return bodies

    def _match_pattern(self, pattern: Any, text: str) -> bool:
        """Check if pattern (literal or compiled regex) matches text."""
        if isinstance(pattern, re.Pattern):
            return pattern.search(text) is not None
        else:
            return pattern.lower() in text.lower()

    def _compute_confidence(self, tech: Dict, matches: Dict[str, bool]) -> int:
        """Calculate dynamic confidence based on number and variety of matches."""
        base = tech.get("confidence", 60)
        total_types = len(tech.get("fingerprints", {}))
        match_count = sum(1 for v in matches.values() if v)

        bonus = 0
        if total_types > 0:
            ratio = match_count / total_types
            if ratio >= 0.75:
                bonus = 15
            elif ratio >= 0.5:
                bonus = 10
            elif ratio >= 0.25:
                bonus = 5

        # Extra bonus if multiple types matched (more reliable)
        if match_count >= 2:
            bonus += 5

        return min(base + bonus, 100)

    def _extract_version(self, tech: Dict, data: Dict[str, str]) -> Optional[str]:
        """Extract version from any source using pre-compiled patterns."""
        version_config = tech.get("version", {})
        if not version_config:
            return None

        # Flatten data into a single string per source (join lists)
        flat_data = {}
        for source, items in data.items():
            if isinstance(items, list):
                flat_data[source] = " ".join(items)
            else:
                flat_data[source] = items

        for source, patterns in version_config.items():
            content = flat_data.get(source, "")
            if not content:
                continue
            for pattern in patterns:
                if isinstance(pattern, re.Pattern):
                    match = pattern.search(content)
                    if match:
                        # Assume version is first capture group
                        return match.group(1) if match.groups() else "unknown"
                else:
                    if pattern in content:
                        return "unknown"  # present but no exact version
        return None

    def _detect(self, html: str, headers: Dict, cookies: Dict, scripts: List[str]) -> List[Dict]:
        """Run detection against all technologies and return list of results."""
        data = self._extract_data(html, headers, cookies, scripts, script_contents=[])
        return self._detect_from_data(data)

    def _detect_from_data(self, data: Dict[str, List[str]]) -> List[Dict]:
        """Run detection against all technologies using an already-built data dict."""
        results = []

        for tech in self.techs:
            matches = {}
            fingerprints = tech.get("fingerprints", {})
            if not fingerprints:
                continue

            for f_type, patterns in fingerprints.items():
                matched = False
                content_list = data.get(f_type, [])
                if not content_list:
                    matches[f_type] = False
                    continue
                for pattern in patterns:
                    for piece in content_list:
                        if self._match_pattern(pattern, piece):
                            matched = True
                            break
                    if matched:
                        break
                matches[f_type] = matched

            # Require at least 1 different fingerprint types to match
            if sum(matches.values()) < 1:
                continue

            confidence = self._compute_confidence(tech, matches)
            if confidence < 70:   # threshold to filter weak signals
                continue

            version = self._extract_version(tech, data)

            results.append({
                "name": tech["name"],
                "category": tech.get("category", "Unknown"),
                "confidence": confidence,
                "version": version,
            })

        # ---- Deduplicate ----
        deduped = {}
        for res in results:
            name = res["name"]
            if name not in deduped or res["confidence"] > deduped[name]["confidence"]:
                deduped[name] = res
        results = list(deduped.values())

        # ---- Mutual Exclusivity (Only for CMS and Ecommerce) ----
        by_category = {}
        for res in results:
            cat = res.get('category', 'Unknown')
            by_category.setdefault(cat, []).append(res)

        for cat, exclusive_list in STRICTLY_MUTUALLY_EXCLUSIVE.items():
            if cat in by_category:
                candidates = [r for r in by_category[cat] if r['name'] in exclusive_list]
                if len(candidates) > 1:
                    best = max(candidates, key=lambda x: x['confidence'])
                    for r in candidates:
                        if r is not best:
                            results.remove(r)

        # ---- Sort by confidence ----
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results

    def run(
        self,
        url: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> Dict[str, Any]:
        """
        Run technology detection on a given URL.

        Args:
            url: Target URL (with or without scheme). If None, prompted interactively.
            silent: Suppress logs and non-essential output.
            display: Show results on stdout.
        """
        self.start(silent)

        if url is None:
            from urllib.parse import urlparse
            while True:
                raw = input("Enter target URL or domain (e.g., example.com or https://example.com): ").strip()
                if not raw:
                    print("Please enter a valid URL or domain.")
                    continue
                parsed = urlparse(raw)
                if not parsed.scheme:
                    raw = "https://" + raw
                    parsed = urlparse(raw)
                if parsed.netloc:
                    url = raw
                    break
                else:
                    print("Invalid URL or domain. Please try again.")
        else:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "https://" + url

        if display:
            print(f"\n[+] Scanning {url} for technologies...")

        # Realistic browser headers to avoid 403
        request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        try:
            response = requests.get(url, timeout=15, allow_redirects=True, headers=request_headers)
            response.raise_for_status()
            html = response.text
            headers = dict(response.headers)
            cookies = response.cookies.get_dict()
            scripts = re.findall(r'<script[^>]+src="([^"]+)"', html, re.IGNORECASE)

            logger.info(
                f"Received {response.status_code} response "
                f"({len(response.content)} bytes, {len(scripts)} scripts found)"
            )

            challenge = detect_challenge_page(response.status_code, html)

            if challenge:
                logger.warning(
                    f"Response looks like a {challenge} "
                    "challenge/block page, not real site content"
                )

            script_contents = self._fetch_script_contents(
                response.url,
                scripts,
                request_headers,
            )

            data = self._extract_data(html, headers, cookies, scripts, script_contents)
            results = self._detect_from_data(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            if display:
                print(f"Error: {e}")
            self.finish(silent)
            return {"technologies": [], "error": str(e)}

        if display:
            print(f"\n[+] Detected {len(results)} technologies")

            if challenge:
                print(
                    f"⚠ This response looks like a {challenge} - "
                    "detected technologies below may be inaccurate "
                    "or incomplete as a result."
                )

            report = Report()
            report.add_section("Technology Detection", results)
            report.display()

        self.finish(silent)
        return {"technologies": results, "url": url}