"""Config loader factory (FR-05, NFR-01)."""

from __future__ import annotations

from pathlib import Path

from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.config.protocols import ConfigLoader
from unit_converter.config.yaml_loader import YamlConfigLoader


def resolve_config_loader(path: Path) -> ConfigLoader:
    """Select JSON or YAML loader from file extension."""
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return YamlConfigLoader()
    return JsonConfigLoader()
