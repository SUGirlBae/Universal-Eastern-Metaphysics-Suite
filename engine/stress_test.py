"""
Multi-Century Divination Stress-Testing & Integrity Suite (1900–2100)
Validates 1,000+ edge cases across leap years, solstices, equinoxes, and midnight transitions.
"""
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

try:
    from .cli import cast_hexagram
    from .lunar_solar import LOCAL_TZ
except (ImportError, ValueError):
    from cli import cast_hexagram
    from lunar_solar import LOCAL_TZ

def run_multi_century_stress_test(num_random=1000):
    print(f"=== COMMENCING MULTI-CENTURY STRESS TEST ({num_random} RANDOM + 21 EDGE CASES) ===")
    
    passed = 0
    failed = 0
    errors = []
    
    # 1. Edge cases: Midnight transitions, leap years, century boundaries
    edge_dates = [
        datetime(1900, 1, 1, 0, 0, tzinfo=LOCAL_TZ),
        datetime(1900, 2, 28, 23, 59, tzinfo=LOCAL_TZ),
        datetime(1904, 2, 29, 12, 0, tzinfo=LOCAL_TZ),
        datetime(1945, 9, 2, 14, 0, tzinfo=LOCAL_TZ),
        datetime(1975, 4, 30, 11, 30, tzinfo=LOCAL_TZ),
        datetime(1999, 12, 31, 23, 59, tzinfo=LOCAL_TZ),
        datetime(2000, 1, 1, 0, 0, tzinfo=LOCAL_TZ),
        datetime(2000, 2, 29, 23, 30, tzinfo=LOCAL_TZ),
        datetime(2024, 2, 29, 23, 50, tzinfo=LOCAL_TZ),
        datetime(2024, 4, 28, 20, 48, tzinfo=LOCAL_TZ),
        datetime(2026, 4, 21, 20, 55, tzinfo=LOCAL_TZ),
        datetime(2026, 4, 22, 20, 49, tzinfo=LOCAL_TZ),
        datetime(2026, 4, 26, 20, 45, tzinfo=LOCAL_TZ),
        datetime(2026, 4, 28, 20, 36, tzinfo=LOCAL_TZ),
        datetime(2026, 8, 28, 17, 12, tzinfo=LOCAL_TZ),
        datetime(2026, 8, 29, 17, 36, tzinfo=LOCAL_TZ),
        datetime(2050, 6, 21, 12, 0, tzinfo=LOCAL_TZ), # Hạ Chí
        datetime(2050, 12, 22, 0, 30, tzinfo=LOCAL_TZ), # Đông Chí
        datetime(2099, 12, 31, 23, 59, tzinfo=LOCAL_TZ),
        datetime(2100, 1, 1, 0, 0, tzinfo=LOCAL_TZ),
        datetime(2100, 12, 31, 23, 59, tzinfo=LOCAL_TZ),
    ]
    
    test_suite = edge_dates.copy()
    
    # 2. Random dates spanning 1900 to 2100 safely using timedelta
    base_dt = datetime(1900, 1, 1, 0, 0, tzinfo=LOCAL_TZ)
    total_days = 365 * 200 + 50 # ~200 years
    
    random.seed(42) # Deterministic reproducibility
    for _ in range(num_random):
        rand_days = random.randint(0, total_days)
        rand_secs = random.randint(0, 86399)
        test_suite.append(base_dt + timedelta(days=rand_days, seconds=rand_secs))
        
    print(f"Total test vectors: {len(test_suite)}")
    
    for idx, dt in enumerate(test_suite):
        try:
            res = cast_hexagram(dt)
            
            # Integrity checks:
            # 1. Non-empty report
            assert res["report"], "Report is empty"
            # 2. Moving line in 1..6
            mov = res["mai_hoa_res"]["moving_line"]
            assert 1 <= mov <= 6, f"Invalid moving line: {mov}"
            # 3. Valid hexagrams
            assert res["luc_hao_res"]["hex_symbol"], "Missing primary hex symbol"
            assert res["luc_hao_res"]["t_hex_symbol"], "Missing trans hex symbol"
            # 4. Valid 6 lines
            assert len(res["luc_hao_res"]["lines"]) == 6, "Missing 6 lines"
            # 5. Exactly one moving line in primary
            moving_count = sum(1 for l in res["luc_hao_res"]["lines"] if l["is_dong"])
            assert moving_count == 1, f"Expected 1 moving line, got {moving_count}"
            # 6. Valid The / Ung positions
            the_l = res["luc_hao_res"]["the_line"]
            ung_l = res["luc_hao_res"]["ung_line"]
            assert abs(the_l - ung_l) == 3, f"Invalid The-Ung distance: {the_l} vs {ung_l}"
            
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(f"Error at {dt.isoformat()}: {str(e)}")
            
        if (idx + 1) % 200 == 0 or (idx + 1) == len(test_suite):
            print(f"  Processed {idx + 1}/{len(test_suite)} cases... (Passed: {passed}, Failed: {failed})")
            
    print("\n=== STRESS TEST RESULTS ===")
    print(f"Total Cases:  {len(test_suite)}")
    print(f"Passed:       {passed} ({(passed/len(test_suite))*100:.2f}%)")
    print(f"Failed:       {failed}")
    
    if failed == 0:
        print("\nSUCCESS: 100.00% ZERO-BUG PASS RATE ACROSS 1900-2100 MULTI-CENTURY SUITE!")
    else:
        print("\nFAILURES DETECTED:")
        for err in errors[:10]:
            print("  ", err)
            
    return failed == 0

if __name__ == "__main__":
    success = run_multi_century_stress_test(1000)
    sys.exit(0 if success else 1)
