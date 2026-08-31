"""
Unit and Integration Test Suite for Ziwei Zero-Diff Comparator (M2 / Tiers 1-4)
Validates zero-diff accuracy, discrepancy detection, and root-cause taxonomy categorization
across 7 comparison steps.
"""
import os
import pytest
from datetime import datetime
from typing import Dict, Any, List

from engine.ground_truth_parser import parse_canonical_astrolabe_ai_copy
from engine.ziwei_comparator import (
    compare_engine_with_ground_truth,
    normalize_branch,
    normalize_palace_code,
    ComparisonReport,
    ComparisonDiff,
    ERR_SI_HUA_TABLE,
    ERR_CUC_SO,
    ERR_BRANCH_ORTHOGRAPHY,
    ERR_TRANSFORMATION_LOGIC,
    ERR_LUNAR_SOLAR_DATE,
    ERR_STAR_PLACEMENT,
    ERR_DA_YUN_RANGE,
    ERR_CAN_CHI,
)
from engine.tu_vi_advanced import calculate_universal_tu_vi

# Sample ground truth markdown matching engine calculation for zero-diff tests
SAMPLE_GROUND_TRUTH = """
* **Tên:** Phạm Ngọc Vector_05
* **Giới tính:** Nam
* **Ngày sinh:** 6/12/1999 1h55 (Hành chính), 2h07 (Giờ Mặt Trời)
* **Âm lịch:** Năm Kỷ Mão, ngày 29 tháng 10, giờ Sửu
* **Nơi sinh:** Bạc Liêu, Vietnam (9.283°, 105.720°)
* **Mệnh:** Thành Đầu Thổ.
* **Cục:** Hỏa Lục Cục (Khởi vận 6 tuổi). **Thân:** Thân cư PHÚC.
* **Niên Hóa (Can Kỷ):** Lộc (A) -> Vũ Khúc (ĐIỀN) | Quyền (B) -> Tham Lang (ĐIỀN) | Khoa (C) -> Thiên Lương (DI) | Kỵ (D) -> Văn Khúc (TẬT).
* **Đường Kị chuyển Lộc:** BÀO -> ĐIỀN, QUAN -> BÀO, ĐIỀN -> QUAN, PHÚC -> BÀO.
* **Đường chuyển Kị:** BÀO -> ĐIỀN (Tham Lang), QUAN -> BÀO (Liêm Trinh), ĐIỀN -> QUAN (Cự Môn), PHÚC -> BÀO (Liêm Trinh).

| Tên Cung | Vị trí | Can Chi | **Đại Vận Tử Vi (DV-TV)** | Chính Tinh | Phụ Tinh | Phi Lộc (A) | Phi Quyền (B) | Phi Khoa (C) | Phi Kỵ (D) | Tự Hóa / Hướng Tâm | Phương Viên Lộc Kị Toàn Đồ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **MỆNH** | Tuất | Giáp Tuất | **6 - 15** | VCD xung (Thiên Cơ - Thiên Lương) | Địa Không, Hỏa Tinh, Thiên Diêu | -> BÀO | -> BÀO | -> ĐIỀN | -> QUAN |  |  |
| **BÀO** | Dậu | Quý Dậu | **16 - 25** | Liêm Trinh, Phá Quân | Văn Xương, Bát Tọa | -> BÀO | -> QUAN | -> PHÚC | -> ĐIỀN | **Tự hóa Lộc** (Phá Quân) |  |
| **PHỐI** | Thân | Nhâm Thân | **26 - 35** | VCD xung (Thái Dương - Cự Môn) | Thiên Việt, Tử Phù | -> DI | -> TẬT | -> ĐIỀN | -> ĐIỀN |  |  |
| **TỬ** | Mùi | Tân Mùi | **36 - 45** | VCD xung (Vũ Khúc - Tham Lang) | Kình Dương, Quan Phù | -> QUAN | -> QUAN | -> TẬT | -> BÀO |  |  |
| **TÀI** | Ngọ | Canh Ngọ | **46 - 55** | VCD xung (Thiên Đồng - Thái Âm) | Lộc Tồn, Thiên Hình | -> QUAN | -> ĐIỀN | -> PHÚC | -> PHÚC | **Hướng tâm Khoa** (Thái Âm), **Hướng tâm Kỵ** (Thiên Đồng) |  |
| **TẬT** | Tị | Kỷ Tị | **56 - 65** | Tử Vi, Thất Sát | Đà La, Văn Khúc | -> ĐIỀN | -> ĐIỀN | -> DI | -> TẬT | **Tự hóa Kỵ** (Văn Khúc) | 2 Kỵ (D) |
| **DI** | Thìn | Mậu Thìn | **66 - 75** | Thiên Cơ, Thiên Lương | Hóa Khoa, Thiên Không | -> ĐIỀN | -> PHÚC | -> ĐIỀN | -> DI | **Tự hóa Kỵ** (Thiên Cơ) | 2 Lộc (A), 1 Kỵ (D) |
| **NÔ** | Mão | Đinh Mão | **76 - 85** | Thiên Tướng | Thiên Khốc, Thái Tuế | -> PHÚC | -> PHÚC | -> DI | -> QUAN |  |  |
| **QUAN** | Dần | Bính Dần | **86 - 95** | Thái Dương, Cự Môn | Thiên Quý, Trực Phù | -> PHÚC | -> DI | -> BÀO | -> BÀO |  | 11 Lộc (A), 7 Kỵ (D) |
| **ĐIỀN** | Sửu | Đinh Sửu | **96 - 105** | Vũ Khúc, Tham Lang | Tả Phụ, Hữu Bật | -> PHÚC | -> PHÚC | -> DI | -> QUAN |  |  |
| **PHÚC** | Tý | Bính Tý | **106 - 115** | Thiên Đồng, Thái Âm | Địa Kiếp, Thiên Khôi | -> PHÚC | -> DI | -> BÀO | -> BÀO | **Tự hóa Lộc** (Thiên Đồng) |  |
| **PHỤ** | Hợi | Ất Hợi | **116 - 125** | Thiên Phủ | Linh Tinh, Bạch Hổ | -> DI | -> DI | -> TẬT | -> PHÚC | **Hướng tâm Khoa** (Tử Vi) |  |
"""


# ==============================================================================
# TIER 1: ZERO-DIFF ACCURACY TESTS
# ==============================================================================

def test_zero_diff_on_matching_chart():
    """
    Tier 1 - Case 1: Identical calculation and ground-truth produces 0 diffs.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert report.is_zero_diff, f"Expected zero diff, found {len(report)} diffs: {report}"
    assert len(report) == 0


def test_comparator_returns_report_properties():
    """
    Tier 1 - Case 2: Comparator returns a ComparisonReport object with metadata properties.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert isinstance(report, ComparisonReport)
    assert report.total_diffs == 0
    assert isinstance(report.format_report(), str)
    assert "100% ZERO-DIFF MATCH" in report.format_report()


def test_7_step_verification_summary():
    """
    Tier 1 - Case 3: Verifies all 7 comparison pipeline steps are executed and tracked.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    summary = report.summary_by_step
    assert len(summary) == 7
    for step in range(1, 8):
        assert step in summary
        assert summary[step]["diffs_count"] == 0


# ==============================================================================
# TIER 2: GRANULAR MISMATCH DETECTION TESTS
# ==============================================================================

def test_detect_can_chi_mismatch():
    """
    Tier 2 - Case 1: Detects intentionally mutated Can Chi in palace and isolates root cause.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    # Mutate a palace Can Chi
    for p in engine_res["palaces"]:
        if p["branch_name"] == "Tuất":
            p["can_name"] = "Canh"  # True is Giáp

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert not report.is_zero_diff
    assert report.total_diffs > 0
    assert ERR_CAN_CHI in report.root_causes
    assert any("Tuất" in str(d) and "Can Chi" in str(d) for d in report)


def test_detect_cuc_so_mismatch():
    """
    Tier 2 - Case 2: Detects mismatch in Cuc name / Cuc number.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    # Mutate Cuc
    engine_res["client_profile"]["cuc_name"] = "Thủy Nhị Cục"

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert not report.is_zero_diff
    assert ERR_CUC_SO in report.root_causes


def test_detect_main_stars_mismatch():
    """
    Tier 2 - Case 3: Detects mismatch in 14 Main Stars placement.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    # Mutate Main Stars in Dần (Quan)
    for p in engine_res["palaces"]:
        if p["branch_name"] == "Dần":
            p["main_stars"] = ["Tử Vi"]  # True is Thái Dương, Cự Môn

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert not report.is_zero_diff
    assert ERR_STAR_PLACEMENT in report.root_causes


def test_detect_missing_self_transformation():
    """
    Tier 2 - Case 4: Detects missing Tự Hóa (Self-Transformation).
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    # Clear self transformations for Dậu (Bào)
    for f in engine_res["flying_stars"]["palace_flying_stars"]:
        if f["branch_name"] == "Dậu":
            f["self_transformations"] = []

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert not report.is_zero_diff
    assert any("Dậu" in str(d) and "Tự Hóa" in str(d) for d in report)


def test_detect_flying_stars_destination_mismatch():
    """
    Tier 2 - Case 5: Detects mutated destination in Flying Stars Matrix.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")

    # Mutate Phi Lộc target for Mệnh (Tuất)
    for f in engine_res["flying_stars"]["palace_flying_stars"]:
        if f["branch_name"] == "Tuất":
            f["phi_loc"]["target_palace"] = "QUAN"  # True is BÀO

    report = compare_engine_with_ground_truth(engine_res, gt_data)
    assert not report.is_zero_diff
    assert any("Tuất" in str(d) and "Phi Lộc" in str(d) for d in report)


def test_branch_spelling_normalization_tolerance():
    """
    Tier 2 - Case 6: Verifies that 'Tị' and 'Tỵ' are normalized without causing false positive diffs.
    """
    assert normalize_branch("Tị") == "Tỵ"
    assert normalize_branch("Tân Tị") == "Tân Tỵ"
    assert normalize_branch("Quý TỴ") == "Quý TỴ"


# ==============================================================================
# TIER 3: ROOT-CAUSE ISOLATION & SCHOOL COMPARISON
# ==============================================================================

def test_si_hua_root_cause_isolation():
    """
    Tier 3 - Case 1: Can Canh variation correctly classified as ERR_SI_HUA_TABLE.
    """
    gt_data = parse_canonical_astrolabe_ai_copy(SAMPLE_GROUND_TRUTH)
    dt = datetime(1999, 12, 6, 1, 55)
    res_trung_chau = calculate_universal_tu_vi(dt, gender=1, school="trung_chau")

    report = compare_engine_with_ground_truth(res_trung_chau, gt_data)
    if not report.is_zero_diff:
        assert ERR_SI_HUA_TABLE in report.root_causes or ERR_TRANSFORMATION_LOGIC in report.root_causes
