# Project: East Asian Metaphysical Suite All-In-One (Production Grade)

## Architecture
- **Metaphysical Domain Engines**:
  - `engine/ha_lac_engine.py`: Bát Tự Hà Lạc (Tiên/Hậu Thiên, Nguyên Khí, Hóa Công, 100 năm biến hào)
  - `engine/ky_mon_engine.py` & `engine/ky_mon_strategic.py`: Kỳ Môn Độn Giáp (18 Cục Âm Dương, 24 Tiết Khí, Cửu Cung, Cửu Tinh, Bát Môn, Bát Thần, Tam Kỳ Lục Nghi, Cát Hung cách cục)
  - `engine/feng_shui.py`: Huyền Không Phi Tinh Vận 9 (24 Sơn Hướng, Tam Nguyên Long Âm Dương phi tinh thuận nghịch, Thành Môn Quyết, Phản Ngâm Phục Ngâm, Hóa giải 5/2)
  - `engine/timing_almanac.py`: Trạch Cát Tung Shing (12 Trực Kiến Trừ, 28 Tú, Lục Diệu, Hoàng Đạo/Hắc Đạo)
  - `engine/dan_dao_health.py`: Đan Đạo Dưỡng Sinh & Đông Y Tạng Phủ (12 Tịch Quái Tham Đồng Khế, Tý Ngọ Lưu Chú, Lục Tự Quyết, Dẫn Hỏa Quy Nguyên)
  - `engine/annual_forecast.py`: Dự Báo Lưu Niên 12 Tháng (6 Hào biến hóa, Lưu Thái Tuế, Lưu Tứ Hóa, Bát Tự Hà Lạc, Kỳ Môn)
  - `engine/tu_vi_advanced.py`: Tử Vi Đẩu Số 110+ sao, 12 Cung Phi Tinh, Tứ Hóa, Hướng Tâm
- **Canonical Databases & Truth Arbitration**:
  - `data/canon_index.db`: SQLite FTS5 Index 140+ Cổ Thư Toàn Văn
  - `data/tuvi_canonical_rules.db`: 6,285+ Quy Tắc Kinh Điển Danh Gia
  - `data/case_tracker.db`: Case Tracker lưu vết chiêm nghiệm & lịch sử tự tiến hóa
  - `engine/triangulation_arbitrator.py`: Hệ thống Trọng tài Chân lý 3 Tầng (Tier 1 Cổ Thư > Tier 2 Master Rules > Tier 3 Engine Nội bộ)
- **Adversarial Auditor & Self-Evolution**:
  - `engine/adversarial_auditor.py`: Chuyên gia Trọng tài Cực kỳ Khó tính (Adversarial Judge), Săn lùng Edge Cases, Phản tư Metacognitive Delta-Gap, `/learn` Protocol
  - `tools/ziwei_regression_generator.py` & `engine/auto_test_generator.py`: Tự động sinh test case hồi quy khi phát hiện sai lệch
- **Stress-Testing & Verification Pipeline**:
  - `tools/ziwei_vector_generator.py` & `tools/multi_century_stress_test.py`: Pipeline Kiểm thử Tải cao 1900-2100 qua cả 7 bộ môn, Zero-Crash, Zero-Diff
- **Interfaces & Delivery**:
  - `cli.py` & `engine/cli.py`: Production CLI đầy đủ cờ lệnh (`--ha-lac`, `--ky-mon`, `--feng-shui`, `--dan-dao`, `--annual`, `--triangulate`, `--tu-vi`, `--stress-test`, `--benchmark`)
  - `agent_facade.py` & `engine/agent_facade.py`: Unified Facade xuất JSON chuẩn 2.2.0-agent
  - `mcp_server.py`: Fast JSON-RPC MCP Server đóng gói toàn bộ tools
  - `install_to_agent.py`: Đồng bộ mã nguồn, skills, rules lên agent và kho lưu trữ

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Bát Tự Hà Lạc Engine | Can Chi $\to$ Thiên/Địa số, Base 25/30, Ký cung 5 (Cấn/Khôn), Tiên/Hậu Thiên, Nguyên Khí, Hóa Công, 100 năm biến hào | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Kỳ Môn Độn Giáp Engine | 18 Cục Âm Dương Độn, 24 Tiết Khí Tam Nguyên, Bát Môn, Cửu Tinh, Bát Thần, Tam Kỳ Lục Nghi, Cát Hung Cách Cục | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Huyền Không Phi Tinh Vận 9 | 24 Sơn Hướng, Tam Nguyên Long Âm Dương phi tinh thuận nghịch, Thành Môn Quyết, Phản Ngâm Phục Ngâm, Hóa giải Ngũ Hoàng/Nhị Hắc | M1 | ORIGINAL_REQUEST §R1 |
| 4 | Trạch Cát Tung Shing | 12 Trực Kiến Trừ, 28 Tú, Lục Diệu, 12 Thần Hoàng Đạo / Hắc Đạo | M1 | ORIGINAL_REQUEST §R1 |
| 5 | Đan Đạo Dưỡng Sinh | Chu Dịch Tham Đồng Khế (12 Tịch Quái), Hoàng Đế Nội Kinh, Tý Ngọ Lưu Chú, Lục Tự Quyết, Dẫn Hỏa Quy Nguyên | M1 | ORIGINAL_REQUEST §R1 |
| 6 | Dự Báo Lưu Niên 12 Tháng | 6 Hào phân kỳ 12 tháng, Lưu Thái Tuế & Lưu Tứ Hóa, Bát Tự Hà Lạc, Kỳ Môn Độn Giáp | M1 | ORIGINAL_REQUEST §R1 |
| 7 | Canonical Database Integration | Tích hợp liên thông SQLite FTS5 140+ cổ thư (`data/canon_index.db`) & 6,285+ quy tắc (`data/tuvi_canonical_rules.db`) | M1 | ORIGINAL_REQUEST §R1 |
| 8 | Adversarial Judge Sub-Agent | Săn tìm edge-cases (tháng nhuận, Dạ Tý 23h-00h, Vận 9 transition, hung sát) không thỏa hiệp | M2 | ORIGINAL_REQUEST §R2 |
| 9 | Metacognitive Delta-Gap Analysis | Tự động phản tư, phân tích Delta-Gap và kích hoạt `/learn` khi phát hiện sai số | M2 | ORIGINAL_REQUEST §R2 |
| 10 | 3-Tier Truth Arbitration | Trọng tài chân lý 3 tầng (Tier 1 Cổ Thư > Tier 2 Master Rules > Tier 3 Engine Nội Bộ) + Consensus Scoring | M2 | ORIGINAL_REQUEST §R2 |
| 11 | Continuous Scaffolding Case Tracker | Ghi nhận chiêm nghiệm và lịch sử phản tư vào `data/case_tracker.db` | M2 | ORIGINAL_REQUEST §R2 |
| 12 | Multi-Century Random Stress-Test | Pipeline sinh ngẫu nhiên hàng ngàn vector kiểm chuẩn 1900–2100 cho cả 7 bộ môn | M3 | ORIGINAL_REQUEST §R3 |
| 13 | High-Speed Latency Optimization | Đảm bảo tốc độ phản hồi < 2ms/truy vấn qua LRU caching và tối ưu hóa ephemeris | M3 | ORIGINAL_REQUEST §R3 |
| 14 | Zero-Crash & Zero-Diff Validation | Cơ chế xác thực zero-diff và tự động sinh test case hồi quy | M3 | ORIGINAL_REQUEST §R3 |
| 15 | Production CLI | CLI hỗ trợ đầy đủ `--ha-lac`, `--ky-mon`, `--feng-shui`, `--dan-dao`, `--annual`, `--triangulate`, `--benchmark` | M4 | ORIGINAL_REQUEST §R4 |
| 16 | Unified Agent Facade | Schema `2.2.0-agent` xuất JSON chuẩn hóa cho AI Agent | M4 | ORIGINAL_REQUEST §R4 |
| 17 | MCP Server Delivery | Đóng gói đầy đủ tools (9+ tools) cho toàn bộ hệ sinh thái | M4 | ORIGINAL_REQUEST §R4 |
| 18 | Rule 24 & 25 Technical Metadata | Xuất bảng Markdown Metadata 100% (Thời gian kép, Tứ Trụ, Thần Sát, Tinh Bàn) | M4 | ORIGINAL_REQUEST §R4 |
| 19 | Multi-Target Synchronization | Đồng bộ mã nguồn, skills, rules sang Agent Skills directory và kho tri thức | M4 | ORIGINAL_REQUEST §R4 |
| 20 | E2E Testing Suite (Tiers 1-4) & Adversarial Hardening (Tier 5) | Bộ test suite `pytest` đạt PASS 100% (>120+ tests) và vượt qua kiểm thử đối kháng | Final Milestone | ORIGINAL_REQUEST §Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Full-Spectrum Metaphysical Domain Engines & Databases (R1) | Complete & verify 7 engines + FTS5 canon database queries | none | DONE |
| M2 | Adversarial Ultra-Critical Auditor & Epistemological Triangulation (R2) | Implement Adversarial Judge, Delta-Gap, `/learn`, 3-Tier Arbitration, Case Tracker | M1 | DONE |
| M3 | Multi-Century Random Stress-Testing & Self-Scaffolding (R3) | 1900-2100 vector stress tests, latency optimization (<2ms), zero-diff validation | M1, M2 | DONE |
| M4 | Production CLI, Unified Facade & MCP Server Delivery (R4) | CLI flags, Facade JSON schema, MCP server, Rule 24/25 Metadata, multi-target sync | M1, M2, M3 | DONE |
| Final | E2E Testing Pass (Tiers 1-4) & Adversarial Hardening (Tier 5) + Forensic Audit | 100% pytest pass (>120+ tests), Adversarial challenges, Forensic Audit CLEAN | M1, M2, M3, M4 | DONE |

## Interface Contracts
### `engine/ha_lac_engine.py`
- `calculate_ha_lac(dt: datetime, gender: int = 1) -> Dict[str, Any]`
- Returns: `{"thien_so": int, "dia_so": int, "tien_thien_hexagram": Dict, "hau_thien_hexagram": Dict, "nguyen_khi_hao": int, "hoa_cong_hao": int, "dai_van_timeline": List[Dict], "metadata": Dict}`

### `engine/ky_mon_engine.py` & `engine/ky_mon_strategic.py`
- `calculate_ky_mon_chart(dt: datetime) -> Dict[str, Any]`
- Returns: `{"cuc_so": int, "don_type": "Duong"|"Am", "tiet_khi": str, "truc_phu": Dict, "truc_su": Dict, "palaces": Dict[int, Dict], "auspicious_patterns": List[str], "inauspicious_patterns": List[str], "metadata": Dict}`

### `engine/feng_shui.py`
- `calculate_flying_stars_period9(facing_degree: float, birth_year: int = 1990) -> Dict[str, Any]`
- Returns: `{"period": 9, "mountain_name": str, "facing_name": str, "base_stars": Dict, "mountain_stars": Dict, "facing_stars": Dict, "special_formations": List[str], "five_yellow_remedy": str, "two_black_remedy": str, "metadata": Dict}`

### `engine/timing_almanac.py`
- `calculate_timing_almanac(dt: datetime) -> Dict[str, Any]`
- Returns: `{"truc_12": str, "tu_28": str, "luc_dieu": str, "hoang_dao_than": str, "is_hoang_dao": bool, "auspicious_activities": List[str], "taboo_activities": List[str]}`

### `engine/dan_dao_health.py`
- `calculate_dan_dao_health(dt: datetime) -> Dict[str, Any]`
- Returns: `{"tich_quai": str, "tiet_khi": str, "ty_ngo_luu_chu": Dict, "luc_tu_quyet": str, "dan_hoa_quy_nguyen": Dict, "organ_diagnosis": Dict}`

### `engine/annual_forecast.py`
- `calculate_annual_forecast(birth_dt: datetime, target_year: int, question: str = "") -> Dict[str, Any]`
- Returns: `{"target_year": int, "lunar_year_can_chi": str, "thai_tue_palace": str, "luu_tu_hoa": Dict, "six_lines_forecast": List[Dict], "qimen_annual_guidance": Dict}`

### `engine/triangulation_arbitrator.py`
- `arbitrate_epistemological_truth(dt: datetime, gender: int, question_topic: str) -> Dict[str, Any]`
- Returns: `{"tier1_canon_evidence": List[Dict], "tier2_master_rules": List[Dict], "tier3_engine_results": Dict, "consensus_score": float, "final_arbitration_verdict": str, "rule24_metadata_table": str}`

### `engine/adversarial_auditor.py`
- `audit_metaphysical_case(chart_data: Dict, expected_rules: List[str] = None) -> Dict[str, Any]`
- Returns: `{"audit_verdict": "PASS"|"FAIL", "delta_gap": Dict, "edge_case_triggers": List[str], "metacognitive_reflection": str, "learn_protocol_triggered": bool}`

## Code Layout
- `engine/`: Core metaphysical calculation modules, arbitrator, auditor, facade, CLI
- `data/`: `canon_index.db` (FTS5 140+ books), `tuvi_canonical_rules.db` (6,285+ rules), `case_tracker.db`
- `tools/`: Vector generators, stress-testing harnesses, regression generators, sync scripts
- `tests/`: Comprehensive E2E and unit test suites across all 7 disciplines
- Root: `cli.py`, `agent_facade.py`, `mcp_server.py`, `SKILL.md`, `tool_definitions.json`, `install_to_agent.py`
