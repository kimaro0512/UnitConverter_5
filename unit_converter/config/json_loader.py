"""JSON configuration loader (FR-03, FR-05)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from unit_converter.config.base_loader import BaseFileConfigLoader


class JsonConfigLoader(BaseFileConfigLoader):
    """Load unit definitions from a JSON config file."""

    def _parse(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))
