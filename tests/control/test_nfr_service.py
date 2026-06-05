"""Control NFR tests (NFR-05)."""

from __future__ import annotations

import inspect


def test_control_NFR05_no_stdin_mock(conversion_service) -> None:
    """NFR-05: control tests orchestrate service without stdin mocking."""
    # Given
    source = inspect.getsource(conversion_service.convert_input)
    # Then — string param path, not interactive stdin
    assert "stdin" not in source
    assert "parse_unit_value(raw)" in source
