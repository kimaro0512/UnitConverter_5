# BCE 테스트 케이스 설계 (Track 1)

**단계:** SPEC — Given/When/Then 설계만. **pytest 코드 없음.**

명명: `test_{entity|control|boundary}_{FRxx}_{snake_case}`

---

## FR-01 — `단위:값` 파싱

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | 파싱은 Boundary(parser) |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | Service가 parser 호출 — Boundary/Control 경계 |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR01_parse_valid_unit_value` | raw=`"meter:2.5"` | `parse_unit_value(raw)` | `Quantity("meter", 2.5)` |
| `test_boundary_FR01_parse_trims_whitespace` | raw=`" meter:2.5 "` | `parse_unit_value(raw)` | unit=`meter`, value=`2.5` |
| `test_boundary_FR09_reject_missing_colon` | raw=`"meter2.5"` | `parse_unit_value(raw)` | `ParseError` |
| `test_boundary_FR09_reject_non_numeric` | raw=`"meter:abc"` | `parse_unit_value(raw)` | `ParseError` |

---

## FR-02 — 모든 단위로 변환

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| `test_entity_FR02_convert_to_all_registered_units` | registry: meter/feet/yard | `convert(Quantity("meter", 2.5))` | `values` 3개, unit 집합 일치 |
| `test_entity_FR02_feet_input_converts_to_meter` | 동일 registry | `convert(Quantity("feet", 8.2021))` | meter≈2.5 |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR02_service_convert_input` | service + default registry | `convert_input("meter:2.5")` | `ConversionResult`, source.value=2.5 |
| `test_control_FR02_service_returns_all_unit_values` | 동일 | `convert_input("meter:1.0")` | feet·yard·meter 모두 포함 |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR02_cli_stdout_contains_feet` | CLI 빌드됨 | subprocess stdin `meter:2.5\n` | returncode=0, `"feet"` in stdout |
| `test_boundary_FR02_legacy_parity` | UnitConverter.py | 동일 입력 | feet 값 Entity TC와 ±0.1 이내 (선택) |

---

## FR-03 — meter / feet / yard

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| `test_entity_FR03_default_units_in_registry` | `JsonConfigLoader` 또는 default registry | `unit_names()` | `{"meter","feet","yard"}` |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | registry 로드는 Boundary/Entity |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR03_config_json_lists_three_units` | `config/units.json` | load | 3 units |

---

## FR-04 — meter 기준 비율 ⭐ Red 첫 후보

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| `test_entity_FR04_meter_hub_converts_to_feet_and_yard` | ratios: 1, 3.28084, 1.09361 | `convert(Quantity("meter", 1.0))` | feet≈3.28084, yard≈1.09361 |
| `test_entity_FR04_feet_yard_cross_consistent` | 동일 | feet→yard via meter hub | yard/feet ≈ 1.09361/3.28084 |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | engine 위임 |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | 비율은 config, engine에 literal 없음 (NFR-06) |

**Green 범위 (예시 3):** `engine`, `registry`, `domain`, `config/units.json` only.

---

## FR-05 — JSON/YAML 설정 로드

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | — |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | — |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR05_load_units_from_json` | valid `units.json` | `JsonConfigLoader.load` | `has_unit("feet")` |
| `test_boundary_FR05_load_units_from_yaml` | valid `units.yaml` | `YamlConfigLoader.load` | `has_unit("yard")` |
| `test_boundary_FR05_missing_file_raises` | path 없음 | `load` | 적절한 예외 |

---

## FR-06 — 동적 단위 등록

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| `test_entity_FR06_registry_stores_cubit` | empty registry | `register(cubit 0.4572)` | `has_unit("cubit")` |
| `test_entity_FR06_cubit_in_conversion_output` | cubit 등록됨 | `convert(Quantity("meter",1))` | values에 cubit |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR06_service_register_and_convert` | service | register + convert | cubit 결과 포함 |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR06_parse_register_cubit` | raw=`"1 cubit = 0.4572 meter"` | `parse_unit_registration` | `UnitDefinition("cubit", 0.4572)` |

---

## FR-07 — JSON / CSV / 표 출력

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | 포맷은 Boundary |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR07_service_format_json` | sample `ConversionResult` | `format_result(..., JsonFormatter())` | valid JSON string |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR07_json_format` | sample result | `JsonFormatter.format` | `"feet"` in output |
| `test_boundary_FR07_csv_format` | sample result | `CsvFormatter.format` | comma-separated |
| `test_boundary_FR07_table_format` | sample result | `TableFormatter.format` | header + rows |
| `test_boundary_FR07_factory_all_formats` | — | `get_formatter(name)` | text/json/csv/table |

---

## FR-08 — 음수 거부

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | — |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR08_reject_negative_value` | registry + validator | `validate(Quantity("meter", -1))` | `ValidationError` |
| `test_control_FR08_zero_allowed` | validator | `validate(Quantity("meter", 0))` | 예외 없음 (0 허용 여부 SPEC: **허용**) |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR08_cli_negative_exit_nonzero` | CLI | stdin `meter:-1\n` | 비정상 종료 또는 오류 메시지 |

---

## FR-09 — 잘못된 형식

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | — |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR09_service_invalid_format` | service | `convert_input("invalid")` | `ParseError` or `ValidationError` |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| (FR-01 boundary TC와 공유) | | | |

---

## FR-10 — unknown unit

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| — | — | — | — |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| `test_control_FR10_reject_unknown_unit` | validator, registry without mile | `validate(Quantity("mile", 1))` | `UnknownUnitError` |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR10_cli_unknown_unit` | CLI | stdin `mile:1\n` | 오류, 변환 출력 없음 |

---

## FR-11 — 1자리 반올림

### Entity
| TC | Given | When | Then |
|----|-------|------|------|
| `test_entity_FR11_rounding_policy_one_decimal` | `ConversionResult.rounded_value(8.2021)` | round | `8.2` |

### Control
| TC | Given | When | Then |
|----|-------|------|------|
| — | formatter 위임 | | |

### Boundary
| TC | Given | When | Then |
|----|-------|------|------|
| `test_boundary_FR11_text_output_one_decimal` | result meter 2.5 | `TextFormatter.format` | `"8.2"` and `"2.7"` in output (README 예시) |

---

## NFR (BCE 배치)

| ID | BCE | TC (설계명) | 검증 |
|----|-----|-------------|------|
| NFR-01 | Entity | `test_entity_NFR01_engine_no_unit_branch` | engine 소스에 `elif unit` 없음 |
| NFR-02 | — | 구조 리뷰 | entity/control/boundary 디렉터리 분리 |
| NFR-03 | — | Track 2 | pytest 전체 |
| NFR-04 | — | 명명 규칙 | FR-ID in test name |
| NFR-05 | Control | `test_control_NFR05_no_stdin_mock` | service 테스트에 mock stdin 없음 |
| NFR-06 | Entity | `test_entity_NFR06_engine_no_magic_numbers` | engine에 `3.28084` 없음 |

---

## 상태

| 항목 | 값 |
|------|-----|
| Track | 1 (Discovery) — **Red 준비 완료** |
| pytest `.py` | 없음 |
| Red 첫 TC | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` |

**다음:** [TRACK2-RED-ENTRY.md](../../docs/TRACK2-RED-ENTRY.md) Gate G5~G6 후 Red.
