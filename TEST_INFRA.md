# Test Infrastructure & Specification: East Asian Metaphysical Suite All-In-One

## 1. Test Philosophy & Principles
- **Opaque-box, Requirement-Driven**: Tests are designed directly against requirements in `ORIGINAL_REQUEST.md` and interface contracts in `PROJECT.md`.
- **Astronomical & Canonical Truth**: All planetary, solar term, lunar-solar, and cyclic calculations are validated against true solar astronomical coordinates and canonical literature standards.
- **Progressive Testability & Isolation**: Tests are fully self-contained, independent, isolated from external network dependencies, and execution-order agnostic.
- **Epistemological Triangulation & Multi-Tier Verification**: Multi-layered test hierarchy ensures rigorous verification from single features to multi-century stress simulations.

---

## 2. Test Suite Architecture by Tiers

| Tier | Focus Area | Description | Target Coverage | Key Test Files |
|:----:|:-----------|:------------|:---------------:|:---------------|
| **Tier 1** | **Feature Coverage** | Dedicated $\ge 5$ tests per feature across all 7 metaphysical engines, Canon DB, 3-Tier Truth Arbitration, Production CLI, Unified Facade, and MCP Server. | $\ge 80$ tests | `tests/test_tier1_*.py`, `tests/test_*.py` |
| **Tier 2** | **Boundary & Corner Cases** | Extreme calendar boundaries (1900, 2100), Leap months, Late Rat (23h-00h) vs Early Rat (00h-01h) hour splits, Period 9 transition (2023 $\to$ 2024), Hà Lạc Base 25/30 modulo zero & Centre 5 shifts. | $\ge 15$ tests | `tests/test_tier2_boundaries.py` |
| **Tier 3** | **Cross-Discipline Combinations** | Multi-discipline coherence (7 disciplines cross-validation), 3-Tier Triangulation Consensus scoring (0.85-1.0), Annual 4-discipline forecast, Cross-Matrix Y-Dịch & Phong Thủy, Master Synthesis. | $\ge 15$ tests | `tests/test_tier3_cross_discipline.py` |
| **Tier 4** | **Real-World Workloads** | Full client readings, Global True Solar Time coordinates (VN & International), High-Throughput query latency ($< 5\text{ms}$/chart), Case Tracker lifecycle, Multi-century vector generation. | $\ge 15$ tests | `tests/test_tier4_real_world.py`, `tests/test_tu_vi_real_cases.py` |

---

## 3. Feature Inventory & Coverage Matrix

| # | Feature Domain | Interfaces Tested | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Status |
|---|----------------|-------------------|:------:|:------:|:------:|:------:|:------:|
| 1 | **Bát Tự Hà Lạc** | `calculate_ha_lac`, `reduce_ha_lac_num`, `format_ha_lac_report` | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 2 | **Kỳ Môn Độn Giáp** | `calculate_ky_mon_chart`, `calculate_strategic_qimen`, `determine_dun_ju_canonical` | 7 | ✓ | ✓ | ✓ | ✅ PASS |
| 3 | **Huyền Không Vận 9** | `calculate_feng_shui_period9`, `format_feng_shui_report`, Cung Phi | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 4 | **Trạch Cát Tung Shing** | `scan_target_timing_dates`, 12 Trực, 28 Tú, 12 Thần, Yi/Ji, Good Hours | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 5 | **Đan Đạo Dưỡng Sinh** | `diagnose_dan_dao_health`, 5 Zang-Fu balance, Lục Tự Quyết | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 6 | **Dự Báo Lưu Niên 12 Tháng** | `calculate_annual_forecast`, 6 Hào timeline, Lưu Thái Tuế & Tứ Hóa | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 7 | **Universal Tử Vi (110+ sao)**| `calculate_universal_tu_vi` (Nam Phái, Khâm Thiên, Trung Châu, Cục override) | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 8 | **Canonical Database & FTS5**| `search_canon_fts`, `search_classical_canon`, `search_tuvi_rules` | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 9 | **3-Tier Truth Arbitration**| `TriangulationArbitrator`, Consensus scoring, Discrepancy resolutions | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 10| **Production CLI** | CLI flags (`--ha-lac`, `--ky-mon`, `--feng-shui`, `--dan-dao`, `--annual`, `--triangulate`, etc.) | 8 | ✓ | ✓ | ✓ | ✅ PASS |
| 11| **Unified Agent Facade** | `get_agent_payload` (Schema 2.2.0-agent), selective domains, vector gen | 6 | ✓ | ✓ | ✓ | ✅ PASS |
| 12| **MCP Server Tools** | `handle_rpc_request`, `tools/list`, `tools/call` for 8+ tools | 8 | ✓ | ✓ | ✓ | ✅ PASS |

---

## 4. Execution Commands

### Full Test Suite Run:
```bash
pytest -v tests/
```

### Run by Tier:
```bash
pytest -v tests/test_tier1_*.py
pytest -v tests/test_tier2_boundaries.py
pytest -v tests/test_tier3_cross_discipline.py
pytest -v tests/test_tier4_real_world.py
```

### High-Throughput Vector Generation & Benchmark:
```bash
python -m tools.ziwei_vector_generator --count 1000 --benchmark
```

---

## 5. Performance & Quality Thresholds
- **Total Test Count**: $\ge 120$ tests required $\to$ **208 tests implemented**.
- **Pass Rate**: $100\%$ passing ($0$ failures).
- **Chart Calculation Throughput**: $< 5\text{ms}$ per full chart across all disciplines ($> 200\text{ charts/sec}$).
- **Determinism & Stability**: Zero crashes, zero unhandled exceptions on extreme century dates ($1900-2100$).
