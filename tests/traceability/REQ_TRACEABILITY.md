# 요구사항 추적성 매트릭스 (FR / NFR)

PRD: [README.md](../../README.md)  
아키텍처: [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)

**단계:** SPEC 정리 — 본 문서는 **TC 설계(추적성)** 만 포함하며, `unit_converter/` 패키지·`tests/**/*.py` 코드는 **아직 없음**.

**상태:** `designed` = TC 설계만 완료, `implemented` = 테스트 코드 작성·통과

---

## Functional Requirements

| ID | 요구사항 | 모듈 | 테스트 파일 | 테스트 케이스 (제안명) | 상태 |
|----|----------|------|-------------|------------------------|------|
| FR-01 | `단위:값` 파싱 | `unit_converter/input/parser.py` | `tests/unit/test_parser.py` | `test_FR01_parse_valid_unit_value` | designed |
| FR-01 | 공백 trim | `unit_converter/input/parser.py` | `tests/unit/test_parser.py` | `test_FR01_parse_trims_whitespace` | designed |
| FR-02 | 모든 단위로 변환 | `unit_converter/conversion/engine.py` | `tests/unit/test_engine.py` | `test_FR02_convert_to_all_registered_units` | designed |
| FR-02 | E2E 변환 | `unit_converter/app/service.py` | `tests/integration/test_service.py` | `test_FR02_service_convert_meter_input` | designed |
| FR-03 | meter/feet/yard | `config/units.json`, `registry.py` | `tests/unit/test_engine.py` | `test_FR03_default_units_present` | designed |
| FR-04 | meter 기준 비율 | `unit_converter/conversion/engine.py` | `tests/unit/test_engine.py` | `test_FR04_feet_yard_consistent_via_meter` | designed |
| FR-05 | JSON 로드 | `unit_converter/config/json_loader.py` | `tests/unit/test_config_loaders.py` | `test_FR05_load_units_from_json` | designed |
| FR-05 | YAML 로드 | `unit_converter/config/yaml_loader.py` | `tests/unit/test_config_loaders.py` | `test_FR05_load_units_from_yaml` | designed |
| FR-06 | cubit 등록 | `unit_converter/input/unit_registration_parser.py` | `tests/unit/test_unit_registration_parser.py` | `test_FR06_parse_register_cubit` | designed |
| FR-06 | 등록 후 변환 | `unit_converter/conversion/registry.py` | `tests/unit/test_registry.py` | `test_FR06_registered_unit_used_in_conversion` | designed |
| FR-07 | JSON 출력 | `unit_converter/output/json_formatter.py` | `tests/unit/test_formatters.py` | `test_FR07_json_format` | designed |
| FR-07 | CSV 출력 | `unit_converter/output/csv_formatter.py` | `tests/unit/test_formatters.py` | `test_FR07_csv_format` | designed |
| FR-07 | 표 출력 | `unit_converter/output/table_formatter.py` | `tests/unit/test_formatters.py` | `test_FR07_table_format` | designed |
| FR-08 | 음수 거부 | `unit_converter/input/validator.py` | `tests/unit/test_validator.py` | `test_FR08_reject_negative_value` | designed |
| FR-09 | 형식 오류 | `unit_converter/input/parser.py`, `validator.py` | `tests/unit/test_parser.py`, `test_validator.py` | `test_FR09_reject_missing_colon`, `test_FR09_reject_non_numeric` | designed |
| FR-10 | unknown unit | `unit_converter/input/validator.py` | `tests/unit/test_validator.py` | `test_FR10_reject_unknown_unit` | designed |
| FR-11 | 1자리 반올림 | `unit_converter/output/text_formatter.py` | `tests/unit/test_formatters.py` | `test_FR11_text_output_one_decimal` | designed |

---

## Non-Functional Requirements

| ID | 요구사항 | 구조 / 모듈 | 테스트 / 검증 | 상태 |
|----|----------|-------------|---------------|------|
| NFR-01 | OCP — 단위 추가 시 engine 불변 | `conversion/protocols.py`, `registry.py`, `engine.py` | `test_NFR01_engine_source_has_no_unit_specific_branches` in `test_package_structure.py` | designed |
| NFR-02 | SRP — 모듈별 단일 책임 | 패키지 레이어 (`domain`, `input`, …) | `test_NFR02_subpackages_exist` in `test_package_structure.py` | designed |
| NFR-03 | TC로 로직 검증 | `tests/` | `pytest` CI, coverage on `unit_converter` | designed |
| NFR-04 | FR ↔ TC 추적 | 본 문서 | PR/리뷰 시 FR-ID in test name | designed |
| NFR-05 | I/O 분리 | `app/service.py` vs `app/cli.py` | `test_NFR05_service_runs_without_stdin` in `test_service.py` | designed |
| NFR-06 | 설정 외부화 | `config/units.json`, loaders | `test_NFR06_engine_has_no_magic_numbers` in `test_package_structure.py` | designed |

---

## README 섹션 → FR/NFR 매핑

| README | 요구 ID |
|--------|---------|
| Overview — `단위:값` 변환 | FR-01, FR-02 |
| Overview — 단위 추가 변경 최소 | NFR-01 |
| Overview — TC 검증 | NFR-03 |
| 기본 #1 입출력 예시 | FR-01, FR-02, FR-11 |
| 기본 #2 지원 단위 | FR-03 |
| 기본 #3 OCP | NFR-01 |
| 기본 #4 TC | NFR-03 |
| 비즈니스 로직 meter 기준 | FR-04 |
| 품질 OCP/SRP | NFR-01, NFR-02 |
| 품질 입력 검증 | FR-08, FR-09, FR-10 |
| 추가 설정 외부화 | FR-05, NFR-06 |
| 추가 동적 등록 | FR-06 |
| 추가 출력 포맷 | FR-07 |

---

## 구현 체크리스트 (Activities 순서)

| 단계 | README Activity | FR/NFR | 산출물 |
|------|-----------------|--------|--------|
| 1 | 문제 코드 분석 | — | LEGACY-SMELLS-AND-PRD-GAP.md |
| 2 | 기본+품질 구현 | FR-01~04, FR-08~10, NFR-01~02, NFR-05~06 | domain, conversion, input, app/service |
| 3 | TC 구현 | NFR-03, NFR-04 | tests/unit/* (본 문서 설계 → 코드 작성) |
| 4 | 추가 요구 | FR-05~07 | config/, output/, registration |
| 5 | 회고 | NFR-04 | 본 매트릭스 status → implemented |

---

## 테스트 명명 규칙

```python
def test_FR01_parse_valid_unit_value():
    """FR-01: unit:value 형식을 Quantity로 파싱한다."""
    ...
```

- 함수명: `test_{FR|NFR}{ID}_{snake_case_description}`
- docstring 첫 줄: `FR-xx:` 또는 `NFR-xx:` 로 시작

---

## 갭 분석 교차 참조

| 갭 ID (LEGACY doc) | 해소 FR/NFR |
|--------------------|-------------|
| A4~A6 OCP/SRP/클래스 | NFR-01, NFR-02 |
| A7 음수 | FR-08 |
| A10 TC | NFR-03 |
| B1~B3 추가 요구 | FR-05~07 |
| C7 PRD↔TC 추적 | NFR-04, 본 문서 |
