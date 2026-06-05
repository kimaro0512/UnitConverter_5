"""Package path helpers."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
DEFAULT_UNITS_CONFIG = PROJECT_ROOT / "config" / "units.json"
