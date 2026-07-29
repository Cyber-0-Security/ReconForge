"""
Directory Enumeration Tool

Entry point for the directory enumeration engine.
"""

from __future__ import annotations

from core.base_tool import BaseTool
from core.logger import logger
from core.validator import validator

from modules.web_enumeration.tools.directory_enum.engine import engine
from modules.web_enumeration.tools.directory_enum.formatter import print_results
from modules.web_enumeration.tools.directory_enum.models import ScanConfig


class DirectoryEnumerationTool(BaseTool):
    """
    Directory Enumeration Tool.
    """

    def __init__(self) -> None:

        super().__init__("Directory Enumeration")

    def run(
        self,
        target: str | None = None,
        silent: bool = False,
        display: bool = True,
    ) -> list:
        """
        Execute directory enumeration.
        """

        self.start(silent)

        if target is None:

            target = validator.get_domain()

        wordlist = input(
            "Wordlist [common.txt]: "
        ).strip()

        if not wordlist:

            wordlist = "common.txt"

        extensions = input(
            "Extensions (comma separated, optional): "
        ).strip()

        extension_list = []

        if extensions:

            extension_list = [

                extension.strip()

                for extension in extensions.split(",")

                if extension.strip()

            ]

        config = ScanConfig(

            url=self._normalize_url(target),

            wordlist=wordlist,

            extensions=extension_list,

        )

        logger.info("Starting directory enumeration...")

        results = engine.scan(config)

        if display:

            print_results(results)

        self.finish(silent)

        return results

    @staticmethod
    def _normalize_url(
        target: str,
    ) -> str:
        """
        Ensure the target contains a scheme.
        """

        target = target.strip()

        if target.startswith(
            (
                "http://",
                "https://",
            )
        ):

            return target

        return f"https://{target}"