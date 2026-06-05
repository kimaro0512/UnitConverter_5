# Unit Converter — 패키지 구조 (OCP / SRP)

README(PRD)와 [LEGACY-SMELLS-AND-PRD-GAP.md](../LEGACY-SMELLS-AND-PRD-GAP.md)를 반영한 **교육용 실습** 아키텍처 **설계 SPEC**입니다.

> **현재 단계:** SPEC 정리 — 아래 `unit_converter/` 트리는 **목표 구조**이며, 저장소에는 아직 **구현 코드 없음**.  
> **현재 코드:** [UnitConverter.py](../UnitConverter.py) (레거시)만 존재.

---

## 1. 목표 패키지 트리 (구현 전)

```
UnitConverter_5/
├── pyproject.toml
├── README.md
├── UnitConverter.py               # (선택) 레거시 호환 thin wrapper → unit_converter.app.cli
│
├── config/
│   └── units.json                 # FR-05: 기본 변환 비율 (meter 기준)
│
├── unit_converter/
│   ├── __init__.py
│   ├── __main__.py                # python -m unit_converter
│   │
│   ├── domain/                    # SRP: 순수 도메인 모델·예외
│   │   ├── __init__.py
│   │   ├── models.py              # Quantity, UnitDefinition, ConversionResult
│   │   └── exceptions.py          # ParseError, ValidationError, UnknownUnitError
│   │
│   ├── conversion/                # SRP+OCP: 변환 핵심 (I/O 없음)
│   │   ├── __init__.py
│   │   ├── protocols.py           # UnitRegistryPort, ConversionStrategy (Protocol/ABC)
│   │   ├── registry.py            # UnitRegistry — 단위 등록·조회
│   │   └── engine.py              # ConversionEngine — 기준단위 경유 일괄 변환
│   │
│   ├── config/                    # SRP+OCP: 설정 로드
│   │   ├── __init__.py
│   │   ├── protocols.py           # ConfigLoader Protocol
│   │   ├── json_loader.py         # JsonConfigLoader
│   │   └── yaml_loader.py         # YamlConfigLoader (확장, OCP)
│   │
│   ├── input/                     # SRP: 입력 처리
│   │   ├── __init__.py
│   │   ├── parser.py              # "meter:2.5" → Quantity
│   │   ├── validator.py             # 음수·형식·단위 검증 (규칙 조합)
│   │   └── unit_registration_parser.py  # "1 cubit = 0.4572 meter"
│   │
│   ├── output/                    # SRP+OCP: 출력 포맷
│   │   ├── __init__.py
│   │   ├── protocols.py           # OutputFormatter Protocol
│   │   ├── text_formatter.py      # 기본 줄 출력 (README 예시)
│   │   ├── json_formatter.py
│   │   ├── csv_formatter.py
│   │   └── table_formatter.py
│   │
│   └── app/                       # SRP: 유스케이스·진입점
│       ├── __init__.py
│       ├── service.py             # ConversionService (오케스트레이션)
│       └── cli.py                 # stdin/stdout, 포맷·설정 경로 CLI 옵션
│
├── tests/
│   ├── entity/                  # BCE Entity — README only (SPEC)
│   ├── control/                 # BCE Control — README only (SPEC)
│   ├── boundary/                # BCE Boundary — README only (SPEC)
│   └── traceability/
│       ├── REQ_TRACEABILITY.md
│       └── BCE-TC-DESIGN.md
│
└── docs/
    ├── ARCHITECTURE.md
    ├── DUAL-TRACK-TDD.md        # Dual Track + BCE 가이드 (§1~10)
    ├── TRACK2-RED-ENTRY.md      # Red Gate · 예시3 Green 범위
    ├── pyproject.toml.spec      # Track 2 Day1 템플릿
    └── cursor-prompts/
        └── DUAL-TRACK-PROMPTS.md
```

> **Dual Track SPEC:** [DUAL-TRACK-TDD.md](./DUAL-TRACK-TDD.md) · Red 준비: [TRACK2-RED-ENTRY.md](./TRACK2-RED-ENTRY.md)

---

## 2. OCP / SRP 적용 원칙

### SRP — 한 모듈 = 한 변경 이유

| 모듈 | 단일 책임 |
|------|-----------|
| `domain/models` | 값 객체·결과 구조 정의 |
| `input/parser` | 문자열 → 구조화 데이터 |
| `input/validator` | 비즈니스 규칙 검증 |
| `conversion/registry` | 단위 정의 저장·조회 |
| `conversion/engine` | 기준단위 경유 수치 변환 |
| `config/*_loader` | 파일 → registry 초기화 |
| `output/*_formatter` | `ConversionResult` → 문자열 |
| `app/service` | 유스케이스 조합 (테스트 진입점) |
| `app/cli` | 사용자 I/O·옵션 파싱만 |

### OCP — 확장 시나리오

| 확장 | 추가 | 수정 (최소) |
|------|------|-------------|
| 단위 추가 (mile) | `config/units.json` 또는 `registry.register()` | 없음 |
| 출력 포맷 (Markdown) | `output/markdown_formatter.py` | factory 등록 1곳 |
| 설정 포맷 (TOML) | `config/toml_loader.py` | loader wiring 1곳 |
| 검증 규칙 (max value) | validator rule 클래스 | validator 조합 |

### 핵심 Protocol (개념)

```python
# conversion/protocols.py — OutputFormatter는 output/protocols.py
class ConfigLoader(Protocol):
    def load(self, path: Path) -> UnitRegistry: ...

class OutputFormatter(Protocol):
    def format(self, result: ConversionResult) -> str: ...
```

`ConversionEngine`은 **registry만** 의존합니다. meter hub는 `UnitDefinition` / registry에 캡슐화합니다.

---

## 3. PRD 요구사항 ID

> **ID SSOT:** 본 절 FR-01~11, NFR-01~06. TC·코드·문서는 상세 ID만 사용.  
> Given/When/Then·BCE 매핑: [REQ_TRACEABILITY.md](../tests/traceability/REQ_TRACEABILITY.md).

### Functional Requirements (FR)

| ID | 요구사항 | README 출처 |
|----|----------|-------------|
| FR-01 | `단위:값` 형식 입력 파싱 | 기본 #1 |
| FR-02 | 지원 모든 단위로 변환 출력 | Overview, 기본 #1 |
| FR-03 | 초기 단위: meter, feet, yard | 기본 #2 |
| FR-04 | meter 기준 비율 계산 | 비즈니스 로직 |
| FR-05 | JSON/YAML 설정에서 비율 로드 | 추가 #1 |
| FR-06 | 동적 단위 등록 (`1 cubit = 0.4572 meter`) | 추가 #2 |
| FR-07 | 출력 포맷 JSON / CSV / 표 | 추가 #3 |
| FR-08 | 음수 입력 거부 | 품질-입력검증 |
| FR-09 | 잘못된 형식 거부 | 품질-입력검증 |
| FR-10 | 없는 단위 거부 | 품질-입력검증 |
| FR-11 | README 예시 수준 반올림 출력 | 기본 #1 예시 |

### Non-Functional Requirements (NFR)

| ID | 요구사항 | README 출처 |
|----|----------|-------------|
| NFR-01 | OCP — 단위 추가 시 기존 코드 변경 최소 | 기본 #3, 품질 |
| NFR-02 | SRP — 클래스/모듈 단일 책임 | 품질 |
| NFR-03 | TC로 변환·검증 검증 | Overview, Activities |
| NFR-04 | FR/NFR ↔ 모듈 ↔ TC 추적 | 워크샵 목표 |
| NFR-05 | 핵심 로직 I/O 분리 (단위 테스트 가능) | 품질·Activities |
| NFR-06 | magic number 제거, 설정 외부화 | 추가 #1 |

---

## 4. FR/NFR → 모듈 매핑

### FR

| ID | 주 담당 | 협력 |
|----|---------|------|
| FR-01 | `input/parser.py` | `domain/models.py` |
| FR-02 | `conversion/engine.py` | `registry.py`, `output/*` |
| FR-03 | `config/units.json` | `registry.py` |
| FR-04 | `domain/models.py` | `engine.py` |
| FR-05 | `config/json_loader.py`, `yaml_loader.py` | `registry.py` |
| FR-06 | `input/unit_registration_parser.py` | `registry.register()` |
| FR-07 | `output/*_formatter.py` | `app/cli.py` |
| FR-08~10 | `input/validator.py` | `exceptions.py` |
| FR-11 | `output/*_formatter.py` | rounding policy in domain |

### NFR

| ID | 구조적 대응 | 검증 |
|----|-------------|------|
| NFR-01 | Protocol + registry/factory | 단위 추가 시 engine diff 0 |
| NFR-02 | 레이어 분리 | 모듈별 unit test |
| NFR-03 | `tests/` | pytest |
| NFR-04 | `tests/traceability/REQ_TRACEABILITY.md` | FR-ID in test names |
| NFR-05 | `app/service.py` public API | service without mock I/O |
| NFR-06 | `config/units.json`, loaders | no literals in engine |

상세 TC 매핑은 [REQ_TRACEABILITY.md](../tests/traceability/REQ_TRACEABILITY.md)를 참고하세요.

---

## 5. 데이터 흐름

```
CLI (app/cli.py)
  → Parser (FR-01) → Validator (FR-08~10)
  → ConversionService (app/service.py)
       → UnitRegistry ← ConfigLoader (FR-05) / register (FR-06)
       → ConversionEngine (FR-02, FR-04)
       → ConversionResult
  → OutputFormatter (FR-07, FR-11) → stdout
```

---

## 6. import 의존 방향

```
app        →  input, output, conversion, config, domain
conversion, input, output, config  →  domain
domain     →  stdlib only
tests      →  public API
```

`conversion`은 `input` / `output` / `cli`를 import하지 않습니다.

---

## 7. 레거시 마이그레이션

| UnitConverter.py | 신 구조 |
|------------------|---------|
| `main()` | `app/cli.py` + `app/service.py` |
| if/elif 단위 | `registry` + `engine` |
| 하드코딩 비율 | `config/units.json` |
| print 3줄 | `TextFormatter` |

레거시 호환 thin wrapper:

```python
from unit_converter.app.cli import main

if __name__ == "__main__":
    main()
```

---

## 8. 실행 (구현 후)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -e ".[dev]"
python -m unit_converter
# pytest — TC 코드 작성 후 (설계: tests/traceability/REQ_TRACEABILITY.md)
# 또는
unit-converter
```
