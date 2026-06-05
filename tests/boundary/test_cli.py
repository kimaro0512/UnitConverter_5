"""Boundary CLI tests (FR-02, FR-08, FR-10)."""

from __future__ import annotations

import re
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
    completed = subprocess.run(
        cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=10,
    )
    # Then
    assert completed.returncode == 0
    assert "feet" in completed.stdout


def test_boundary_FR02_legacy_parity(
    project_root,
) -> None:
    """FR-02: legacy UnitConverter.py feet output within tolerance (optional)."""
    # Given
    cmd = [sys.executable, "UnitConverter.py"]
    stdin = "meter:2.5\n"
    # When
    completed = subprocess.run(
        cmd,
        cwd=project_root,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )
    # Then
    assert completed.returncode == 0
    match = re.search(r"=\s*([\d.]+)\s*feet", completed.stdout)
    assert match is not None
    feet = float(match.group(1))
    assert feet == pytest.approx(8.2021, abs=0.1)


def test_boundary_FR08_cli_negative_exit_nonzero(
    project_root,
) -> None:
    """FR-08: CLI rejects meter:-1 with non-zero exit or error message."""
    # Given
    cmd = [sys.executable, "-m", "unit_converter", "meter:-1"]
    # When
    completed = subprocess.run(
        cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=10,
    )
    # Then
    assert completed.returncode != 0


def test_boundary_FR10_cli_unknown_unit(
    project_root,
) -> None:
    """FR-10: CLI rejects unknown unit mile:1."""
    # Given
    cmd = [sys.executable, "-m", "unit_converter", "mile:1"]
    # When
    completed = subprocess.run(
        cmd,
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=10,
    )
    # Then
    assert completed.returncode != 0
