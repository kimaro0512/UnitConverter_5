# Track 2 Red 진입 체크리스트

Red 단계 **진입 전** 준비 SPEC. 아직 `tests/**/*.py` 및 `unit_converter/` 구현은 **시작하지 않음**.

관련: [DUAL-TRACK-TDD.md](./DUAL-TRACK-TDD.md) · [BCE-TC-DESIGN.md](../tests/traceability/BCE-TC-DESIGN.md)

---

## 1. Red 진입 조건 (Gate)

| # | 항목 | 상태 |
|---|------|------|
| G1 | FR/NFR ID 확정 (`REQ_TRACEABILITY.md`) | ✅ |
| G2 | BCE TC 설계 완료 (`BCE-TC-DESIGN.md`) | ✅ |
| G3 | BCE 디렉터리 README (`tests/entity|control|boundary/`) | ✅ |
| G4 | Cursor Rule (`.cursor/rules/dual-track-tdd.mdc`) | ✅ |
| G5 | `pyproject.toml` + pytest 환경 (Track 2 Day 1) | ⬜ Red 진입 시 |
| G6 | `unit_converter/` 패키지 스켈레톤 (Track 2 Day 1) | ⬜ Red 진입 시 |

**Red 시작 선언 (Cursor Chat):**

```
Track 2 Red 시작. FR-04 Entity only.
G5, G6부터 진행한 뒤 tests/entity/ 첫 TC만 작성. 구현 코드는 아직 금지.
```

---

## 2. Red → Green 사이클 (예시 3 권장 흐름)

### Cycle 0 — 환경 (Red 직전)

```bash
# Red 진입 시 최초 1회
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
```

산출: `pyproject.toml`, `unit_converter/` 최소 스켈레톤 (`docs/pyproject.toml.spec` 참고)

---

### Cycle 1 — Entity FR-04 (첫 Red, 권장)

#### Step 1: Red

| 항목 | 내용 |
|------|------|
| **파일** | `tests/entity/test_conversion_engine.py` |
| **TC** | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` |
| **Given** | registry에 meter(1.0), feet(3.28084), yard(1.09361) |
| **When** | `engine.convert(Quantity("meter", 1.0))` |
| **Then** | feet≈3.28084, yard≈1.09361 |
| **기대** | `pytest tests/entity/ -v` → **FAILED** (import 또는 NotImplemented) |

**Cursor Agent (Red):**

```
Track 2 Red. BCE=entity. FR-04 only.
tests/entity/test_conversion_engine.py 1개만 생성.
unit_converter/conversion/engine.py 는 NotImplementedError 스텁만 허용.
다른 FR, Control, Boundary 건드리지 마.
```

#### Step 2: Green (예시 3 — **한 TC만**)

| 허용 수정 | 금지 |
|-----------|------|
| `unit_converter/conversion/engine.py` | `cli.py`, `parser.py` |
| `unit_converter/conversion/registry.py` | formatters, loaders |
| `unit_converter/domain/models.py` | `UnitConverter.py` 레거시 |
| `unit_converter/domain/exceptions.py` | |
| `config/units.json` (비율) | engine 내부 magic number |

**Cursor Agent (Green):**

```
Track 2 Green. test_entity_FR04_meter_hub_converts_to_feet_and_yard 하나만 PASS.
허용 파일: engine, registry, domain, config/units.json 만.
pytest tests/entity/test_conversion_engine.py::test_entity_FR04_meter_hub_converts_to_feet_and_yard -v
```

**기대:** `PASSED` (1), 다른 TC 없음

#### Step 3: Refactor (같은 FR 범위)

- registry hub 로직 정리
- `REQ_TRACEABILITY` / `BCE-TC-DESIGN` status → `red-done` / `green-done` (Track 2에서)

---

### Cycle 2~N — 권장 순서

| 순서 | BCE | FR | TC (설계명) |
|------|-----|-----|-------------|
| 1 | Entity | FR-04 | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` |
| 2 | Entity | FR-03 | `test_entity_FR03_default_units_in_registry` |
| 3 | Entity | FR-02 | `test_entity_FR02_convert_to_all_registered_units` |
| 4 | Control | FR-02 | `test_control_FR02_service_convert_input` |
| 5 | Control | FR-08~10 | validator/service negative paths |
| 6 | Boundary | FR-01 | `test_boundary_FR01_parse_unit_value` (parser) |
| 7 | Boundary | FR-11 | `test_boundary_FR11_text_formatter_one_decimal` |
| 8 | Boundary | FR-05~07 | loaders, formatters |
| 9 | Entity/Control | FR-06 | registration |
| 10 | Boundary | FR-02 | `test_boundary_FR02_cli_stdout_feet` |

---

## 3. Red 단계 pytest 명령 (진입 후)

```bash
pytest tests/entity/ -v                    # Entity만
pytest tests/control/ -v
pytest tests/boundary/ -v
pytest -k "entity and FR04" -v
pytest --collect-only -q                     # 설계 대비 수집 확인
```

---

## 4. SPEC 단계에서 하지 않는 것

- ❌ Red TC `.py` 작성
- ❌ Green 구현
- ❌ `pytest` 실패/성공 사이클
- ❌ `UnitConverter.py` 리팩터 (Track 2에서 별도 결정)

---

## 5. Red 진입 선언 템플릿

```
프로젝트 UnitConverter_5 Track 2 Red 진입.
첫 사이클: Entity FR-04 (예시 3 Green 범위 준수).
@docs/TRACK2-RED-ENTRY.md @tests/traceability/BCE-TC-DESIGN.md
```
