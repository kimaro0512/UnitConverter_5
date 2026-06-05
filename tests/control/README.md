# tests/control — Control (BCE)

**역할:** 유스케이스 조율. Entity를 조합; **stdin/stdout mock 금지** (NFR-05).

**대상 모듈 (목표):** `app/service.py`, `input/validator.py`

**상태:** SPEC 준비 — `.py` 테스트 파일 **없음**

**설계:** [BCE-TC-DESIGN.md](../traceability/BCE-TC-DESIGN.md) Control 섹션

**Red 순서 (권장):** Entity(FR-04) Green 이후 → FR-02 Service → FR-08~10 Validator
