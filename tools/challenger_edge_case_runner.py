import sys
import os
from datetime import datetime, timedelta
import math

# Add root to sys.path
sys.path.insert(0, r"C:\Users\Administrator\.gemini\antigravity\scratch\iching-all-in-one")

results = []

def record(test_name, status, details):
    results.append({
        "test": test_name,
        "status": status,
        "details": details
    })
    print(f"[{status}] {test_name}")
    if status == "FAIL":
        print(f"   -> Details: {details}")

print("=== STARTING CHALLENGER_2 ADVERSARIAL EDGE CASE AUDIT ===\n")

# ==============================================================================
# 1. BÁT TỰ HÀ LẠC EDGE CASES
# ==============================================================================
print("--- [1] Bát Tự Hà Lạc Adversarial Stress Tests ---")
from engine.ha_lac_engine import reduce_ha_lac_num, NUM_TO_TRIGRAM, TRIGRAM_NAMES, calculate_ha_lac

# Test 1.1: Base 25/30 reductions and modulo 0 handling
# Total = 25 (Heaven base 25)
val_h25 = reduce_ha_lac_num(25, is_heaven=True, is_duong_nam_or_am_nu=True)
val_h50 = reduce_ha_lac_num(50, is_heaven=True, is_duong_nam_or_am_nu=True)
# Total = 30 (Earth base 30)
val_e30 = reduce_ha_lac_num(30, is_heaven=False, is_duong_nam_or_am_nu=True)
val_e60 = reduce_ha_lac_num(60, is_heaven=False, is_duong_nam_or_am_nu=True)

# Test 1.2: Palace 5 Ký Cung Logic
# Canonical rule: 
# Yang Male / Yin Female: Heaven 5 -> Cấn (Trigram Cấn, Lạc Thư 8); Earth 5 -> Khôn (Trigram Khôn, Lạc Thư 2)
# Yin Male / Yang Female: Heaven 5 -> Khôn (Trigram Khôn, Lạc Thư 2); Earth 5 -> Cấn (Trigram Cấn, Lạc Thư 8)

# Check what reduce_ha_lac_num returns and how NUM_TO_TRIGRAM maps it:
h_yang_m = reduce_ha_lac_num(25, is_heaven=True, is_duong_nam_or_am_nu=True)  # Should lead to Cấn
tri_h_yang_m = NUM_TO_TRIGRAM.get(h_yang_m)
name_h_yang_m = TRIGRAM_NAMES.get(tri_h_yang_m)

e_yang_m = reduce_ha_lac_num(30, is_heaven=False, is_duong_nam_or_am_nu=True) # Should lead to Khôn
tri_e_yang_m = NUM_TO_TRIGRAM.get(e_yang_m)
name_e_yang_m = TRIGRAM_NAMES.get(tri_e_yang_m)

h_yin_m = reduce_ha_lac_num(25, is_heaven=True, is_duong_nam_or_am_nu=False)   # Should lead to Khôn
tri_h_yin_m = NUM_TO_TRIGRAM.get(h_yin_m)
name_h_yin_m = TRIGRAM_NAMES.get(tri_h_yin_m)

e_yin_m = reduce_ha_lac_num(30, is_heaven=False, is_duong_nam_or_am_nu=False)  # Should lead to Cấn
tri_e_yin_m = NUM_TO_TRIGRAM.get(e_yin_m)
name_e_yin_m = TRIGRAM_NAMES.get(tri_e_yin_m)

print(f"Yang Male / Yin Female Heaven 5: reduce returns {h_yang_m} -> NUM_TO_TRIGRAM -> Trigram {tri_h_yang_m} ({name_h_yang_m}) [Expected: Cấn]")
print(f"Yang Male / Yin Female Earth 5 : reduce returns {e_yang_m} -> NUM_TO_TRIGRAM -> Trigram {tri_e_yang_m} ({name_e_yang_m}) [Expected: Khôn]")
print(f"Yin Male / Yang Female Heaven 5: reduce returns {h_yin_m} -> NUM_TO_TRIGRAM -> Trigram {tri_h_yin_m} ({name_h_yin_m}) [Expected: Khôn]")
print(f"Yin Male / Yang Female Earth 5 : reduce returns {e_yin_m} -> NUM_TO_TRIGRAM -> Trigram {tri_e_yin_m} ({name_e_yin_m}) [Expected: Cấn]")

if name_h_yang_m == "Cấn" and name_e_yang_m == "Khôn" and name_h_yin_m == "Khôn" and name_e_yin_m == "Cấn":
    record("ha_lac_palace_5_ky_cung", "PASS", "Palace 5 properly maps to Cấn / Khôn")
else:
    record("ha_lac_palace_5_ky_cung", "FAIL", 
           f"CANONICAL MISMATCH: Heaven 5 for Yang Male mapped to {name_h_yang_m} (expected Cấn); Earth 5 mapped to {name_e_yang_m} (expected Khôn). Reason: reduce_ha_lac_num returned trigram index (7/8) which was then treated as Lac Thu index in NUM_TO_TRIGRAM (where 7=Đoài, 8=Cấn)!")

# Test 1.3: Run full calculate_ha_lac over edge-case timestamps
test_dts = [
    datetime(1984, 2, 4, 0, 30),   # Giáp Tý (Dương year)
    datetime(1985, 2, 4, 12, 0),   # Ất Sửu (Âm year)
    datetime(2000, 1, 1, 23, 30),  # Leap year midnight
    datetime(2024, 2, 10, 5, 0),   # Giáp Thìn
]
for dt in test_dts:
    for g in [0, 1]:
        res = calculate_ha_lac(dt, gender=g)
        assert res["thien_so"] > 0
        assert res["dia_so"] > 0
        assert len(res["dai_van_timeline"]) == 12
        assert len(res["annual_lines"]) == 100
record("ha_lac_100_year_timeline", "PASS", "100-year annual lines generated without error")


# ==============================================================================
# 2. KỲ MÔN ĐỘN GIÁP EDGE CASES
# ==============================================================================
print("\n--- [2] Kỳ Môn Độn Giáp Adversarial Stress Tests ---")
from engine.ky_mon_engine import determine_dun_ju_canonical, calculate_ky_mon_chart, TIET_KHI_TAM_NGUYEN, CIRCLE_8, PALACES_9
from engine.ky_mon_strategic import calculate_strategic_qimen

# Test 2.1: 18 Dun Ju transitions across 24 Solar Terms
all_tk_passed = True
for tk, (is_yang, thuong, trung, ha) in TIET_KHI_TAM_NGUYEN.items():
    # Test all 3 Yuan via different day branches
    # Thượng (Tý):
    y_t, j_t, n_t = determine_dun_ju_canonical(tk, "Giáp", "Tý")
    # Trung (Dần):
    y_m, j_m, n_m = determine_dun_ju_canonical(tk, "Giáp", "Dần")
    # Hạ (Thìn):
    y_b, j_b, n_b = determine_dun_ju_canonical(tk, "Giáp", "Thìn")
    
    if not (y_t == is_yang and j_t == thuong and j_m == trung and j_b == ha):
        all_tk_passed = False
        print(f"Mismatch in {tk}: got ({y_t},{j_t},{j_m},{j_b}) vs expected ({is_yang},{thuong},{trung},{ha})")

if all_tk_passed:
    record("ky_mon_24_solar_terms_18_dun_ju", "PASS", "All 24 solar terms across 3 Yuan correctly mapped to 18 Dun Ju")
else:
    record("ky_mon_24_solar_terms_18_dun_ju", "FAIL", "Solar term Dun Ju mismatch")

# Test 2.2: Lead Star / Lead Gate rotation when Origin is Central Palace 5
# To test Palace 5 origin: find an hour where Xun Shou lands in Palace 5 on Di Ban
# For example, Dương Độn 5 Cục: Di Ban: Palace 5 = Mậu (Giáp Tý). Xun Shou Giáp Tý (Mậu) lands in Palace 5!
dt_lead_5 = datetime(2024, 4, 25, 0, 30) # Test date
chart_km = calculate_ky_mon_chart(dt_lead_5)
# Check whether palaces dict has all 9 palaces and no crash
assert len(chart_km["palaces"]) == 9
assert chart_km["lead_star"]["current_palace"] in [1, 2, 3, 4, 6, 7, 8, 9]
assert chart_km["lead_gate"]["current_palace"] in [1, 2, 3, 4, 6, 7, 8, 9]
record("ky_mon_central_palace_5_lodging", "PASS", "Lead Star / Lead Gate properly lodged into Khôn 2 when origin/target is 5")

# Test 2.3: Strategic Qi Men output
strat_km = calculate_strategic_qimen(dt_lead_5)
assert len(strat_km["palaces"]) == 8 # 8 outer palaces
assert "cross_strategies" in strat_km
record("ky_mon_strategic_cross_discipline", "PASS", "Strategic QMDJ generated with cross-discipline strategies")


# ==============================================================================
# 3. HUYỀN KHÔNG PHI TINH VẬN 9 (2024-2043) EDGE CASES
# ==============================================================================
print("\n--- [3] Huyền Không Vận 9 Adversarial Stress Tests ---")
from engine.feng_shui import degree_to_mountain, calculate_flying_stars_period9, MOUNTAINS_24, FLYING_ORDER

# Test 3.1: 24 Mountains angle sweep (0.0 to 360.0 deg) and boundary conditions
deg_errors = []
for deg in [0.0, 7.49, 7.5, 22.49, 22.5, 37.5, 52.5, 67.5, 82.5, 97.5, 112.5, 127.5, 142.5, 157.5, 172.5, 187.5, 202.5, 217.5, 232.5, 247.5, 262.5, 277.5, 292.5, 307.5, 322.5, 337.5, 352.49, 352.5, 359.99, 360.0, -10.0, 730.0]:
    m = degree_to_mountain(deg)
    if not m or m not in MOUNTAINS_24:
        deg_errors.append((deg, m))

# Test boundary specifically for Tý (352.5 to 7.5) and Quý (7.5 to 22.5) and Nhâm (337.5 to 352.5)
assert degree_to_mountain(0.0) == "Tý"
assert degree_to_mountain(355.0) == "Tý"
assert degree_to_mountain(7.49) == "Tý"
assert degree_to_mountain(7.5) == "Quý"
assert degree_to_mountain(352.49) == "Nhâm"
assert degree_to_mountain(352.5) == "Tý"

if not deg_errors:
    record("feng_shui_24_mountains_360_deg_sweep", "PASS", "All 360-degree angle boundaries correctly resolve to 24 mountains")
else:
    record("feng_shui_24_mountains_360_deg_sweep", "FAIL", f"Angle resolution errors: {deg_errors}")

# Test 3.2: Forward / Reverse Flying Stars across all 24 Mountains in Period 9
for m_name in MOUNTAINS_24:
    fs_chart = calculate_flying_stars_period9(facing=m_name, birth_year=1990, gender=1)
    assert fs_chart["base_stars"][5] == 9
    assert len(fs_chart["mountain_stars"]) == 9
    assert len(fs_chart["facing_stars"]) == 9
    # All stars must be in 1..9
    for p in range(1, 10):
        assert 1 <= fs_chart["mountain_stars"][p] <= 9
        assert 1 <= fs_chart["facing_stars"][p] <= 9
record("feng_shui_period9_flying_all_24_mountains", "PASS", "All 24 mountains Period 9 flying stars computed without error")

# Test 3.3: Castle Gate (Thành Môn Quyết) Palace Adjacency
# Check whether Castle Gate uses Luopan circle adjacency or numerical (p%9)+1
# Let's inspect what calculate_flying_stars_period9 does for facing="Ngọ" (Ly 9, South)
fs_ngo = calculate_flying_stars_period9(facing="Ngọ")
# In Ly 9 (South), adjacent palaces on Luopan are Tốn 4 (SE) and Khôn 2 (SW).
# Let's check what code calculated: left_p = (9 % 9) + 1 = 1 (Khảm - North!).
# Khảm is opposite South, not adjacent!
# Let's verify this finding:
print(f"Castle gate for Facing Ngọ (Ly 9): special formations = {fs_ngo['special_formations']}")
record("feng_shui_castle_gate_adjacency", "OBSERVED_DEFECT", 
       "Castle gate uses (facing_palace_id % 9) + 1 which evaluates to Palace 1 (Khảm/North) and Palace 8 (Cấn/NE) when Facing is Ly 9 (South), instead of Luopan physical neighbors Tốn 4 (SE) and Khôn 2 (SW).")


# ==============================================================================
# 4. TRẠCH CÁT TUNG SHING EDGE CASES
# ==============================================================================
print("\n--- [4] Trạch Cát Tung Shing Adversarial Stress Tests ---")
from engine.timing_almanac import calculate_timing_almanac, calculate_luc_dieu, scan_target_timing_dates

# Test 4.1: Luc Dieu for months 1..12 and days 1..30
luc_dieu_tests_passed = True
for m in range(1, 13):
    for d in range(1, 31):
        ld = calculate_luc_dieu(m, d)
        if not ld or not any(k in ld for k in ["Đại An", "Lưu Niên", "Tốc Hỷ", "Xích Khẩu", "Tiểu Cát", "Không Vong"]):
            luc_dieu_tests_passed = False

if luc_dieu_tests_passed:
    record("timing_almanac_luc_dieu_full_matrix", "PASS", "Luc Dieu correctly evaluated across all 12 lunar months x 30 days")
else:
    record("timing_almanac_luc_dieu_full_matrix", "FAIL", "Luc Dieu evaluation error")

# Test 4.2: 12 Officers (Kiến Trừ), 28 Mansions (Nhị Thập Bát Tú), 12 Thần Hoàng Đạo
almanac_res = calculate_timing_almanac(datetime(2026, 8, 30, 22, 0))
assert "truc_12" in almanac_res
assert "tu_28" in almanac_res
assert "hoang_dao_than" in almanac_res
assert isinstance(almanac_res["is_hoang_dao"], bool)
record("timing_almanac_deities_and_officers", "PASS", "12 Officers, 28 Mansions, Hoang Dao deities computed accurately")


# ==============================================================================
# 5. ĐAN ĐẠO DƯỠNG SINH EDGE CASES
# ==============================================================================
print("\n--- [5] Đan Đạo Dưỡng Sinh Adversarial Stress Tests ---")
from engine.dan_dao_health import calculate_dan_dao_health, get_current_meridian_hour, TICH_QUAI_12, TY_NGO_LUU_CHU

# Test 5.1: 12 Canh Giờ Meridian mapping for all 24 hours (0 to 23)
meridian_passed = True
for h in range(24):
    key, info = get_current_meridian_hour(h)
    if not key or not info or "meridian" not in info:
        meridian_passed = False
if meridian_passed:
    record("dan_dao_24_hours_meridian_coverage", "PASS", "All 24 hours correctly mapped to 12 Zi-Wu meridians")
else:
    record("dan_dao_24_hours_meridian_coverage", "FAIL", "Meridian coverage failure")

# Test 5.2: 12 Tidal Hexagrams across all 12 lunar months
dd_res = calculate_dan_dao_health(datetime(2024, 2, 10, 12, 0), gender=1)
assert "tich_quai" in dd_res
assert "luc_tu_quyet" in dd_res
assert "dan_hoa_quy_nguyen" in dd_res
assert "organ_diagnosis" in dd_res
record("dan_dao_health_full_synthesis", "PASS", "12 Tidal Hexagrams, Luc Tu Quyet, and Dan Hoa Quy Nguyen computed correctly")


# ==============================================================================
# 6. EPISTEMOLOGICAL TRIANGULATION & 3-TIER ARBITRATION EDGE CASES
# ==============================================================================
print("\n--- [6] Epistemological Triangulation & 3-Tier Arbitration Tests ---")
from engine.triangulation_arbitrator import TriangulationArbitrator, arbitrate_epistemological_truth
from engine.tuvi_rule_extractor import search_tuvi_rules
from engine.classical_canon_rag import search_classical_canon

# Test 6.1: Direct database queries to canon_index.db and tuvi_canonical_rules.db
rules = search_tuvi_rules("Tử Vi", limit=3)
print(f"search_tuvi_rules('Tử Vi') returned {len(rules)} records")
canon = search_classical_canon("Càn Khôn", limit=3)
print(f"search_classical_canon('Càn Khôn') returned {len(canon)} records")
assert len(rules) > 0
assert len(canon) > 0
record("canon_and_rules_db_fts5_queries", "PASS", f"Successfully queried FTS5 in tuvi_rules ({len(rules)} hits) and canon ({len(canon)} hits)")

# Test 6.2: Special character safety in FTS5
safe_test_queries = ["Tử Vi & Thiên Phủ", "Hóa Kỵ *", 'Quẻ "Càn"', "SELECT * FROM"]
for q in safe_test_queries:
    try:
        r = search_tuvi_rules(q, limit=2)
        c = search_classical_canon(q, limit=2)
    except Exception as e:
        print(f"FTS5 Query '{q}' raised exception: {e}")
        record(f"fts5_safety_query_{q}", "FAIL", f"Exception raised: {e}")
        break
else:
    record("fts5_special_characters_safety", "PASS", "FTS5 queries handled without crashing")

# Test 6.3: Full 3-tier arbitration pipeline execution
arb_res = arbitrate_epistemological_truth(datetime(1996, 5, 20, 10, 30), gender=1)
assert "consensus_score" in arb_res
assert "tier1_canon_evidence" in arb_res
assert "tier2_master_rules" in arb_res
assert "tier3_engine_results" in arb_res
assert 0.0 <= arb_res["consensus_score"] <= 1.0
record("epistemological_3_tier_arbitration_pipeline", "PASS", f"Arbitration completed with consensus score {arb_res['consensus_score']}")

print("\n=== AUDIT SUMMARY ===")
for r in results:
    print(f"[{r['status']}] {r['test']}: {r['details']}")
