"""
Configuration loader.
"""

from __future__ import annotations

from pathlib import Path

from core.config.models import ProjectConfig
from core.config.parser import JsonParser
from core.shared.exceptions import ConfigurationError


class ConfigLoader:

    def load(
        self,
        path: Path,
    ) -> ProjectConfig:

        if not path.exists():

            raise ConfigurationError(
                f"Configuration file not found: {path}"
            )

        if not path.is_file():

            raise ConfigurationError(
                f"Expected a file: {path}"
            )

        if path.suffix.lower() != ".json":

            raise ConfigurationError(
                "Configuration must be a JSON file."
            )

        data = JsonParser.parse(path)

        return ProjectConfig(
            source=path,
            data=data,
        )
