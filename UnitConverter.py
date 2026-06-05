"""Legacy entry point — thin wrapper to unit_converter.app.cli (R1 Refactor)."""

from __future__ import annotations

import sys

from unit_converter.app.cli import main


def run() -> int:
    """Preserve interactive stdin when invoked without CLI arguments."""
    if len(sys.argv) > 1:
        return main(sys.argv[1:])
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    return main([input_str.strip()])


if __name__ == "__main__":
    raise SystemExit(run())
