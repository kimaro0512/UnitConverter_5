"""Shared pytest fixtures for BCE Red skeleton (Track 2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_UNITS_CONFIG = {
    "base_unit": "meter",
    "units": {"meter": 1.0, "feet": 3.28084, "yard": 1.09361},
}


def build_registry(base_unit: str, units: dict[str, float]):
    """Test helper: populate registry via production register_many."""
    from unit_converter.conversion.registry import UnitRegistry
    from unit_converter.domain.models import UnitDefinition

    registry = UnitRegistry(base_unit=base_unit)
    definitions = [
        UnitDefinition(name=name, ratio_to_base=ratio)
        for name, ratio in units.items()
    ]
    registry.register_many(definitions)
    return registry


@pytest.fixture
def project_root() -> Path:
    return ROOT


@pytest.fixture
def units_json_path(project_root: Path) -> Path:
    return project_root / "config" / "units.json"


@pytest.fixture
def units_yaml_path(project_root: Path) -> Path:
    return project_root / "config" / "units.yaml"


@pytest.fixture
def units_config_data(units_json_path: Path) -> dict:
    if units_json_path.is_file():
        return json.loads(units_json_path.read_text(encoding="utf-8"))
    return dict(DEFAULT_UNITS_CONFIG)


@pytest.fixture
def default_registry(units_config_data: dict):
    try:
        return build_registry(units_config_data["base_unit"], units_config_data["units"])
    except ModuleNotFoundError:
        return None


@pytest.fixture
def empty_registry():
    try:
        from unit_converter.conversion.registry import UnitRegistry

        return UnitRegistry(base_unit="meter")
    except ModuleNotFoundError:
        return None


@pytest.fixture
def engine(default_registry):
    if default_registry is None:
        return None
    try:
        from unit_converter.conversion.engine import ConversionEngine

        return ConversionEngine(default_registry)
    except ModuleNotFoundError:
        return None


@pytest.fixture
def conversion_service(default_registry, engine):
    if default_registry is None or engine is None:
        return None
    try:
        from unit_converter.app.service import ConversionService
        from unit_converter.input.validator import InputValidator

        return ConversionService(
            registry=default_registry,
            engine=engine,
            validator=InputValidator(default_registry),
        )
    except ModuleNotFoundError:
        return None


@pytest.fixture
def sample_conversion_result():
    try:
        from unit_converter.domain.models import (
            ConversionResult,
            ConvertedValue,
            Quantity,
        )
    except ModuleNotFoundError:
        return None

    source = Quantity(unit="meter", value=2.5)
    values = [
        ConvertedValue(unit="meter", value=2.5),
        ConvertedValue(unit="feet", value=8.2021),
        ConvertedValue(unit="yard", value=2.7340),
    ]
    return ConversionResult(source=source, values=values)


@pytest.fixture
def engine_source_path(project_root: Path) -> Path:
    return project_root / "unit_converter" / "conversion" / "engine.py"
