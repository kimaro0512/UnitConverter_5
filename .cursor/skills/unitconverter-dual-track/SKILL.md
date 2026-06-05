---
name: unitconverter-dual-track
description: >-
  UnitConverter_5 Dual Track TDD Red/Green/Refactor 절차. Track 2, FR-04 Entity Red,
  pytest Red→Green, BCE 레이어별 TC 작성, Green 허용 파일 범위 확인 시 사용.
---

# UnitConverter Dual Track (Track 2)

Rules(`.cursor/rules/dual-track-tdd.mdc`)는 **제약**만 정의한다. 본 Skill은 **절차**와 **FR별 Green 범위**를 안내한다.

## 선행 확인

1. 사용자가 **"Track 2"** 또는 **"Red 시작"**을 명시했는지 확인. 없으면 Track 1(SPEC only) 유지.
2. Gate G5~G6 미완이면 `docs/TRACK2-RED-ENTRY.md` §1부터 처리.
3. 상세 FR·TC·Green 범위: [reference.md](./reference.md) 및 `@tests/traceability/BCE-TC-DESIGN.md`.

## 응답 선언 (필수)

작업 시작 시 한 줄:

`Phase: Red|Green|Refactor` · `Layer: entity|control|boundary` · `Track: 2` · `FR-{xx}`

## Red 절차

1. **한 FR-ID + 한 BCE 레이어**만 선택 (`reference.md` 권장 순서 참고).
2. `tests/{entity|control|boundary}/test_*.py`에 TC **1개**(또는 설계상 동일 FR 묶음)만 추가.
3. 함수명: `test_{entity|control|boundary}_{FRxx}_{snake_case}` · docstring 첫 줄 `FR-xx:`.
4. production은 **NotImplementedError 스텁**만 허용(Red 단계).
5. pytest 실행 → **FAILED** 확인( import / NotImplemented / assertion ).
6. Agent 프롬프트 끝에 포함:

   `Dual Track 2. BCE={layer} only. FR-{xx} one item. Do not modify SPEC docs unless asked.`

## Green 절차

1. **방금 Red에서 실패한 TC 1건**만 PASS 목표.
2. `reference.md`의 해당 FR **허용 파일**만 수정. 범위 밖 파일 금지.
3. `config/units.json`만 비율 SSOT — engine/parser/테스트에 `3.28084`/`1.09361` 리터럴 금지.
4. pytest **단일 TC** 실행 → PASSED 확인.
5. assert 완화·skip·xfail·테스트 삭제로 Green **금지**.

## Refactor 절차

1. **같은 FR 범위** 내에서만 정리(registry hub, 중복 제거 등).
2. 해당 FR pytest 전부 PASS 유지.
3. `REQ_TRACEABILITY.md` status 갱신은 사용자 요청 시만.

## Gate G5~G6 (Red 진입 Day 1)

```bash
python -m venv venv
venv\Scripts\activate          # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

- `pyproject.toml` + `docs/pyproject.toml.spec` 참고
- `unit_converter/` 최소 스켈레톤만 (첫 Red: Entity FR-04)

## 첫 사이클 (권장)

| 단계 | 내용 |
|------|------|
| Red | `test_entity_FR04_meter_hub_converts_to_feet_and_yard` |
| Green 허용 | `engine.py`, `registry.py`, `domain/*`, `config/units.json` |
| pytest | `pytest tests/entity/test_conversion_engine.py::test_entity_FR04_meter_hub_converts_to_feet_and_yard -v` |

## @ 참조 (작업 시)

- `docs/TRACK2-RED-ENTRY.md`
- `tests/traceability/BCE-TC-DESIGN.md`
- `tests/traceability/REQ_TRACEABILITY.md`
- `docs/cursor-prompts/DUAL-TRACK-PROMPTS.md` (프롬프트 템플릿)

## Command 대체

별도 `.cursor/commands/` 없이 본 Skill + `/unitconverter-dual-track` 또는 자동 감지로 Red/Green 절차를 실행한다.
