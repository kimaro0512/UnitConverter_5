"""Entity scenario capture (shared by Golden Master)."""

from __future__ import annotations

from pathlib import Path

from tests.scenarios.helpers import block, float_text
from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.conversion.engine import ConversionEngine
from unit_converter.conversion.registry import UnitRegistry
from unit_converter.domain.models import Quantity, UnitDefinition


def collect_entity_blocks(
    empty_registry,
    sample_conversion_result,
    units_json_path: Path,
    engine_source_path: Path,
) -> list[str]:
    blocks: list[str] = []
    fresh_registry = JsonConfigLoader().load(units_json_path)
    fresh_engine = ConversionEngine(fresh_registry)

    quantity = Quantity(unit="meter", value=2.5)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    blocks.append(
        block(
            "test_entity_FR02_convert_to_all_registered_units",
            f"feet={float_text(feet)}",
            f"yard={float_text(yard)}",
        )
    )

    quantity = Quantity(unit="feet", value=8.2021)
    result = fresh_engine.convert(quantity)
    meter = next(item.value for item in result.values if item.unit == "meter")
    blocks.append(
        block(
            "test_entity_FR02_feet_input_converts_to_meter",
            f"meter={float_text(meter)}",
        )
    )

    names = sorted(fresh_registry.unit_names())
    blocks.append(
        block(
            "test_entity_FR03_default_units_in_registry",
            f"units={','.join(names)}",
        )
    )

    quantity = Quantity(unit="meter", value=1.0)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    blocks.append(
        block(
            "test_entity_FR04_meter_hub_converts_to_feet_and_yard",
            f"feet={float_text(feet)}",
            f"yard={float_text(yard)}",
        )
    )

    quantity = Quantity(unit="feet", value=3.28084)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    ratio = yard / feet
    blocks.append(
        block(
            "test_entity_FR04_feet_yard_cross_consistent",
            f"ratio={float_text(ratio)}",
        )
    )

    cubit = UnitDefinition(name="cubit", ratio_to_base=0.4572)
    empty_registry.register(cubit)
    blocks.append(
        block(
            "test_entity_FR06_registry_stores_cubit",
            f"has_cubit={empty_registry.has_unit('cubit')}",
        )
    )

    reg = UnitRegistry(base_unit="meter")
    reg.register_many(
        [
            UnitDefinition(name="meter", ratio_to_base=1.0),
            UnitDefinition(name="cubit", ratio_to_base=0.4572),
        ]
    )
    eng = ConversionEngine(reg)
    result = eng.convert(Quantity(unit="meter", value=1.0))
    unit_set = sorted(item.unit for item in result.values)
    blocks.append(
        block(
            "test_entity_FR06_cubit_in_conversion_output",
            f"units={','.join(unit_set)}",
        )
    )

    rounded = sample_conversion_result.rounded_value(8.2021)
    blocks.append(
        block(
            "test_entity_FR11_rounding_policy_one_decimal",
            f"rounded={float_text(rounded)}",
        )
    )

    source = engine_source_path.read_text(encoding="utf-8")
    blocks.append(
        block(
            "test_entity_NFR01_engine_no_unit_branch",
            f"elif_unit={'elif unit' in source}",
            f"feet_eq={'unit == \"feet\"' in source}",
            f"yard_eq={'unit == \"yard\"' in source}",
            f"meter_eq={'unit == \"meter\"' in source}",
        )
    )
    blocks.append(
        block(
            "test_entity_NFR06_engine_no_magic_numbers",
            f"ratio_feet={'3.28084' in source}",
            f"ratio_yard={'1.09361' in source}",
        )
    )

    return blocks
