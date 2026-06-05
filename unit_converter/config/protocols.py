"""Config loader protocols (FR-05, NFR-06)."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from unit_converter.conversion.registry import UnitRegistry


class ConfigLoader(Protocol):
    """Load unit definitions from an external file into a registry."""

    def load(self, path: Path) -> UnitRegistry: ...
