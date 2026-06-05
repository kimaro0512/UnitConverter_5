"""Control NFR tests (NFR-05)."""

from __future__ import annotations

import inspect

import pytest


def test_control_NFR05_no_stdin_mock(conversion_service) -> None:
    """NFR-05: control tests orchestrate service without stdin mocking."""
    # Given
    # When
    try:
        if conversion_service is not None:
            inspect.getsource(conversion_service.convert_input)
    except (ModuleNotFoundError, TypeError, OSError):
        pass
    # Then
    pytest.fail("Red skeleton: convert_input path must not depend on stdin mock")
