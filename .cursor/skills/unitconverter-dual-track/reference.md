# UnitConverter Dual Track — Reference

ID SSOT: **FR-01~11, NFR-01~06** · 명명: `test_{entity|control|boundary}_{FRxx}_{snake_case}`

---

## FR P0 — Given / Then (요약)

| ID | Given | Then |
|----|-------|------|
| FR-01 | `meter:2.5` | Quantity(meter, 2.5) |
| FR-02 | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-03 | default registry | meter, feet, yard |
| FR-04 | meter 1.0 | feet≈3.28084, yard≈1.09361 |
| FR-08 | `meter:-1` | ValidationError |
| FR-09 | `meter` / `abc` / `meter:2.5:extra` | ParseError |
| FR-10 | `cubit:1` 미등록 | UnknownUnitError |
| FR-11 | 8.2021 feet | 표시 `8.2` |

P1: FR-05(설정), FR-06(동적등록), FR-07(`--format`)

---

## Track 2 권장 순서 (Cycle)

| # | BCE | FR | 대표 TC (설계명) |
|---|-----|-----|------------------|
| 1 | Entity | FR-04 | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` |
| 2 | Entity | FR-03 | `test_entity_FR03_default_units_in_registry` |
| 3 | Entity | FR-02 | `test_entity_FR02_convert_to_all_registered_units` |
| 4 | Control | FR-02 | `test_control_FR02_service_convert_input` |
| 5 | Control | FR-08~10 | `test_control_FR08_*`, `FR09`, `FR10` |
| 6 | Boundary | FR-01, FR-09 | `test_boundary_FR01_*`, `FR09_*` |
| 7 | Boundary | FR-11 | `test_boundary_FR11_*` |
| 8 | Boundary | FR-05~07 | loaders, formatters |
| 9 | Entity/Control | FR-06 | registry + registration |
| 10 | Boundary | FR-02 | `test_boundary_FR02_cli_*` |

상세 Given/When/Then: `tests/traceability/BCE-TC-DESIGN.md`

---

## Green 허용 파일 (FR별)

### FR-04 Entity (첫 Green — 예시 3)

| 허용 | 금지 |
|------|------|
| `unit_converter/conversion/engine.py` | `app/cli.py`, `input/parser.py` |
| `unit_converter/conversion/registry.py` | formatters, loaders |
| `unit_converter/domain/models.py` | `UnitConverter.py` |
| `unit_converter/domain/exceptions.py` | |
| `config/units.json` | engine 내부 magic number |

### FR-03 Entity

FR-04 허용 + `registry` 기본 단위 등록 로직 (설계에 따라 `config/units.json` 연동)

### FR-02 Entity

FR-03 Green 완료 전제 + `engine.convert` 전 단위 출력

### FR-02 Control

| 허용 | 금지 |
|------|------|
| `unit_converter/app/service.py` | stdin/stdout mock (NFR-05) |
| Entity Green 산출물 | CLI, parser |

### FR-08~10 Control

| 허용 | 금지 |
|------|------|
| `unit_converter/input/validator.py` | Boundary I/O |
| `app/service.py` (해당 FR만) | |

### FR-01, FR-09 Boundary

| 허용 | 금지 |
|------|------|
| `unit_converter/input/parser.py` | engine/service 직접 수정(해당 FR 범위 밖) |

### FR-05~07 Boundary

| 허용 | 금지 |
|------|------|
| `unit_converter/config/*_loader.py` | engine 비율 하드코딩 |
| `unit_converter/output/*_formatter.py` | |
| `app/cli.py` (FR-07 옵션) | |

### FR-06

Entity: `conversion/registry.py` · Boundary: `input/unit_registration_parser.py`

---

## pytest 명령

```bash
pytest tests/entity/ -v
pytest tests/control/ -v
pytest tests/boundary/ -v
pytest -k "entity and FR04" -v
pytest tests/entity/test_conversion_engine.py::test_entity_FR04_meter_hub_converts_to_feet_and_yard -v
pytest --collect-only -q
```

---

## NFR 검증 TC (설계명)

| ID | TC |
|----|-----|
| NFR-01 | `test_entity_NFR01_engine_no_unit_branch` |
| NFR-05 | `test_control_NFR05_no_stdin_mock` |
| NFR-06 | `test_entity_NFR06_engine_no_magic_numbers` |

---

## Red 진입 Gate

| # | 항목 |
|---|------|
| G1 | `REQ_TRACEABILITY.md` |
| G2 | `BCE-TC-DESIGN.md` |
| G3 | `tests/entity|control|boundary/README.md` |
| G4 | `.cursor/rules/dual-track-tdd.mdc` |
| G5 | `pyproject.toml` + pytest |
| G6 | `unit_converter/` 스켈레톤 |

---

## 매트릭스 전체

`tests/traceability/REQ_TRACEABILITY.md` — FR ↔ 모듈 ↔ TC ↔ status
