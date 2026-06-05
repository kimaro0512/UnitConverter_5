# Dual Track TDD + Cursor AI + BCE (UnitConverter_5)

**현재 단계:** SPEC / **Red 진입 준비** — TC 설계·규칙·디렉터리만. `tests/**/*.py`·`unit_converter/` 구현 **없음**.

| 문서 | 역할 |
|------|------|
| [BCE-TC-DESIGN.md](../tests/traceability/BCE-TC-DESIGN.md) | FR/NFR BCE TC Given/When/Then |
| [REQ_TRACEABILITY.md](../tests/traceability/REQ_TRACEABILITY.md) | FR ↔ 모듈 ↔ TC 추적 |
| [TRACK2-RED-ENTRY.md](./TRACK2-RED-ENTRY.md) | Red Gate·Cycle 1(FR-04)·예시 3 Green 범위 |
| [cursor-prompts/DUAL-TRACK-PROMPTS.md](./cursor-prompts/DUAL-TRACK-PROMPTS.md) | Cursor 프롬프트 6종 |
| [.cursor/rules/dual-track-tdd.mdc](../.cursor/rules/dual-track-tdd.mdc) | AI 상시 규칙 |

---

## 1. Dual Track TDD

| Track | 이름 | 목적 | 산출물 |
|-------|------|------|--------|
| **1** | Discovery | *무엇이 맞는가* | SPEC, BCE TC 설계, Mom Test |
| **2** | Delivery | *어떻게 맞게* | Red → Green → Refactor |

```
Track 1 (현재) ──► Track 2 Red ──► Green ──► Refactor
   SPEC/BCE           pytest FAIL    PASS      정리
```

---

## 2. BCE 매핑

| BCE | 디렉터리 | 모듈 | I/O |
|-----|----------|------|-----|
| **Entity** | `tests/entity/` | engine, registry, domain | 금지 |
| **Control** | `tests/control/` | service, validator | stdin mock 금지 |
| **Boundary** | `tests/boundary/` | cli, parser, loaders, formatters | 허용 |

상세: [ARCHITECTURE.md](./ARCHITECTURE.md) · [tests/entity/README.md](../tests/entity/README.md)

---

## 3. Cursor AI 기술 (6예시)

| # | 용도 | Track | 문서 |
|---|------|-------|------|
| 1 | BCE TC 설계 | 1 | [프롬프트 #1](./cursor-prompts/DUAL-TRACK-PROMPTS.md) |
| 2 | Entity Red | 2 | #2 |
| 3 | Green 한 TC (FR-04) | 2 | #3 · [TRACK2-RED-ENTRY](./TRACK2-RED-ENTRY.md) |
| 4 | Cursor Rule | 1+2 | `.cursor/rules/dual-track-tdd.mdc` |
| 5 | Control Red | 2 | #5 |
| 6 | Boundary CLI Red | 2 | #6 |

**SPEC 단계:** 예시 1·4·SPEC용 프롬프트만 사용.

---

## 4. Track별 Cursor 모드

| 작업 | 모드 |
|------|------|
| BCE 설계, FR 분해 | Chat (Ask) |
| SPEC markdown | Agent (docs only) |
| Red TC `.py` | Agent (**Red 선언 후**) |
| Green 최소 구현 | Agent + FR-ID 1개 |
| 소규모 Refactor | Inline (Ctrl+K) |

---

## 5. Dual Track 실행 루틴 (6h Activities)

| # | Track | 작업 | 산출 |
|---|-------|------|------|
| 1 | 1 | 레거시·PRD 갭 | LEGACY-SMELLS-AND-PRD-GAP.md ✅ |
| 2 | 1 | 아키텍처 SPEC | ARCHITECTURE.md ✅ |
| 3 | 1 | BCE TC 설계 | BCE-TC-DESIGN.md ✅ |
| 4 | 1 | Red 진입 체크리스트 | TRACK2-RED-ENTRY.md ✅ |
| 5 | 2 | G5 pyproject + 스켈레톤 | pyproject.toml ⬜ |
| 6 | 2 | Entity Red FR-04 | tests/entity/*.py ⬜ |
| 7 | 2 | Green (예시 3) | engine/registry ⬜ |
| 8 | 2 | Control → Boundary | 순차 ⬜ |
| 9 | 2 | Refactor | ⬜ |
| 10 | 1+2 | 회고, traceability `implemented` | ⬜ |

---

## 6. BCE TC 설계

전 FR-01~11 + NFR: [BCE-TC-DESIGN.md](../tests/traceability/BCE-TC-DESIGN.md)

**Red 첫 TC:** `test_entity_FR04_meter_hub_converts_to_feet_and_yard`

---

## 7. pytest 명령 (Track 2 진입 후)

```bash
pytest tests/entity/ -v
pytest tests/control/ -v
pytest tests/boundary/ -v
pytest -k "entity and FR04" -v
pytest --collect-only -q
```

환경 SPEC: [pyproject.toml.spec](./pyproject.toml.spec)

---

## 8. 주의사항

1. SPEC 단계에서 Red `.py` 작성하지 않기  
2. Entity TC에 `input()`/`print()` 넣지 않기  
3. Track 2에서 FR-ID **하나** + BCE **한 층**만 Agent에 요청  
4. Green(예시 3)에서 허용 파일 범위 초과 금지  
5. `UnitConverter.py`는 Red/Green 범위에서 별도 명시 전까지 유지  

---

## 9. 저장소 현황

| 있음 | 없음 (Red Gate) |
|------|-----------------|
| `UnitConverter.py` 레거시 | `tests/**/*.py` |
| SPEC docs, BCE 설계 | `pyproject.toml` (spec만) |
| `tests/entity|control|boundary/README` | Red 실행 |

---

## 10. 한 줄 요약

**Track 1(SPEC) 완료 → Track 2 Red는 [TRACK2-RED-ENTRY.md](./TRACK2-RED-ENTRY.md) Gate G5~G6 후 Entity FR-04부터.**

Red 시작 선언:

```
Track 2 Red 시작. @docs/TRACK2-RED-ENTRY.md
```
