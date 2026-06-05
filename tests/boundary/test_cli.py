"""Boundary CLI tests (FR-02, FR-08, FR-10)."""

from __future__ import annotations

import subprocess
import sys

import pytest


def test_boundary_FR02_cli_stdout_contains_feet(
    project_root,
) -> None:
    """FR-02: CLI prints feet for meter:2.5 input."""
    # Given
    cmd = [sys.executable, "-m", "unit_converter", "meter:2.5"]
    # When
    try:
        completed = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        completed = None
    # Then
    pytest.fail("Red skeleton: returncode=0 and 'feet' in stdout")


def test_boundary_FR02_legacy_parity(
    project_root,
) -> None:
    """FR-02: legacy UnitConverter.py feet output within tolerance (optional)."""
    # Given
    cmd = [sys.executable, "UnitConverter.py"]
    stdin = "meter:2.5\n"
    # When
    try:
        completed = subprocess.run(
            cmd,
            cwd=project_root,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        completed = None
    # Then
    pytest.fail("Red skeleton: legacy feet within ±0.1 of entity expectation")


def test_boundary_FR08_cli_negative_exit_nonzero(
    project_root,
) -> None:
    """FR-08: CLI rejects meter:-1 with non-zero exit or error message."""
    # Given
    cmd = [sys.executable, "-m", "unit_converter", "meter:-1"]
    # When
    try:
        completed = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        completed = None
    # Then
    pytest.fail("Red skeleton: non-zero exit or error for meter:-1")


def test_boundary_FR10_cli_unknown_unit(
    project_root,
) -> None:
    """FR-10: CLI rejects unknown unit mile:1."""
    # Given
    cmd = [sys.executable, "-m", "unit_converter", "mile:1"]
    # When
    try:
        completed = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        completed = None
    # Then
    pytest.fail("Red skeleton: error output and no conversion for mile:1")
