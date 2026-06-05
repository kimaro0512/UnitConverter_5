"""Boundary config loader tests (FR-03, FR-05)."""

from __future__ import annotations

import pytest

from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.config.yaml_loader import YamlConfigLoader


def test_boundary_FR03_config_json_lists_three_units(units_json_path) -> None:
    """FR-03: units.json defines three units."""
    # Given / When
    registry = JsonConfigLoader().load(units_json_path)
    # Then
    assert len(registry.unit_names()) == 3


def test_boundary_FR05_load_units_from_json(units_json_path) -> None:
    """FR-05: JsonConfigLoader loads feet from units.json."""
    # Given / When
    registry = JsonConfigLoader().load(units_json_path)
    # Then
    assert registry.has_unit("feet")


def test_boundary_FR05_load_units_from_yaml(units_yaml_path) -> None:
    """FR-05: YamlConfigLoader loads yard from units.yaml."""
    # Given / When
    registry = YamlConfigLoader().load(units_yaml_path)
    # Then
    assert registry.has_unit("yard")


def test_boundary_FR05_missing_file_raises(project_root) -> None:
    """FR-05: missing config path raises appropriate error."""
    # Given
    path = project_root / "config" / "missing-units.json"
    # When / Then
    with pytest.raises(FileNotFoundError):
        JsonConfigLoader().load(path)
