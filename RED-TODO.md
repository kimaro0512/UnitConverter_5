# Red 단계 TODO (Track 2)

**Phase:** Red only — 실패하는 pytest TC 작성 · production은 **NotImplementedError 스텁**만  
**Green/Refactor:** 본 문서 범위 밖 → Green 완료 후 별도 진행

참고: [docs/TRACK2-RED-ENTRY.md](docs/TRACK2-RED-ENTRY.md) · [tests/traceability/BCE-TC-DESIGN.md](tests/traceability/BCE-TC-DESIGN.md) · [.cursor/skills/unitconverter-dual-track/](.cursor/skills/unitconverter-dual-track/SKILL.md)

---

## Red 원칙 (매 사이클)

- [ ] 한 번에 **FR-ID 1개 + BCE 레이어 1개**만
- [ ] TC 명명: `test_{entity|control|boundary}_{FRxx}_{snake_case}`
- [ ] docstring 첫 줄: `FR-xx:` 또는 `NFR-xx:`
- [ ] Entity/Control: I/O·Domain Mock **금지**
- [ ] Boundary: subprocess/capfd 등 Mock **허용**
- [ ] assert 완화·`skip`·`xfail`·TC 삭제 **금지**
- [ ] Red 완료 기준: `pytest` → **FAILED** (import / NotImplemented / assertion)
- [ ] `REQ_TRACEABILITY.md` status → `red` 갱신

**Cursor Agent 선언 (매 요청):**

`Phase: Red` · `Layer: {entity|control|boundary}` · `Track: 2` · `FR-{xx}`

---

## Gate — Red 진입 전

| # | 태스크 | 상태 |
|---|--------|------|
| G1 | FR/NFR ID 확정 (`REQ_TRACEABILITY.md`) | [x] |
| G2 | BCE TC 설계 (`BCE-TC-DESIGN.md`) | [x] |
| G3 | BCE 디렉터리 README | [x] |
| G4 | Cursor Rule (`.cursor/rules/dual-track-tdd.mdc`) | [x] |
| G5 | `pyproject.toml` + `pip install -e ".[dev]"` (`docs/pyproject.toml.spec` 참고) | [x] |
| G6 | `unit_converter/` import 가능 스켈레톤 (Red용 NotImplemented 스텁) | [x] |

### Cycle 0 — 환경

- [ ] `python -m venv venv`
- [ ] `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (macOS/Linux)
- [ ] `pip install -e ".[dev]"`
- [ ] `pytest --version` 확인
- [ ] `pytest --collect-only -q` (TC 0건 → Red 후 증가 확인)

**Red 시작 선언 (Agent):**

```
Track 2 Red 시작. FR-04 Entity only.
G5, G6부터 진행한 뒤 tests/entity/ 첫 TC만 작성. 구현 코드는 아직 금지.
@docs/TRACK2-RED-ENTRY.md @tests/traceability/BCE-TC-DESIGN.md
```

---

## Cycle 1 — Entity FR-04 ⭐ (첫 Red → Green 완료)

**파일:** `tests/entity/test_conversion_engine.py`

- [x] `test_entity_FR04_meter_hub_converts_to_feet_and_yard` — Then assert 교체
  - Given: registry meter(1.0), feet(3.28084), yard(1.09361)
  - When: `engine.convert(Quantity("meter", 1.0))`
  - Then: feet≈3.28084, yard≈1.09361
- [x] `test_entity_FR04_feet_yard_cross_consistent` — Then assert 교체
- [x] `unit_converter/conversion/engine.py` — meter hub `convert` 구현
- [x] `pytest tests/entity/test_conversion_engine.py -k FR04 -v` → **PASSED** (2)

---

## Cycle 2 — Entity FR-03

**파일:** `tests/entity/test_conversion_engine.py`

- [ ] `test_entity_FR03_default_units_in_registry`
- [ ] pytest Entity → 해당 TC **FAILED** 확인

---

## Cycle 3 — Entity FR-02

**파일:** `tests/entity/test_conversion_engine.py`

- [ ] `test_entity_FR02_convert_to_all_registered_units` (feet≈8.2021, yard≈2.7340)
- [ ] `test_entity_FR02_feet_input_converts_to_meter`
- [ ] pytest → **FAILED** 확인

---

## Cycle 4 — Entity FR-04 (보조)

**파일:** `tests/entity/test_conversion_engine.py`

- [x] `test_entity_FR04_feet_yard_cross_consistent` (Cycle 1 Green에 포함)

---

## Cycle 5 — Entity FR-11

**파일:** `tests/entity/test_conversion_result.py`

- [ ] `test_entity_FR11_rounding_policy_one_decimal` (8.2021 → 8.2)
- [ ] pytest → **FAILED** 확인

---

## Cycle 6 — Control FR-02

**파일:** `tests/control/test_conversion_service.py`

- [ ] `test_control_FR02_service_convert_input`
- [ ] `test_control_FR02_service_returns_all_unit_values`
- [ ] stdin/stdout mock **사용하지 않음** (NFR-05)
- [ ] in-memory registry + engine fixture
- [ ] pytest Control → **FAILED** 확인

---

## Cycle 7 — Control FR-08

**파일:** `tests/control/test_validator.py`

- [ ] `test_control_FR08_reject_negative_value`
- [ ] `test_control_FR08_zero_allowed`
- [ ] pytest → **FAILED** 확인

---

## Cycle 8 — Control FR-09

**파일:** `tests/control/test_conversion_service.py`

- [ ] `test_control_FR09_service_invalid_format`
- [ ] pytest → **FAILED** 확인

---

## Cycle 9 — Control FR-10

**파일:** `tests/control/test_validator.py`

- [ ] `test_control_FR10_reject_unknown_unit`
- [ ] `test_control_FR10_reject_unregistered_cubit`
- [ ] pytest → **FAILED** 확인

---

## Cycle 10 — Control FR-06

**파일:** `tests/control/test_conversion_service.py`

- [ ] `test_control_FR06_service_register_and_convert`
- [ ] pytest → **FAILED** 확인

---

## Cycle 11 — Control FR-07

**파일:** `tests/control/test_conversion_service.py`

- [ ] `test_control_FR07_service_format_json`
- [ ] pytest → **FAILED** 확인

---

## Cycle 12 — Boundary FR-01 · FR-09

**파일:** `tests/boundary/test_parser.py`

- [ ] `test_boundary_FR01_parse_valid_unit_value`
- [ ] `test_boundary_FR01_parse_trims_whitespace`
- [ ] `test_boundary_FR09_reject_missing_colon`
- [ ] `test_boundary_FR09_reject_non_numeric`
- [ ] `test_boundary_FR09_reject_bare_unit`
- [ ] `test_boundary_FR09_reject_bare_non_unit`
- [ ] `test_boundary_FR09_reject_extra_colon`
- [ ] pytest Boundary parser → **FAILED** 확인

---

## Cycle 13 — Boundary FR-03 · FR-05

**파일:** `tests/boundary/test_config_loaders.py`

- [ ] `test_boundary_FR03_config_json_lists_three_units`
- [ ] `test_boundary_FR05_load_units_from_json`
- [ ] `test_boundary_FR05_load_units_from_yaml`
- [ ] `test_boundary_FR05_missing_file_raises`
- [ ] pytest → **FAILED** 확인

---

## Cycle 14 — Boundary FR-06

**파일:** `tests/boundary/test_unit_registration_parser.py`

- [ ] `test_boundary_FR06_parse_register_cubit`
- [ ] pytest → **FAILED** 확인

---

## Cycle 15 — Boundary FR-07

**파일:** `tests/boundary/test_formatters.py`

- [ ] `test_boundary_FR07_json_format`
- [ ] `test_boundary_FR07_csv_format`
- [ ] `test_boundary_FR07_table_format`
- [ ] `test_boundary_FR07_factory_all_formats`
- [ ] pytest → **FAILED** 확인

---

## Cycle 16 — Boundary FR-11

**파일:** `tests/boundary/test_formatters.py`

- [ ] `test_boundary_FR11_text_output_one_decimal`
- [ ] pytest → **FAILED** 확인

---

## Cycle 17 — Boundary FR-02 · FR-08 · FR-10 (CLI)

**파일:** `tests/boundary/test_cli.py`

- [ ] `test_boundary_FR02_cli_stdout_contains_feet` (subprocess `python -m unit_converter`)
- [ ] `test_boundary_FR08_cli_negative_exit_nonzero`
- [ ] `test_boundary_FR10_cli_unknown_unit`
- [ ] (선택) `test_boundary_FR02_legacy_parity`
- [ ] pytest Boundary CLI → **FAILED** 확인

---

## Cycle 18 — Entity FR-06

**파일:** `tests/entity/test_registry.py`

- [ ] `test_entity_FR06_registry_stores_cubit`
- [ ] `test_entity_FR06_cubit_in_conversion_output`
- [ ] pytest → **FAILED** 확인

---

## Cycle 19 — NFR (Red TC)

**파일:** `tests/entity/`, `tests/control/`

- [ ] `test_entity_NFR01_engine_no_unit_branch` (engine 소스에 unit 분기 없음)
- [ ] `test_entity_NFR06_engine_no_magic_numbers` (`3.28084` 리터럴 없음)
- [ ] `test_control_NFR05_no_stdin_mock` (Control TC에 stdin mock 없음)
- [ ] pytest → **FAILED** 또는 정적 검증 **FAILED** 확인

---

## Red 마무리 점검

- [ ] `pytest tests/entity/ -v` — Entity Red TC 전부 수집·실행
- [ ] `pytest tests/control/ -v`
- [ ] `pytest tests/boundary/ -v`
- [ ] `pytest --collect-only -q` — `BCE-TC-DESIGN.md` 설계 TC와 대조
- [ ] `REQ_TRACEABILITY.md` — Red 완료 TC status `red` 반영
- [ ] **Green 단계**로 전환 (`TRACK2-RED-ENTRY.md` Cycle 1 Step 2부터, FR-04 1건씩)

---

## pytest 빠른 참조

```bash
pytest tests/entity/ -v
pytest tests/control/ -v
pytest tests/boundary/ -v
pytest -k "entity and FR04" -v
pytest tests/entity/test_conversion_engine.py::test_entity_FR04_meter_hub_converts_to_feet_and_yard -v
pytest --collect-only -q
```

---

## Red에서 하지 않는 것

- [ ] ~~Green 구현 (TC PASS 목적 코드)~~
- [ ] ~~assert 완화 / skip / xfail~~
- [ ] ~~한 프롬프트로 전 FR Red TC 일괄 Green~~
- [ ] ~~SPEC 문서 임의 변경~~
- [ ] ~~`UnitConverter.py` 레거시 리팩터~~ (별도 결정)
