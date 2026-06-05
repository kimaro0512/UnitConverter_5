# tests/boundary — Boundary (BCE)

**역할:** 시스템 경계 — CLI, 설정 파일, 출력 문자열, subprocess.

**대상 모듈 (목표):** `app/cli.py`, `config/*_loader.py`, `output/*_formatter.py`, `input/parser.py`

**상태:** SPEC 준비 — `.py` 테스트 파일 **없음**

**설계:** [BCE-TC-DESIGN.md](../traceability/BCE-TC-DESIGN.md) Boundary 섹션

**도구:** `subprocess`, `tmp_path`, `capsys` (Red 단계에서 선택)
