"""Golden Master approval helpers (tests only — not production)."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parent
_GOLDEN_ROOT = _TESTS_ROOT / "golden"


def _update_mode() -> bool:
    return os.environ.get("UPDATE_GOLDEN", "").strip().lower() in ("1", "true", "yes")


def format_golden_success(values: list[int]) -> str:
    """int[6] success line: r1 c1 n1 r2 c2 n2 (1-index coordinates)."""
    if len(values) != 6:
        raise ValueError(f"int[6] required, got len={len(values)}")
    for idx in (0, 1, 3, 4):
        if not (1 <= values[idx] <= 4):
            raise ValueError(f"1-index row/col expected at [{idx}], got {values[idx]}")
    return " ".join(str(v) for v in values)


def format_golden_error(code: str, name: str) -> str:
    """Error line: E00x NAME (boundary golden)."""
    return f"{code} {name}"


def format_golden_cli(
    exit_code: int,
    stdout: str = "",
    stderr: str = "",
    *,
    error: tuple[str, str] | None = None,
) -> str:
    """Fixed CLI golden: exit code, optional error code line, stdout, stderr."""
    lines = [str(exit_code)]
    if error is not None:
        lines.append(format_golden_error(error[0], error[1]))
    out = stdout.rstrip("\n")
    err = stderr.rstrip("\n")
    if out:
        lines.extend(out.splitlines())
    if err:
        lines.extend(err.splitlines())
    return "\n".join(lines)


def format_golden(actual: list[int] | str) -> str:
    if isinstance(actual, list):
        return format_golden_success(actual)
    return actual.strip()


def assert_matches_golden(actual: list[int] | str, relative: str) -> None:
    """Compare actual output to tests/golden/<relative> (or write when UPDATE_GOLDEN=1)."""
    text = format_golden(actual)
    path = _GOLDEN_ROOT / relative
    if _update_mode():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
        return
    if not path.exists():
        raise AssertionError(f"Golden file missing: {path} (run with UPDATE_GOLDEN=1)")
    expected = path.read_text(encoding="utf-8").strip()
    if text == expected:
        return
    diff = "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            text.splitlines(),
            fromfile=f"golden/{relative}",
            tofile="actual",
            lineterm="",
        )
    )
    raise AssertionError(f"Golden mismatch for {relative}:\n{diff}")
