"""
Unit and Integration Test Suite for Multi-Century Vector Generator & Edge-Case Synthesizer (M1 / Tier 1 & Tier 2)
Tests `tools/ziwei_vector_generator.py` for deterministic reproducibility, boundary coverage,
and schema validity across 1900-2100.
"""
import pytest
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any, List

try:
    from tools.ziwei_vector_generator import (
        generate_random_vectors,
        generate_edge_case_vectors,
        generate_stress_suite,
    )
except ImportError:
    # Allow fallback if module is imported via engine or relative path
    try:
        from engine.ziwei_vector_generator import (
            generate_random_vectors,
            generate_edge_case_vectors,
            generate_stress_suite,
        )
    except ImportError:
        pass


# ==============================================================================
# TIER 1: FEATURE COVERAGE TESTS (>=5 Cases)
# ==============================================================================

def test_generate_random_vectors_basic():
    """
    Tier 1 - Case 1: Verifies default and custom count generation.
    """
    from tools.ziwei_vector_generator import generate_random_vectors

    # Default count test
    vectors_default = generate_random_vectors()
    assert isinstance(vectors_default, list), "Expected list output"
    assert len(vectors_default) > 0, "Vector list must not be empty"

    # Custom count test
    count = 25
    vectors_custom = generate_random_vectors(count=count, seed=42)
    assert len(vectors_custom) == count, f"Expected {count} vectors, got {len(vectors_custom)}"


def test_seed_reproducibility():
    """
    Tier 1 - Case 2: Deterministic pseudo-random generation across identical seeds.
    """
    from tools.ziwei_vector_generator import generate_random_vectors

    seed = 9999
    run_1 = generate_random_vectors(count=30, seed=seed)
    run_2 = generate_random_vectors(count=30, seed=seed)
    assert run_1 == run_2, "Identical seeds must produce identical vector outputs"

    # Different seeds should produce distinct sequences
    run_3 = generate_random_vectors(count=30, seed=1234)
    assert run_1 != run_3, "Different seeds must produce different vector outputs"


def test_vector_schema_and_types():
    """
    Tier 1 - Case 3: Output schema conformity to Interface Contract in PROJECT.md.
    Schema: {"year": int, "month": int, "day": int, "hour": int, "minute": int,
             "gender": "nam"|"nu"|int, "view_mode": str, "school": str, "edge_case_type": str}
    """
    from tools.ziwei_vector_generator import generate_random_vectors

    vectors = generate_random_vectors(count=20, seed=42)
    for idx, vec in enumerate(vectors):
        assert isinstance(vec, dict), f"Vector {idx} is not a dict"
        assert "year" in vec and isinstance(vec["year"], int), f"Vector {idx} missing/invalid 'year'"
        assert "month" in vec and isinstance(vec["month"], int), f"Vector {idx} missing/invalid 'month'"
        assert "day" in vec and isinstance(vec["day"], int), f"Vector {idx} missing/invalid 'day'"
        assert "hour" in vec and isinstance(vec["hour"], int), f"Vector {idx} missing/invalid 'hour'"
        assert "minute" in vec and isinstance(vec["minute"], int), f"Vector {idx} missing/invalid 'minute'"
        assert "gender" in vec, f"Vector {idx} missing 'gender'"
        
        # Validate value ranges
        assert 1900 <= vec["year"] <= 2100, f"Year {vec['year']} out of bounds [1900, 2100]"
        assert 1 <= vec["month"] <= 12, f"Month {vec['month']} out of bounds [1, 12]"
        assert 1 <= vec["day"] <= 31, f"Day {vec['day']} out of bounds [1, 31]"
        assert 0 <= vec["hour"] <= 23, f"Hour {vec['hour']} out of bounds [0, 23]"
        assert 0 <= vec["minute"] <= 59, f"Minute {vec['minute']} out of bounds [0, 59]"


def test_generate_stress_suite_scale():
    """
    Tier 1 - Case 4: High-volume stress suite generation (1,000+ vectors).
    """
    from tools.ziwei_vector_generator import generate_stress_suite

    stress_suite = generate_stress_suite(count=1000, seed=42)
    assert isinstance(stress_suite, list)
    assert len(stress_suite) >= 1000, f"Expected >= 1000 vectors in stress suite, got {len(stress_suite)}"

    # Ensure all vectors can construct a valid datetime object
    for idx, vec in enumerate(stress_suite[:100]):
        try:
            dt = datetime(vec["year"], vec["month"], vec["day"], vec["hour"], vec["minute"])
            assert dt is not None
        except ValueError as e:
            pytest.fail(f"Vector {idx} generated invalid date {vec}: {e}")


def test_cli_invocation_support():
    """
    Tier 1 - Case 5: Invocable via CLI as a standalone script or module.
    """
    cmd = [sys.executable, "-m", "tools.ziwei_vector_generator", "--count", "10", "--seed", "42"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"CLI invocation failed with error:\n{res.stderr}"
    assert "10" in res.stdout or "vectors" in res.stdout.lower() or "{" in res.stdout, (
        f"CLI output did not contain expected feedback: {res.stdout}"
    )


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (6 Classes per ORIGINAL_REQUEST §R1)
# ==============================================================================

def test_edge_case_class_1_century_and_leap_boundaries():
    """
    Tier 2 - Class 1: Century leap year boundaries (1900, 2000, 2100 Feb 28/29).
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    assert len(edge_vectors) > 0, "Edge-case vector list must not be empty"

    # Verify presence of century boundary years
    years_present = {v["year"] for v in edge_vectors}
    assert 1900 in years_present, "Class 1: Year 1900 century boundary missing"
    assert 2000 in years_present, "Class 1: Year 2000 leap century boundary missing"
    assert 2100 in years_present, "Class 1: Year 2100 century boundary missing"

    # Verify Feb 29 on leap year 2000 or other leap years
    feb29_vectors = [v for v in edge_vectors if v.get("month") == 2 and v.get("day") == 29]
    assert len(feb29_vectors) > 0, "Class 1: Leap year Feb 29 edge cases missing"


def test_edge_case_class_2_lunar_leap_months():
    """
    Tier 2 - Class 2: Lunar leap months (1984 Leap 10, 2006 Leap 7, 2020 Leap 4, 2023 Leap 2, 2025 Leap 6).
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    leap_month_cases = [
        v for v in edge_vectors
        if "leap" in str(v.get("edge_case_type", "")).lower() or
           v.get("year") in (1984, 2006, 2020, 2023, 2025)
    ]
    assert len(leap_month_cases) >= 3, (
        f"Class 2: Expected >=3 lunar leap month edge cases, found {len(leap_month_cases)}"
    )


def test_edge_case_class_3_solar_term_minute_transitions():
    """
    Tier 2 - Class 3: Solar term transitions to minute precision (Lập Xuân, Hạ Chí, Thu Phân, Đông Chí).
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    solar_term_cases = [
        v for v in edge_vectors
        if "solar" in str(v.get("edge_case_type", "")).lower() or
           "tiet_khi" in str(v.get("edge_case_type", "")).lower() or
           v.get("minute") in (0, 59, 30, 45)
    ]
    assert len(solar_term_cases) >= 4, (
        f"Class 3: Expected >=4 solar term minute transition edge cases, found {len(solar_term_cases)}"
    )


def test_edge_case_class_4_zi_hour_transitions():
    """
    Tier 2 - Class 4: Zi hour transitions (Dạ Tý 23:00 - 23:59 vs. Chính Tý 00:00 - 00:59).
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    zi_hour_cases = [v for v in edge_vectors if v.get("hour") in (23, 0)]
    assert len(zi_hour_cases) >= 2, (
        f"Class 4: Expected >=2 Zi hour boundary cases (23h and 00h), found {len(zi_hour_cases)}"
    )

    # Check 23h Da Ty and 00h Chinh Ty representation
    hours_present = {v["hour"] for v in zi_hour_cases}
    assert 23 in hours_present, "Class 4: Hour 23 (Dạ Tý) missing"
    assert 0 in hours_present, "Class 4: Hour 00 (Chính Tý) missing"


def test_edge_case_class_5_year_boundary_changing_pillars():
    """
    Tier 2 - Class 5: Year boundary changing pillars (Dec 31 23:59 -> Jan 1 00:00).
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    year_boundary_cases = [
        v for v in edge_vectors
        if (v.get("month") == 12 and v.get("day") == 31) or
           (v.get("month") == 1 and v.get("day") == 1)
    ]
    assert len(year_boundary_cases) >= 2, (
        f"Class 5: Expected >=2 Year boundary cases (Dec 31 / Jan 1), found {len(year_boundary_cases)}"
    )


def test_edge_case_class_6_special_cuc_and_gender_polarities():
    """
    Tier 2 - Class 6: Special Cục số combinations & Nam/Nữ polarity across Stems and Branches.
    """
    from tools.ziwei_vector_generator import generate_edge_case_vectors

    edge_vectors = generate_edge_case_vectors()
    genders = {str(v.get("gender")).lower() for v in edge_vectors}
    assert "nam" in genders or "1" in genders or 1 in genders, "Class 6: Male polarity missing"
    assert "nu" in genders or "0" in genders or 0 in genders or "nữ" in genders, "Class 6: Female polarity missing"


def test_vector_generator_custom_year_range():
    """
    Tier 2: Custom year range filtering [start_year, end_year].
    """
    from tools.ziwei_vector_generator import generate_random_vectors

    start_y = 1960
    end_y = 1975
    vectors = generate_random_vectors(count=50, seed=42, start_year=start_y, end_year=end_y)
    for v in vectors:
        assert start_y <= v["year"] <= end_y, f"Year {v['year']} outside custom range [{start_y}, {end_y}]"
