"""YAML configuration loader (FR-05)."""

from __future__ import annotations

from pathlib import Path

import yaml

from unit_converter.conversion.registry import UnitRegistry
from unit_converter.domain.models import UnitDefinition


class YamlConfigLoader:
    """Load unit definitions from a YAML config file."""

    def load(self, path: Path) -> UnitRegistry:
        """FR-05: Build a registry from ``units.yaml``."""
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {path}")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        registry = UnitRegistry(base_unit=data["base_unit"])
        definitions = [
            UnitDefinition(name=name, ratio_to_base=ratio)
            for name, ratio in data["units"].items()
        ]
        registry.register_many(definitions)
        return registry
