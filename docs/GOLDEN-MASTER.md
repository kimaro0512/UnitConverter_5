# Golden Master — 승인 기준선 (Baseline)

> **용도:** GREEN PASS 이후 Refactor·회귀 시 **41개 BCE 시나리오 전체** 스냅샷과 비교하는 **단일** 기준선.  
> **규칙:** 기준선 변경은 **의도적** Green/Refactor 완료 후에만 — assert 완화·golden 수동 편집으로 맞추지 않는다.

---

## 구조 (의도한 설계)

| 항목 | 내용 |
|------|------|
| **Golden TC** | `tests/test_golden_master.py::test_golden_master_all_scenarios` **1건** |
| **Golden 파일** | `tests/golden/unit_converter.approved.txt` **1개** |
| **스냅샷 빌더** | `tests/golden_master_report.py` — 41 BCE 시나리오 출력 직렬화 |
| **개별 TC (41건)** | 기존 assert 유지 — Golden Master와 **별도** 회귀 |

---

## GREEN PASS 게이트

| 단계 | 명령 | 기대 |
|------|------|------|
| 1 | `python -m pytest tests/ -q` | **42 passed** (41 BCE + 1 Golden) |
| 2 | Golden만 | `test_golden_master_all_scenarios` → **matched** |

---

## Golden 파일 갱신 (`UPDATE_GOLDEN`)

**전제:** pytest 전체 Green, 출력 변경이 **의도적**일 때만.

### Windows (PowerShell)

```powershell
cd c:\DEV\UnitConverter_5
$env:UPDATE_GOLDEN='1'
python -m pytest tests/test_golden_master.py::test_golden_master_all_scenarios -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/test_golden_master.py::test_golden_master_all_scenarios -v
python -m pytest tests/ -q
```

### Windows (cmd)

```cmd
cd c:\DEV\UnitConverter_5
set UPDATE_GOLDEN=1
python -m pytest tests/test_golden_master.py::test_golden_master_all_scenarios -v
set UPDATE_GOLDEN=
python -m pytest tests/test_golden_master.py::test_golden_master_all_scenarios -v
python -m pytest tests/ -q
```

**흐름:** `UPDATE_GOLDEN=1` → `unit_converter.approved.txt` **덮어쓰기** → git diff **리뷰** → `UPDATE_GOLDEN` 없이 재실행 → **matched** → 커밋.

**금지:** `tests/golden/unit_converter.approved.txt` 수동 편집.

---

## 포맷 (고정)

헬퍼: `tests/_approval.py` — `assert_matches_golden(actual, relative)`

파일은 **41개 블록** — 블록명 알파벳 순, 블록 구분 `\n\n`:

```text
[test_boundary_FR02_cli_stdout_contains_feet]
0
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard

[test_control_FR08_reject_negative_value]
E008 NEGATIVE_VALUE
ValidationError
```

| 블록 종류 | 본문 형식 |
|-----------|-----------|
| CLI 성공 | `format_golden_cli` — exit + stdout |
| CLI/검증 오류 | `E00x NAME` + 예외/메시지 |
| 수치 | `key=NNNNNN` (소수 6자리) |
| 포매터 | `format()` 출력 그대로 |
| NFR 소스 | `flag=true/false` |

**오류 코드:** E008 NEGATIVE_VALUE (FR-08), E009 PARSE_ERROR (FR-09), E010 UNKNOWN_UNIT (FR-10).

---

## 검증 이력

| 일자 | Phase | pytest | 결과 | 비고 |
|------|-------|--------|------|------|
| 2026-06-05 | Green + Golden (v2) | `tests/ -q` | **42 passed** | 단일 `unit_converter.approved.txt` |

---

## 관련 문서

- [.cursor/rules/golden-master.mdc](../.cursor/rules/golden-master.mdc)
- [report/03.REPORT.md](../report/03.REPORT.md)
- [.cursorrules](../.cursorrules)
