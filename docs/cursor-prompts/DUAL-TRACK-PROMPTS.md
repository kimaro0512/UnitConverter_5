# Cursor Dual Track 프롬프트 템플릿

복사 후 `@파일` 참조와 함께 사용. **SPEC 단계**는 Track 1·준비만.

---

## 예시 1 — Track 1: BCE TC 설계 (코드 금지)

```
@README.md @docs/ARCHITECTURE.md @tests/traceability/REQ_TRACEABILITY.md

Dual Track TDD Track 1.
FR-04(meter 기준 변환)에 대해 Entity/Control/Boundary 테스트를 각 2개씩 표로 설계.
- pytest 함수명: test_{entity|control|boundary}_{FR04}_{설명}
- Given/When/Then 포함
- 테스트 코드·production 코드 생성 금지
- 결과는 BCE-TC-DESIGN.md 형식
```

**실행:** Chat (Ask). 산출물을 `BCE-TC-DESIGN.md`에 반영.

---

## 예시 2 — Track 2: Entity Red (Red 진입 **후**)

```
@docs/TRACK2-RED-ENTRY.md @docs/ARCHITECTURE.md @UnitConverter.py

Track 2 Red — Entity only.
1) tests/entity/test_conversion_engine.py 만 생성
2) FR-04: test_entity_FR04_meter_hub_converts_to_feet_and_yard (Red)
3) engine은 NotImplementedError 스텁만
4) pytest tests/entity/ → FAIL 확인
```

**실행:** Agent. `pytest tests/entity/ -v`

---

## 예시 3 — Track 2: Green 한 TC만 (권장)

```
Track 2 Green. test_entity_FR04_meter_hub_converts_to_feet_and_yard 만 PASS.

허용: unit_converter/conversion/engine.py, registry.py,
      unit_converter/domain/*, config/units.json
금지: cli, parser, validator, formatters, loaders, UnitConverter.py

pytest tests/entity/test_conversion_engine.py::test_entity_FR04_meter_hub_converts_to_feet_and_yard -v
```

**실행:** Agent → 터미널에서 pytest 1건 PASSED.

---

## 예시 4 — Cursor Rule

파일: `.cursor/rules/dual-track-tdd.mdc` (저장됨)

**실행:** Rule 자동 적용. 프롬프트 끝에 `Dual Track 1, SPEC only` 또는 `Track 2 Red, FR-04 entity` 추가.

---

## 예시 5 — Control (Red 진입 후, Entity Green 이후)

```
@tests/traceability/BCE-TC-DESIGN.md

Track 2 Red. BCE=control. FR-02 only.
tests/control/test_conversion_service.py
- test_control_FR02_service_convert_input
- stdin/stdout mock 금지 (NFR-05)
- in-memory registry fixture
Red only, service NotImplemented 허용
```

---

## 예시 6 — Boundary CLI (Red 진입 후)

```
Track 2 Red. BCE=boundary. FR-02 CLI.
tests/boundary/test_cli.py
- subprocess로 python -m unit_converter
- stdin "meter:2.5\n", stdout에 feet
Red only — cli/service 연결은 Green에서
```

---

## SPEC 단계용 (현재)

```
@docs/DUAL-TRACK-TDD.md

SPEC 단계 확인. tests/**/*.py 와 unit_converter 구현 없이
Track 2 Red 진입 체크리스트(G5,G6) 빠진 항목만 목록으로 알려줘.
```
