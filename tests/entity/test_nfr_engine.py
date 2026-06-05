"""Entity NFR tests (NFR-01, NFR-06)."""

from __future__ import annotations

import pytest


def test_entity_NFR01_engine_no_unit_branch(engine_source_path) -> None:
    """NFR-01: engine must not branch on unit names (OCP)."""
    # Given
    # When
    try:
        if engine_source_path.is_file():
            engine_source_path.read_text(encoding="utf-8")
    except (ModuleNotFoundError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: engine source has no elif unit branching")


def test_entity_NFR06_engine_no_magic_numbers(engine_source_path) -> None:
    """NFR-06: engine must not hardcode conversion ratios."""
    # Given
    # When
    try:
        if engine_source_path.is_file():
            engine_source_path.read_text(encoding="utf-8")
    except (ModuleNotFoundError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: engine source must not contain 3.28084 literal")
