"""
Unit and Integration Test Suite for CanonicalAstrolabe Ground-Truth Markdown Parser (M2 / Tier 1 & Tier 2)
Validates parsing of 3-table format across all 5 authentic ground truth files:
benchmark_01.md, benchmark_02.md, benchmark_03.md, tử vi Vector_04.md, Tử_vi Vector_05.md.
"""
import os
import pytest
from pathlib import Path
from typing import Dict, Any, List

from engine.ground_truth_parser import (
    parse_canonical_astrolabe_ai_copy,
    normalize_branch,
    normalize_palace_code,
    clean_markdown_text,
    split_markdown_tables,
    parse_tang_can
)

try:
    from engine.ground_truth_parser import parse_astrolabe_benchmark_markdown, CanonicalAstrolabeChart
except ImportError:
    parse_astrolabe_benchmark_markdown = None
    CanonicalAstrolabeChart = None

# Sample embedded text for isolated standalone testing
SAMPLE_MINH_HUNG = """
* **Tên:** Phạm Ngọc Vector_05
* **Giới tính:** Nam
* **Ngày sinh:** 6/12/1999 1h55 (Hành chính), 2h07 (Giờ Mặt Trời)
* **Âm lịch:** Năm Kỷ Mão, ngày 29 tháng 10, giờ Sửu
* **Nơi sinh:** Bạc Liêu, Vietnam (9.283°, 105.720°)
* **Tứ trụ cơ bản (theo tiết khí):** Năm Kỷ Mão, Tháng Ất Hợi, Ngày Nhâm Thìn (Nhật chủ), Giờ Tân Sửu
* **Tử vi cơ bản (theo âm lịch):** Cung Mệnh tại Tuất có VCD (Thiên Cơ - Thiên Lương xung), Cung Tài tại Ngọ VCD (Thiên Đồng - Thái Âm xung), Cung Quan tại Dần có Thái Dương, Cự Môn

---

## I. DỮ LIỆU BÁT TỰ TỨ TRỤ

* **Tiết khí:** Tiểu Tuyết. **Vận:** Nghịch.

### 1. Bảng Tứ Trụ Chi Tiết

| Thành phần | Trụ Năm | Trụ Tháng | **Trụ Ngày (Nhật Chủ)** | Trụ Giờ |
| --- | --- | --- | --- | --- |
| **Thập Thần** | Quan | Thương | **Nhật Chủ** | Ấn |
| **Thiên Can** | **KỶ** | **ẤT** | **NHÂM** | **TÂN** |
| **Địa Chi** | **MÃO** | **HỢI** | **THÌN** | **SỬU** |
| **Tàng Can** | Ất (Thương) | Nhâm (Tỷ), Giáp (Thực) | Mậu (Sát), Ất (Thương), Quý (Kiếp) | Kỷ (Quan), Quý (Kiếp), Tân (Ấn) |
| **Trường Sinh** | Tử | LQuan | Mộ | Suy |
| **Nạp Âm** | Thành Đầu Thổ | Sơn Đầu Hỏa | Trường Lưu Thủy | Bích Thượng Thổ |

### 2. Đại Vận Tứ Trụ (DV-TT) - Khởi từ 6 tuổi

| Vận | 1 (6-15t) | 2 (16-25t) | 3 (26-35t) | 4 (36-45t) | 5 (46-55t) | 6 (56-65t) | 7 (66-75t) | 8 (76-85t) | 9 (86-95t) | 10 (96-105t) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Năm** | 2005 | 2015 | 2025 | 2035 | 2045 | 2055 | 2065 | 2075 | 2085 | 2095 |
| **Can Chi** | **Giáp Tuất** | **Quý Dậu** | **Nhâm Thân** | **Tân Mùi** | **Canh Ngọ** | **Kỷ Tị** | **Mậu Thìn** | **Đinh Mão** | **Bính Dần** | **Ất Sửu** |
| **Thần** | Thực | T.Tài | Tài | Kiêu | Ấn | Sát | Quan | T.Tài | Tài | Kiêu |

---

## II. TỬ VI CHI TIẾT 12 CUNG VỊ và PHI HOÁ

* **Cơ bản:** Âm Nam, Âm dương nghịch lý. **Mệnh:** Thành Đầu Thổ.
* **Cục:** Hỏa Lục Cục (Khởi vận 6 tuổi). **Thân:** Thân cư PHÚC.
* **Đặc điểm:** Sinh mùa Đông (Không được mùa sinh), Cục sinh mệnh.
* **Niên Hóa (Can Kỷ):** Lộc (A) -> Vũ Khúc (ĐIỀN) | Quyền (B) -> Tham Lang (ĐIỀN) | Khoa (C) -> Thiên Lương (DI) | Kỵ (D) -> Văn Khúc (TẬT).
* **Đường Kị chuyển Lộc:** BÀO -> ĐIỀN, QUAN -> BÀO, ĐIỀN -> QUAN, PHÚC -> BÀO.
* **Đường chuyển Kị:** BÀO -> ĐIỀN (Tham Lang), QUAN -> BÀO (Liêm Trinh), ĐIỀN -> QUAN (Cự Môn).

| Tên Cung | Vị trí | Can Chi | **Đại Vận Tử Vi (DV-TV)** | Chính Tinh | Phụ Tinh | Phi Lộc (A) | Phi Quyền (B) | Phi Khoa (C) | Phi Kỵ (D) | Tự Hóa / Hướng Tâm | Phương Viên Lộc Kị Toàn Đồ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **MỆNH** | Tuất | Giáp Tuất | **6 - 15** | VCD xung (Thiên Cơ - Thiên Lương) | Địa Không, Thiên Diêu | -> BÀO | -> BÀO | -> ĐIỀN | -> QUAN |  |  |
| **PHỤ** | Hợi | Ất Hợi | **116 - 125** | Tử Vi, Thất Sát | Địa Kiếp, Hóa Kị | -> PHỤ | -> ĐIỀN | -> MỆNH | -> NÔ |  |  |
| **PHÚC** | Tý | Bính Tý | **106 - 115** | Thiên Đồng, Thái Âm | Thiên Khôi, Văn Xương | -> PHÚC | -> DI | -> BÀO | -> BÀO | **Tự hóa Lộc** (Thiên Đồng) | 1 Kỵ (D) |
| **ĐIỀN** | Sửu | Đinh Sửu | **96 - 105** | Vũ Khúc, Tham Lang | Hóa Lộc, Hóa Quyền | -> NÔ | -> PHÚC | -> PHỤ | -> BÀO |  | 2 Lộc (A) |
| **QUAN** | Dần | Mậu Dần | **86 - 95** | Thái Dương, Cự Môn | Tả Phụ, Hữu Bật | -> BÀO | -> MỆNH | -> QUAN | -> DI |  |  |
| **NÔ** | Mão | Kỷ Mão | **76 - 85** | Thiên Tướng | Thiên Việt, Bác Sĩ | -> ĐIỀN | -> ĐIỀN | -> DI | -> TẬT |  |  |
| **DI** | Thìn | Canh Thìn | **66 - 75** | Thiên Cơ, Thiên Lương | Hóa Khoa, Lộc Tồn | -> QUAN | -> ĐIỀN | -> TÀI | -> PHÚC | **Tự hóa Kỵ** (Thiên Cơ) | 1 Kỵ (D) |
| **TẬT** | Tị | Tân Tị | **56 - 65** | Liêm Trinh, Phá Quân | Văn Khúc, Hóa Kị | -> BÀO | -> QUAN | -> TỬ | -> PHỤ | **Tự hóa Kỵ** (Văn Khúc) | 1 Kỵ (D) |
| **TÀI** | Ngọ | Nhâm Ngọ | **46 - 55** | VCD xung (Thiên Đồng - Thái Âm) | Kình Dương, Linh Tinh | -> TÀI | -> PHÚC | -> NÔ | -> ĐIỀN |  |  |
| **TỬ** | Mùi | Quý Mùi | **36 - 45** | Thiên Phủ | Thiên Mã, Phong Cáo | -> PHỤ | -> QUAN | -> TỬ | -> ĐIỀN |  |  |
| **PHỐI** | Thân | Giáp Thân | **26 - 35** | VCD xung (Thái Dương - Cự Môn) | Đà La, Hỏa Tinh | -> BÀO | -> BÀO | -> ĐIỀN | -> QUAN |  |  |
| **BÀO** | Dậu | Quý Dậu | **16 - 25** | VCD xung (Tử Vi - Thất Sát) | Ân Quang, Thiên Quý | -> PHỤ | -> QUAN | -> TỬ | -> ĐIỀN | **Tự hóa Lộc** (Phá Quân) | 1 Lộc (A) |
"""

def _get_gt_files() -> List[str]:
    """Helper to locate authentic sample files."""
    paths = [
        r"D:\Book-20251020T041506Z-1-001\Tử_vi\benchmark_01.md",
        r"D:\Book-20251020T041506Z-1-001\Tử_vi\benchmark_02.md",
        r"D:\Book-20251020T041506Z-1-001\Tử_vi\benchmark_03.md",
        r"D:\Book-20251020T041506Z-1-001\Tử_vi\tử vi Vector_04.md",
        r"D:\Book-20251020T041506Z-1-001\Tử_vi\Tử_vi Vector_05.md",
    ]
    return [p for p in paths if os.path.exists(p)]


# ==============================================================================
# TIER 1: FEATURE EXTRACTION TESTS
# ==============================================================================

def test_parser_basic_sample():
    """
    Tier 1 - Case 1: Parses sample text and verifies top-level data structure.
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    assert isinstance(data, dict)
    assert "profile" in data
    assert "tu_vi_meta" in data
    assert "palaces" in data
    assert len(data["palaces"]) == 12


def test_parser_profile_extraction():
    """
    Tier 1 - Case 2: Verifies profile metadata (Gender, Raw birth dates, location).
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    profile = data.get("profile", {})
    assert profile.get("gender") == "Nam"
    date_field = profile.get("birth_date_str") or profile.get("birth_datetime_raw") or profile.get("birth_date_raw", "")
    assert "6/12/1999" in date_field
    assert "Bạc Liêu" in profile.get("birth_place", "")


def test_parser_ziwei_meta_fields():
    """
    Tier 1 - Case 3: Verifies Ziwei metadata (Cuc, Menh Nayin, Than palace).
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    meta = data.get("tu_vi_meta", {})
    cuc_field = meta.get("cuc_name") or meta.get("cuc", "")
    assert "Hỏa Lục Cục" in cuc_field
    assert "Thành Đầu Thổ" in meta.get("menh_nayin", "")
    assert "PHÚC" in meta.get("than_palace", "")


def test_parser_four_pillars_table_1():
    """
    Tier 1 - Case 4: Verifies Table 1 (Four Pillars detail: Stems, Branches, Hidden Stems, Chang Sheng, Na Yin).
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    fp = data.get("four_pillars", {}) or data.get("bazi", {}).get("pillars", {})
    assert len(fp) == 4
    assert "year" in fp and "month" in fp and "day" in fp and "hour" in fp

    # Check Day Pillar (Nhật Chủ: Nhâm Thìn)
    day_p = fp["day"]
    assert day_p.get("can") in ("NHÂM", "Nhâm")
    assert day_p.get("chi") in ("THÌN", "Thìn")


def test_parser_bazi_da_yun_table_2():
    """
    Tier 1 - Case 5: Verifies Table 2 (10 Da Yun steps with years, Can Chi, Ten Gods).
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    da_yun = data.get("da_yun_bazi", []) or data.get("bazi", {}).get("da_yun_steps", [])
    assert len(da_yun) == 10
    assert da_yun[0].get("start_year") == 2005
    assert "Giáp Tuất" in da_yun[0].get("can_chi", "")


def test_parser_12_palaces_matrix_attributes():
    """
    Tier 1 - Case 6: Verifies all 12 palaces contain required matrix columns.
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    palaces = data.get("palaces", [])
    assert len(palaces) == 12

    palace_names = {p["name"] for p in palaces}
    expected_names = {"MỆNH", "PHỤ", "PHÚC", "ĐIỀN", "QUAN", "NÔ", "DI", "TẬT", "TÀI", "TỬ", "PHỐI", "BÀO"}
    assert palace_names == expected_names, f"Missing palaces: {expected_names - palace_names}"

    for p in palaces:
        assert p.get("branch"), f"Palace {p['name']} missing branch"
        assert p.get("can_chi"), f"Palace {p['name']} missing can_chi"
        assert "main_stars" in p, f"Palace {p['name']} missing main_stars"
        assert "phi_loc" in p, f"Palace {p['name']} missing phi_loc"
        assert "phi_quyen" in p, f"Palace {p['name']} missing phi_quyen"
        assert "phi_khoa" in p, f"Palace {p['name']} missing phi_khoa"
        assert "phi_ky" in p, f"Palace {p['name']} missing phi_ky"


def test_parser_kham_thien_si_hua_routes():
    """
    Tier 1 - Case 7: Verifies extraction of Đường Kị chuyển Lộc & Đường chuyển Kị.
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    routes = data.get("si_hua_routes", {})
    assert "ky_chuyen_loc" in routes
    assert len(routes["ky_chuyen_loc"]) > 0
    assert any("BÀO -> ĐIỀN" in r for r in routes["ky_chuyen_loc"])


# ==============================================================================
# TIER 2: BOUNDARY & AUTHENTIC SAMPLES VERIFICATION
# ==============================================================================

def test_parser_all_5_authentic_ground_truth_files():
    """
    Tier 2 - Case 1: Verifies parser across all 5 authentic files in D:\\Book-20251020T041506Z-1-001\\Tử_vi\\.
    """
    gt_files = _get_gt_files()
    if not gt_files:
        pytest.skip("Ground-truth files not found in D: drive, skipping file-based test.")

    for fpath in gt_files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        parsed = parse_canonical_astrolabe_ai_copy(content)
        fname = Path(fpath).name
        assert parsed is not None, f"Failed to parse {fname}"
        assert parsed["profile"].get("gender") in ("Nam", "Nữ"), f"Invalid gender in {fname}"
        assert len(parsed["palaces"]) == 12, f"Expected 12 palaces in {fname}, got {len(parsed['palaces'])}"


def test_parser_vcd_and_main_stars_handling():
    """
    Tier 2 - Case 2: Verifies VCD (Vô Chính Diệu) does not mistakenly store 'VCD' as a star name.
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    menh_palace = next(p for p in data["palaces"] if p["name"] == "MỆNH")
    assert "VCD" not in menh_palace["main_stars"], "VCD must not be parsed as a star name"


def test_parser_self_transformations_in_palace():
    """
    Tier 2 - Case 3: Verifies extraction of Tự Hóa / Hướng Tâm.
    """
    data = parse_canonical_astrolabe_ai_copy(SAMPLE_MINH_HUNG)
    phuc_palace = next(p for p in data["palaces"] if p["name"] == "PHÚC")
    raw_th = phuc_palace.get("tu_hoa_huong_tam_raw") or phuc_palace.get("tu_hoa_huong_tam", "")
    self_trans = phuc_palace.get("self_transformations", [])
    
    assert ("Tự hóa Lộc" in raw_th) or any("Tự hóa Lộc" in st for st in self_trans)
    assert ("Thiên Đồng" in raw_th) or any("Thiên Đồng" in st for st in self_trans)

    di_palace = next(p for p in data["palaces"] if p["name"] == "DI")
    raw_di = di_palace.get("tu_hoa_huong_tam_raw") or di_palace.get("tu_hoa_huong_tam", "")
    self_di = di_palace.get("self_transformations", [])
    assert ("Tự hóa Kỵ" in raw_di) or any("Tự hóa Kỵ" in st for st in self_di)


def test_parser_malformed_input_resilience():
    """
    Tier 2 - Case 4: Tests graceful handling of malformed, empty, or truncated inputs.
    """
    # Empty input
    empty_res = parse_canonical_astrolabe_ai_copy("")
    assert isinstance(empty_res, dict)
    assert empty_res.get("palaces") == []

    # Corrupted markdown without tables
    corrupt_text = "Some random text without markdown tables\n* **Giới tính:** Nữ\n"
    corrupt_res = parse_canonical_astrolabe_ai_copy(corrupt_text)
    assert corrupt_res["profile"].get("gender") == "Nữ"
    assert corrupt_res.get("palaces") == []
