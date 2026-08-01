"""
Crawler Resource Extractor

Extracts page resources.
"""

from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ResourceExtractor:
    """
    Extract various resources from an HTML page.
    """

    @staticmethod
    def images(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        return [
            urljoin(base_url, tag["src"])
            for tag in soup.find_all(
                "img",
                src=True,
            )
        ]

    # ---------------------------------------------------------

    @staticmethod
    def stylesheets(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        stylesheets: list[str] = []

        for tag in soup.find_all(
            "link",
            href=True,
        ):

            rel = [
                value.lower()
                for value in tag.get("rel", [])
            ]

            if "stylesheet" in rel:

                stylesheets.append(
                    urljoin(
                        base_url,
                        tag["href"],
                    )
                )

        return stylesheets

    # ---------------------------------------------------------

    @staticmethod
    def iframes(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        return [
            urljoin(base_url, tag["src"])
            for tag in soup.find_all(
                "iframe",
                src=True,
            )
        ]

    # ---------------------------------------------------------

    @staticmethod
    def videos(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        videos: list[str] = []

        for tag in soup.find_all(
            "video",
            src=True,
        ):

            videos.append(
                urljoin(
                    base_url,
                    tag["src"],
                )
            )

        for tag in soup.find_all(
            "source",
            src=True,
        ):

            videos.append(
                urljoin(
                    base_url,
                    tag["src"],
                )
            )

        return videos

    # ---------------------------------------------------------

    @staticmethod
    def audio(
        soup: BeautifulSoup,
        base_url: str,
    ) -> list[str]:

        audio: list[str] = []

        for tag in soup.find_all(
            "audio",
            src=True,
        ):

            audio.append(
                urljoin(
                    base_url,
                    tag["src"],
                )
            )

        return audio

    # ---------------------------------------------------------

    @staticmethod
    def favicon(
        soup: BeautifulSoup,
        base_url: str,
    ) -> str | None:

        for tag in soup.find_all(
            "link",
            href=True,
        ):

            rel = [
                value.lower()
                for value in tag.get("rel", [])
            ]

            if (
                "icon" in rel
                or "shortcut icon" in " ".join(rel)
            ):

                return urljoin(
                    base_url,
                    tag["href"],
                )

        return None

    # ---------------------------------------------------------

    @staticmethod
    def canonical(
        soup: BeautifulSoup,
        base_url: str,
    ) -> str | None:

        tag = soup.find(
            "link",
            rel="canonical",
        )

        if tag and tag.get("href"):

            return urljoin(
                base_url,
                tag["href"],
            )

        return None

    # ---------------------------------------------------------

    @staticmethod
    def meta_refresh(
        soup: BeautifulSoup,
    ) -> str | None:

        tag = soup.find(
            "meta",
            attrs={
                "http-equiv": lambda value:
                    value
                    and value.lower() == "refresh"
            },
        )

        if tag:

            return tag.get(
                "content",
            )

        return None


resource_extractor = ResourceExtractor()