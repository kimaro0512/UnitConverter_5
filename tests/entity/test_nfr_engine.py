"""Entity NFR tests (NFR-01, NFR-06)."""

from __future__ import annotations


def test_entity_NFR01_engine_no_unit_branch(engine_source_path) -> None:
    """NFR-01: engine must not branch on unit names (OCP)."""
    # Given
    source = engine_source_path.read_text(encoding="utf-8")
    # Then
    assert "elif unit" not in source
    assert 'unit == "feet"' not in source
    assert 'unit == "yard"' not in source
    assert 'unit == "meter"' not in source


def test_entity_NFR06_engine_no_magic_numbers(engine_source_path) -> None:
    """NFR-06: engine must not hardcode conversion ratios."""
    # Given
    source = engine_source_path.read_text(encoding="utf-8")
    # Then
    assert "3.28084" not in source
    assert "1.09361" not in source
