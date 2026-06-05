"""Boundary config loader tests (FR-03, FR-05)."""

from __future__ import annotations

import pytest


def test_boundary_FR03_config_json_lists_three_units(units_json_path) -> None:
    """FR-03: units.json defines three units."""
    # Given
    # When
    try:
        from unit_converter.config.json_loader import JsonConfigLoader

        JsonConfigLoader().load(units_json_path)
    except (ModuleNotFoundError, NotImplementedError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: loaded registry has 3 units")


def test_boundary_FR05_load_units_from_json(units_json_path) -> None:
    """FR-05: JsonConfigLoader loads feet from units.json."""
    # Given
    # When
    try:
        from unit_converter.config.json_loader import JsonConfigLoader

        JsonConfigLoader().load(units_json_path)
    except (ModuleNotFoundError, NotImplementedError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: registry.has_unit('feet') is True")


def test_boundary_FR05_load_units_from_yaml(units_yaml_path) -> None:
    """FR-05: YamlConfigLoader loads yard from units.yaml."""
    # Given
    # When
    try:
        from unit_converter.config.yaml_loader import YamlConfigLoader

        YamlConfigLoader().load(units_yaml_path)
    except (ModuleNotFoundError, NotImplementedError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: registry.has_unit('yard') is True")


def test_boundary_FR05_missing_file_raises(project_root) -> None:
    """FR-05: missing config path raises appropriate error."""
    # Given
    path = project_root / "config" / "missing-units.json"
    # When
    try:
        from unit_converter.config.json_loader import JsonConfigLoader

        JsonConfigLoader().load(path)
    except (ModuleNotFoundError, NotImplementedError, OSError, FileNotFoundError):
        pass
    # Then
    pytest.fail("Red skeleton: appropriate exception for missing config file")
