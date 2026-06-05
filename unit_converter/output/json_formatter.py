"""JSON output formatter (FR-07)."""

from __future__ import annotations

import json

from unit_converter.domain.models import ConversionResult


class JsonFormatter:
    """Serialize conversion results as JSON."""

    def format(self, result: ConversionResult) -> str:
        payload = {
            "source": {
                "unit": result.source.unit,
                "value": result.source.value,
            },
            "values": [
                {"unit": item.unit, "value": item.value}
                for item in result.values
            ],
        }
        return json.dumps(payload)
