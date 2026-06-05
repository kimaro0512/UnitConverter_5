"""Golden block formatting helpers."""

from __future__ import annotations

from collections.abc import Callable


def block(name: str, *lines: str) -> str:
    body = "\n".join(lines)
    return f"[{name}]\n{body}"


def float_text(value: float) -> str:
    return f"{value:.6f}"


def exc_name(fn: Callable[[], object], *expected: type[BaseException]) -> str:
    try:
        fn()
    except expected as exc:
        return type(exc).__name__
    raise AssertionError(f"expected {expected}")
