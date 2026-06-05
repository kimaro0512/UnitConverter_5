"""JSON output formatter (FR-07)."""

from __future__ import annotations

import json

from unit_converter.domain.models import ConversionResult
from unit_converter.output.presentation import all_converted_values


class JsonFormatter:
    """Serialize conversion results as JSON (full precision export)."""

    def format(self, result: ConversionResult) -> str:
        payload = {
            "source": {
                "unit": result.source.unit,
                "value": result.source.value,
            },
            "values": [
                {"unit": item.unit, "value": item.value}
                for item in all_converted_values(result)
            ],
        }
        return json.dumps(payload)
