"""Shared pytest fixtures for BCE tests (Track 2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from unit_converter.app.service import ConversionService
from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.conversion.engine import ConversionEngine
from unit_converter.conversion.registry import UnitRegistry
from unit_converter.domain.models import ConversionResult, ConvertedValue, Quantity
from unit_converter.input.validator import InputValidator

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


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
    return json.loads(units_json_path.read_text(encoding="utf-8"))


@pytest.fixture
def default_registry(units_json_path: Path):
    return JsonConfigLoader().load(units_json_path)


@pytest.fixture
def empty_registry():
    return UnitRegistry(base_unit="meter")


@pytest.fixture
def engine(default_registry):
    return ConversionEngine(default_registry)


@pytest.fixture
def conversion_service(default_registry, engine):
    return ConversionService(
        registry=default_registry,
        engine=engine,
        validator=InputValidator(default_registry),
    )


@pytest.fixture
def sample_conversion_result():
    source = Quantity(unit="meter", value=2.5)
    values = [
        ConvertedValue(unit="meter", value=2.5),
        ConvertedValue(unit="feet", value=8.2021),
        ConvertedValue(unit="yard", value=2.7340),
    ]
    return ConversionResult(source=source, values=tuple(values))


@pytest.fixture
def engine_source_path(project_root: Path) -> Path:
    return project_root / "unit_converter" / "conversion" / "engine.py"
