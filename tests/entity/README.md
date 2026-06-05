# tests/entity — Entity (BCE)

**역할:** 순수 도메인·변환 규칙. `stdin`/`stdout`/`open()` 사용 **금지**.

**대상 모듈 (목표):** `domain/*`, `conversion/engine.py`, `conversion/registry.py`

**상태:** SPEC 준비 — `.py` 테스트 파일 **없음** (Red 진입 전)

**설계:** [BCE-TC-DESIGN.md](../traceability/BCE-TC-DESIGN.md) Entity 섹션

**Red 진입 후 첫 TC (권장):** `test_entity_FR04_meter_hub_converts_to_feet_and_yard`
