"""YAML configuration loader (FR-05)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from unit_converter.config.base_loader import BaseFileConfigLoader


class YamlConfigLoader(BaseFileConfigLoader):
    """Load unit definitions from a YAML config file."""

    def _parse(self, path: Path) -> dict[str, Any]:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
