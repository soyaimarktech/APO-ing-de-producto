"""
Configuration models.

Strongly typed objects replacing raw dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ProjectConfig:
    """
    Represents one APO project configuration.
    """

    source: Path

    data: dict[str, Any]

    @property
    def schema_version(self) -> str:
        return self.data.get("schemaVersion", "")

    @property
    def name(self) -> str:
        return self.source.stem
