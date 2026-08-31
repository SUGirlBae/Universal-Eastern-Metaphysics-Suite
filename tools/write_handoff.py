# -*- coding: utf-8 -*-
import sys

content = """# Handoff Report: Metaphysical Canonical Edge-Case & Adversarial Audit

**Agent**: challenger_2 (Metaphysical Canonical Edge-Case Challenger)  
**Timestamp**: 2026-08-30T16:15:00Z  
**Verdict**: **REQUEST_CHANGES** (Actionable canonical bug fixes and schema adjustments required)

---

## 1. Observation

### 1.1 Bát Tự Hà Lạc (engine/ha_lac_engine.py)
- **File**: engine/ha_lac_engine.py, lines 57–76 and 38–47.
- **Code observed**:
```python
# Lines 38-47: NUM_TO_TRIGRAM maps Lac Thu number to Trigram ID
NUM_TO_TRIGRAM = {
    1: 6,  # Khảm (1) -> Trigram 6
    2: 8,  # Khôn (2) -> Trigram 8
    3: 4,  # Chấn (3) -> Trigram 4
    4: 5,  # Tốn (4) -> Trigram 5
    6: 1,  # Càn (6) -> Trigram 1
    7: 2,  # Đoài (7) -> Trigram 2
    8: 7,  # Cấn (8) -> Trigram 7
    9: 3   # Ly (9) -> Trigram 3
}
```
```python
# Lines 71-76: reduce_ha_lac_num logic for Palace 5 lodging
    if single == 5:
        if is_duong_nam_or_am_nu:
            single = 7 if is_heaven else 8  # Thiên -> Cấn (7), Địa -> Khôn (8)
        else:
            single = 8 if is_heaven else 7  # Thiên -> Khôn (8), Địa -> Cấn (7)
    return single
```
- **Empirical Execution Result**:
```
Yang Male / Yin Female Heaven 5: reduce returns 7 -> NUM_TO_TRIGRAM -> Trigram 2 (Đoài) [Expected: Cấn]
Yang Male / Yin Female Earth 5 : reduce returns 8 -> NUM_TO_TRIGRAM -> Trigram 7 (Cấn) [Expected: Khôn]
Yin Male / Yang Female Heaven 5: reduce returns 8 -> NUM_TO_TRIGRAM -> Trigram 7 (Cấn) [Expected: Khôn]
Yin Male / Yang Female Earth 5 : reduce returns 7 -> NUM_TO_TRIGRAM -> Trigram 2 (Đoài) [Expected: Cấn]
[FAIL] ha_lac_palace_5_ky_cung: CANONICAL MISMATCH: Heaven 5 for Yang Male mapped to Đoài (expected Cấn); Earth 5 mapped to Cấn (expected Khôn).
```

### 1.2 Huyền Không Vận 9 Castle Gate (engine/feng_shui.py)
- **File**: engine/feng_shui.py, lines 192–193.
- **Code observed**:
```python
    left_p = (facing_palace_id % 9) + 1
    right_p = ((facing_palace_id - 2) % 9) + 1
```
- **Empirical Execution Result**:
For facing="Ngọ" (Ly 9, South):
`left_p` was computed as `(9 % 9) + 1 = 1` (Khảm 1 - North).
`right_p` was computed as `((9 - 2) % 9) + 1 = 8` (Cấn 8 - Northeast).
Output: `Đắc Thành Môn Quyết: Cung Khảm 1 (Bắc) (Hướng tinh 9)`.
In reality, the physical adjacent gates flanking South (Ly 9) on the Luopan compass are Southeast (Tốn 4) and Southwest (Khôn 2). Khảm 1 is the directly opposite sitting palace (North), NOT a flanking Castle Gate.

### 1.3 FTS5 SQLite Syntax Error on Search Queries (engine/tuvi_rule_extractor.py)
- **File**: engine/tuvi_rule_extractor.py, line 168.
- **Code observed**: `WHERE tuvi_rules_fts MATCH ?` with raw unsanitized user query string.
- **Empirical Execution Result**:
Running `search_tuvi_rules('Tử Vi & Thiên Phủ')` threw verbatim exception:
`sqlite3.OperationalError: fts5: syntax error near "&"`.

### 1.4 Test Suite Failures (pytest -q)
- Running `pytest -q` resulted in `20 failed, 187 passed, 1 skipped in 57.99s`.
- Specific errors include:
  - `KeyError: 'menh_palace_branch'` and `'lunar_year_name'` in `test_tier1_tu_vi_advanced.py` and `test_tier2_boundaries.py`.
  - `TypeError: string indices must be integers, not 'str'` in `test_tier3_cross_discipline.py` (`analyze_wuxing_interaction`).
  - `AssertionError: 0 == 1` in `test_tier4_real_world.py` (`test_case_tracker_full_lifecycle`).

---

## 2. Logic Chain

1. **Bát Tự Hà Lạc Lodging Inversion**:
   - *Observation*: `reduce_ha_lac_num` returns 7 for Heaven 5 and 8 for Earth 5.
   - *Mapping*: `NUM_TO_TRIGRAM[7] == 2` (Đoài) and `NUM_TO_TRIGRAM[8] == 7` (Cấn).
   - *Rule*: In canonical Hà Lạc Lý Số (Thiệu Ung), Yang Male / Yin Female Heaven 5 must lodge in Cấn (Trigram 7) and Earth 5 in Khôn (Trigram 8).
   - *Deduction*: To map to Trigram Cấn (7), the Lạc Thư number must be 8 (`NUM_TO_TRIGRAM[8] = 7`). To map to Trigram Khôn (8), the Lạc Thư number must be 2 (`NUM_TO_TRIGRAM[2] = 8`).
   - *Root cause*: `reduce_ha_lac_num` confused trigram IDs (7=Cấn, 8=Khôn) with Lạc Thư numbers (8=Cấn, 2=Khôn).

2. **Castle Gate (Thành Môn Quyết) Adjacency Miscalculation**:
   - *Observation*: `left_p = (facing_palace_id % 9) + 1` uses decimal index modulo instead of circular spatial compass adjacency.
   - *Spatial Reality*: On the 8-directional Luopan, the ring order is `[1, 8, 3, 4, 9, 2, 7, 6]` (Khảm-Cấn-Chấn-Tốn-Ly-Khôn-Đoài-Càn).
   - *Deduction*: Adjacent palaces for index i in `CIRCLE_8` are `CIRCLE_8[(i-1)%8]` and `CIRCLE_8[(i+1)%8]`. For Ly (9), the neighbors are Tốn (4) and Khôn (2). Modulo 9 indexing erroneously paired South (9) with North (1).

3. **FTS5 Unhandled Special Characters**:
   - *Observation*: FTS5 virtual tables interpret `&`, `*`, `OR`, `NOT`, `"`, `-` as query syntax tokens.
   - *Deduction*: When search strings contain punctuation or raw user input, unescaped queries trigger syntax errors that crash the API. Queries must escape tokens or remove non-alphanumeric punctuation.

---

## 3. Caveats

- Areas audited:
  - Bát Tự Hà Lạc (Heaven/Earth numbers, Base 25/30, Ký cung 5, 100-year timeline).
  - Kỳ Môn Độn Giáp (18 Dun Ju, 24 Solar Terms, 3 Yuan, Central Palace 5 lodging, Strategic matrix).
  - Huyền Không Vận 9 (360° sweep, 24 Mountains, Base/Mountain/Facing flying stars, Special formations, Castle gate).
  - Trạch Cát Tung Shing (12 Officers, 28 Mansions, Luc Dieu, 12 Deities).
  - Đan Đạo Dưỡng Sinh (12 Tidal Hexagrams, 12 Zi-Wu meridians, Luc Tu Quyet, Dan Hoa Quy Nguyen).
  - Epistemological Triangulation (3-tier hierarchy, FTS5 canon & rule queries, consensus scoring).
- High-volume stress testing (10,000+ vector Monte Carlo) is handled by `challenger_1` / `tools/multi_century_stress_test.py`.

---

## 4. Conclusion

- **Overall Assessment**: The mathematical frameworks across the 6 disciplines are 90%+ robust, fast (<2ms execution), and comprehensively designed. However, **2 canonical logic defects** and **1 database query exception** prevent immediate production signoff:
  1. `engine/ha_lac_engine.py`: Fix Palace 5 Lạc Thư mapping (`single = 8 if is_heaven else 2` for Yang Male/Yin Female; `single = 2 if is_heaven else 8` for Yin Male/Yang Female).
  2. `engine/feng_shui.py`: Fix Castle Gate adjacent palace lookup using `CIRCLE_8` index neighbors instead of `(facing_palace_id % 9) + 1`.
  3. `engine/tuvi_rule_extractor.py` & `engine/classical_canon_rag.py`: Sanitize FTS5 query input strings by removing or escaping special operators (`&`, `*`, quotes).
  4. Fix 20 failing unit/integration tests in `tests/` to align schemas and assert contracts cleanly.

---

## 5. Verification Method

To independently verify all findings and test fixes:

1. **Run Challenger Edge-Case Suite**:
```bash
python tools/challenger_edge_case_runner.py
```
*Expected pass condition*: All 6 disciplines report `[PASS]`, with 0 `[FAIL]` and 0 `[OBSERVED_DEFECT]`.

2. **Run Full Pytest Suite**:
```bash
pytest -q
```
*Expected pass condition*: `208 passed, 0 failed`.
"""

with open(r".agents/challenger_2/handoff.md", "w", encoding="utf-8") as f:
    f.write(content)
print("handoff.md written successfully.")
