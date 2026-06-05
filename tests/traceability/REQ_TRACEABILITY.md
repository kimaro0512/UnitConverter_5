# 요구사항 추적성 매트릭스 (FR / NFR)

PRD: [README.md](../../README.md)  
아키텍처: [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)  
Dual Track: [docs/DUAL-TRACK-TDD.md](../../docs/DUAL-TRACK-TDD.md)  
BCE 설계: [BCE-TC-DESIGN.md](./BCE-TC-DESIGN.md)

**단계:** SPEC / **Red 준비** — BCE TC 설계 완료. `tests/**/*.py`·`unit_converter/` **없음**.

**상태:** `designed` = TC 설계 | `red-ready` = Red 작성 대기 | `red` | `green` | `implemented`

---

## Functional Requirements (BCE)

| ID | BCE | 요구사항 | 모듈 | 테스트 파일 | 테스트 케이스 | 상태 |
|----|-----|----------|------|-------------|---------------|------|
| FR-01 | Boundary | `단위:값` 파싱 | `input/parser.py` | `tests/boundary/test_parser.py` | `test_boundary_FR01_parse_valid_unit_value` | designed |
| FR-01 | Boundary | 공백 trim | `input/parser.py` | `tests/boundary/test_parser.py` | `test_boundary_FR01_parse_trims_whitespace` | designed |
| FR-02 | Entity | 모든 단위 변환 | `conversion/engine.py` | `tests/entity/test_conversion_engine.py` | `test_entity_FR02_convert_to_all_registered_units` | designed |
| FR-02 | Control | service 변환 | `app/service.py` | `tests/control/test_conversion_service.py` | `test_control_FR02_service_convert_input` | designed |
| FR-02 | Boundary | CLI stdout | `app/cli.py` | `tests/boundary/test_cli.py` | `test_boundary_FR02_cli_stdout_contains_feet` | designed |
| FR-03 | Entity | 3단위 registry | `registry`, `config/units.json` | `tests/entity/test_conversion_engine.py` | `test_entity_FR03_default_units_in_registry` | designed |
| FR-04 | Entity | meter hub ⭐ | `conversion/engine.py` | `tests/entity/test_conversion_engine.py` | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` | **red-ready** |
| FR-05 | Boundary | JSON 로드 | `config/json_loader.py` | `tests/boundary/test_config_loaders.py` | `test_boundary_FR05_load_units_from_json` | designed |
| FR-05 | Boundary | YAML 로드 | `config/yaml_loader.py` | `tests/boundary/test_config_loaders.py` | `test_boundary_FR05_load_units_from_yaml` | designed |
| FR-06 | Entity | cubit 등록 | `conversion/registry.py` | `tests/entity/test_registry.py` | `test_entity_FR06_registry_stores_cubit` | designed |
| FR-06 | Boundary | 등록 문자열 파싱 | `input/unit_registration_parser.py` | `tests/boundary/test_unit_registration_parser.py` | `test_boundary_FR06_parse_register_cubit` | designed |
| FR-07 | Boundary | JSON/CSV/표 | `output/*_formatter.py` | `tests/boundary/test_formatters.py` | `test_boundary_FR07_*` | designed |
| FR-08 | Control | 음수 거부 | `input/validator.py` | `tests/control/test_validator.py` | `test_control_FR08_reject_negative_value` | designed |
| FR-09 | Boundary | 형식 오류 | `input/parser.py` | `tests/boundary/test_parser.py` | `test_boundary_FR09_reject_missing_colon` | designed |
| FR-10 | Control | unknown unit | `input/validator.py` | `tests/control/test_validator.py` | `test_control_FR10_reject_unknown_unit` | designed |
| FR-11 | Entity | 반올림 정책 | `domain/models.py` | `tests/entity/test_conversion_result.py` | `test_entity_FR11_rounding_policy_one_decimal` | designed |
| FR-11 | Boundary | text 출력 | `output/text_formatter.py` | `tests/boundary/test_formatters.py` | `test_boundary_FR11_text_output_one_decimal` | designed |

상세 Given/When/Then: [BCE-TC-DESIGN.md](./BCE-TC-DESIGN.md)

---

## Non-Functional Requirements (BCE)

| ID | BCE | 요구사항 | 검증 TC | 상태 |
|----|-----|----------|---------|------|
| NFR-01 | Entity | OCP engine | `test_entity_NFR01_engine_no_unit_branch` | designed |
| NFR-02 | — | SRP 레이어 | entity/control/boundary 디렉터리 | designed |
| NFR-03 | — | pytest | Track 2 전체 | designed |
| NFR-04 | — | FR↔TC | test name + 본 문서 | designed |
| NFR-05 | Control | I/O 분리 | `test_control_NFR05_no_stdin_mock` | designed |
| NFR-06 | Entity | 설정 외부화 | `test_entity_NFR06_engine_no_magic_numbers` | designed |

---

## Dual Track 진행

| Track | 단계 | 산출물 | 상태 |
|-------|------|--------|------|
| 1 | Discovery | BCE-TC-DESIGN, 본 매트릭스, Cursor Rule | ✅ |
| 1 | Red 준비 | TRACK2-RED-ENTRY, BCE README | ✅ |
| 2 | Red | `tests/entity/test_conversion_engine.py` | ⬜ |
| 2 | Green (예시3) | FR-04 engine only | ⬜ |

---

## 테스트 명명 규칙

```
test_{entity|control|boundary}_{FRxx}_{snake_case}
test_{entity|control|boundary}_{NFRxx}_{snake_case}
```

docstring: `FR-xx:` / `NFR-xx:` 로 시작

---

## Activities 매핑

| Activity | Track | 산출 |
|----------|-------|------|
| 1 분석 | 1 | LEGACY-SMELLS ✅ |
| 2 기본+품질 | 2 | Entity/Control Red→Green |
| 3 TC | 2 | BCE pytest |
| 4 추가 | 2 | Boundary FR-05~07 |
| 5 회고 | 1+2 | status → implemented |

---

## 갭 분석 교차 참조

| 갭 ID | FR/NFR |
|-------|--------|
| A4~A6 | NFR-01, NFR-02 |
| A7 | FR-08 |
| A10 | NFR-03 |
| B1~B3 | FR-05~07 |
| C7 | NFR-04 |
