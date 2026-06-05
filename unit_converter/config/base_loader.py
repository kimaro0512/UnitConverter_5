"""Shared config → registry loading (FR-05, NFR-06)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from unit_converter.conversion.registry import UnitRegistry
from unit_converter.domain.models import UnitDefinition


def registry_from_config(data: dict[str, Any]) -> UnitRegistry:
    """Build a registry from parsed config data (base_unit + units map)."""
    registry = UnitRegistry(base_unit=data["base_unit"])
    definitions = [
        UnitDefinition(name=name, ratio_to_base=ratio)
        for name, ratio in data["units"].items()
    ]
    return registry.register_many(definitions)


class BaseFileConfigLoader:
    """Template Method: read file → parse → registry_from_config."""

    def load(self, path: Path) -> UnitRegistry:
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {path}")
        return registry_from_config(self._parse(path))

    def _parse(self, path: Path) -> dict[str, Any]:
        raise NotImplementedError
