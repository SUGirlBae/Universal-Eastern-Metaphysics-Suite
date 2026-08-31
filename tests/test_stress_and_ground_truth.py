import pytest
from datetime import datetime
from engine.ground_truth_parser import parse_canonical_astrolabe_ai_copy
from engine.ziwei_comparator import compare_engine_with_ground_truth
from engine.stress_test_pipeline import run_ziwei_stress_test_pipeline
from engine.tu_vi_advanced import calculate_universal_tu_vi

SAMPLE_TINHMENHDO_TEXT = """
* **Giới tính:** Nam
* **Ngày sinh:** 6/12/1999 1h55 (Hành chính), 2h07 (Giờ Mặt Trời)
* **Âm lịch:** Năm Kỷ Mão, ngày 29 tháng 10, giờ Sửu
* **Nơi sinh:** Bạc Liêu, Vietnam (9.283°, 105.720°)
* **Mệnh:** Thành Đầu Thổ.
* **Cục:** Hỏa Lục Cục (Khởi vận 6 tuổi). **Thân:** Thân cư PHÚC.
* **Niên Hóa (Can Kỷ):** Lộc (A) -> Vũ Khúc (ĐIỀN) | Quyền (B) -> Tham Lang (ĐIỀN) | Khoa (C) -> Thiên Lương (DI) | Kỵ (D) -> Văn Khúc (TẬT).
* **Đường Kị chuyển Lộc:** BÀO -> ĐIỀN, QUAN -> BÀO, ĐIỀN -> QUAN, PHÚC -> BÀO.
* **Đường chuyển Kị:** BÀO -> ĐIỀN (Tham Lang), QUAN -> BÀO (Liêm Trinh), ĐIỀN -> QUAN (Cự Môn).

| Tên Cung | Vị trí | Can Chi | **Đại Vận Tử Vi (DV-TV)** | Chính Tinh | Phụ Tinh | Phi Lộc (A) | Phi Quyền (B) | Phi Khoa (C) | Phi Kỵ (D) | Tự Hóa / Hướng Tâm | Phương Viên Lộc Kị Toàn Đồ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **MỆNH** | Tuất | Giáp Tuất | **6 - 15** | VCD xung (Thiên Cơ - Thiên Lương) | Địa Không, Thiên Diêu | -> BÀO | -> BÀO | -> ĐIỀN | -> QUAN |  |  |
| **BÀO** | Dậu | Quý Dậu | **16 - 25** | Liêm Trinh, Phá Quân | Văn Xương, Bát Tọa | -> BÀO | -> QUAN | -> PHÚC | -> ĐIỀN | **Tự hóa Lộc** (Phá Quân) |  |
| **PHÚC** | Tý | Bính Tý | **106 - 115** | Thiên Đồng, Thái Âm | Địa Kiếp, Thiên Khôi | -> PHÚC | -> DI | -> BÀO | -> BÀO | **Tự hóa Lộc** (Thiên Đồng) | 1 Kỵ (D) |
"""

def test_ground_truth_parser_and_comparator():
    gt = parse_canonical_astrolabe_ai_copy(SAMPLE_TINHMENHDO_TEXT)
    assert gt["profile"]["gender"] == "Nam"
    assert len(gt["palaces"]) >= 3
    
    dt = datetime(1999, 12, 6, 1, 55)
    engine_res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")
    diffs = compare_engine_with_ground_truth(engine_res, gt)
    assert len(diffs) == 0 # Zero diff

def test_ziwei_stress_test_500_vectors():
    res = run_ziwei_stress_test_pipeline(num_vectors=500)
    assert res["success"] is True
    assert res["errors_count"] == 0
    assert res["avg_duration_ms"] < 15.0 # High-speed sub-15ms on full 110+ stars & matrix # Sub 5ms
