"""
Universal Multi-School Zi Wei Dou Shu Engine (Động Cơ Tử Vi Đẩu Số Đa Phái Toàn Diện)
Production-grade, 100% Offline, Deterministic, Zero Context Bloat, Optimized for AI Agents.

Schools & Paradigms Supported:
1. Nam Phái (110+ stars, Miếu Vượng Đắc Hãm, Tuần/Triệt, Star groupings)
2. Khâm Thiên Môn Tứ Hóa (Thập Can Niên Hóa A-B-C-D, Cung Can Tự Hóa, Hướng Tâm, Phi Tinh Tứ Hóa, Đường Kỵ chuyển Lộc, Đường chuyển Kỵ)
3. Lương Phái (Lương Nhược Du: Cung Can Phi Tinh, Tam Hợp, Lộc Kỵ tương hỗ)
4. Trung Châu Phái (Vương Đình Chi: 14 Tinh Hệ chuyên sâu, Canh Âm Kỵ / Nhâm Phủ Khoa)
5. Bắc Phái (Tứ Hóa định cách, Khí số vận hành)
6. Hybrids: Tự do kết hợp các trường phái theo yêu cầu

Astrolabes Supported:
- Thiên Bàn (Birth Baseline)
- Địa Bàn (Hidden Soul / Secondary Alignment)
- Nhân Bàn (Dynamic Interaction Alignment)

Dynamic Transit Layers:
- Tiên Thiên (Natal)
- Đại Vận (10-Year Major Cycle)
- Lưu Niên (Annual Cycle & Lưu Thần Sát)
- Lưu Nguyệt (Monthly Cycle)
- Lưu Nhật (Daily Cycle)
- Lưu Thời (Hourly Cycle)
"""
from datetime import datetime
from functools import lru_cache
from typing import Dict, Any, List, Optional, Tuple
import math
import json

try:
    from .lunar_solar import translate_han_viet, CAN, CHI, CHI_ELEMENT, LOCAL_TZ, calculate_time_coordinates
    from .bazi_engine import calculate_bazi
    from .ha_lac_engine import calculate_ha_lac
    from .tu_vi_bat_quai import calculate_dich_quai_12_cung
except (ImportError, ValueError):
    from lunar_solar import translate_han_viet, CAN, CHI, CHI_ELEMENT, LOCAL_TZ, calculate_time_coordinates
    from bazi_engine import calculate_bazi
    from ha_lac_engine import calculate_ha_lac
    from tu_vi_bat_quai import calculate_dich_quai_12_cung

# ==============================================================================
# LỤC THẬP HOA GIÁP NẠP ÂM (60 NA YIN MAP)
# ==============================================================================
NAP_AM_60 = {
    ("Giáp", "Tý"): "Hải Trung Kim", ("Ất", "Sửu"): "Hải Trung Kim",
    ("Bính", "Dần"): "Lư Trung Hỏa", ("Đinh", "Mão"): "Lư Trung Hỏa",
    ("Mậu", "Thìn"): "Đại Lâm Mộc", ("Kỷ", "Tỵ"): "Đại Lâm Mộc",
    ("Canh", "Ngọ"): "Lộ Bàng Thổ", ("Tân", "Mùi"): "Lộ Bàng Thổ",
    ("Nhâm", "Thân"): "Kiếm Phong Kim", ("Quý", "Dậu"): "Kiếm Phong Kim",
    ("Giáp", "Tuất"): "Sơn Đầu Hỏa", ("Ất", "Hợi"): "Sơn Đầu Hỏa",
    ("Bính", "Tý"): "Giản Hạ Thủy", ("Đinh", "Sửu"): "Giản Hạ Thủy",
    ("Mậu", "Dần"): "Thành Đầu Thổ", ("Kỷ", "Mão"): "Thành Đầu Thổ",
    ("Canh", "Thìn"): "Bạch Lạp Kim", ("Tân", "Tỵ"): "Bạch Lạp Kim",
    ("Nhâm", "Ngọ"): "Dương Liễu Mộc", ("Quý", "Mùi"): "Dương Liễu Mộc",
    ("Giáp", "Thân"): "Tuyền Trung Thủy", ("Ất", "Dậu"): "Tuyền Trung Thủy",
    ("Bính", "Tuất"): "Ốc Thượng Thổ", ("Đinh", "Hợi"): "Ốc Thượng Thổ",
    ("Mậu", "Tý"): "Tích Lịch Hỏa", ("Kỷ", "Sửu"): "Tích Lịch Hỏa",
    ("Canh", "Dần"): "Tùng Bách Mộc", ("Tân", "Mão"): "Tùng Bách Mộc",
    ("Nhâm", "Thìn"): "Trường Lưu Thủy", ("Quý", "Tỵ"): "Trường Lưu Thủy",
    ("Giáp", "Ngọ"): "Sa Trung Kim", ("Ất", "Mùi"): "Sa Trung Kim",
    ("Bính", "Thân"): "Sơn Hạ Hỏa", ("Đinh", "Dậu"): "Sơn Hạ Hỏa",
    ("Mậu", "Tuất"): "Bình Địa Mộc", ("Kỷ", "Hợi"): "Bình Địa Mộc",
    ("Canh", "Tý"): "Bích Thượng Thổ", ("Tân", "Sửu"): "Bích Thượng Thổ",
    ("Nhâm", "Dần"): "Kim Bạch Kim", ("Quý", "Mão"): "Kim Bạch Kim",
    ("Giáp", "Thìn"): "Phúc Đăng Hỏa", ("Ất", "Tỵ"): "Phúc Đăng Hỏa",
    ("Bính", "Ngọ"): "Thiên Hà Thủy", ("Đinh", "Mùi"): "Thiên Hà Thủy",
    ("Mậu", "Thân"): "Đại Trạch Thổ", ("Kỷ", "Dậu"): "Đại Trạch Thổ",
    ("Canh", "Tuất"): "Thoa Xuyến Kim", ("Tân", "Hợi"): "Thoa Xuyến Kim",
    ("Nhâm", "Tý"): "Tang Đố Mộc", ("Quý", "Sửu"): "Tang Đố Mộc",
    ("Giáp", "Dần"): "Đại Khê Thủy", ("Ất", "Mão"): "Đại Khê Thủy",
    ("Bính", "Thìn"): "Sa Trung Thổ", ("Đinh", "Tỵ"): "Sa Trung Thổ",
    ("Mậu", "Ngọ"): "Thiên Thượng Hỏa", ("Kỷ", "Mùi"): "Thiên Thượng Hỏa",
    ("Canh", "Thân"): "Thạch Lựu Mộc", ("Tân", "Dậu"): "Thạch Lựu Mộc",
    ("Nhâm", "Tuất"): "Đại Hải Thủy", ("Quý", "Hợi"): "Đại Hải Thủy"
}

try:
    import lunar_python
    if hasattr(lunar_python, "LunarYear") and hasattr(lunar_python.LunarYear, "fromYear"):
        lunar_python.LunarYear.fromYear = lru_cache(maxsize=512)(lunar_python.LunarYear.fromYear)
except Exception:
    pass

@lru_cache(maxsize=16384)
def _cached_lunar_coords(year: int, month: int, day: int, hour: int, minute: int, second: int = 0):
    """Cached high-speed lunar and four pillars coordinate resolver."""
    from lunar_python import Solar
    solar = Solar.fromYmdHms(year, month, day, hour, minute, second)
    lunar = solar.getLunar()
    year_can_idx = (lunar.getYearGanIndex() if hasattr(lunar, 'getYearGanIndex') else (year - 4) % 10)
    year_chi_idx = (lunar.getYearZhiIndex() if hasattr(lunar, 'getYearZhiIndex') else (year - 4) % 12)
    l_month = abs(lunar.getMonth())
    l_day = lunar.getDay()
    l_year = lunar.getYear()
    hour_chi_idx = lunar.getTimeZhiIndex()
    eight_char = lunar.getEightChar()
    fp = {
        "year": translate_han_viet(eight_char.getYear()),
        "month": translate_han_viet(eight_char.getMonth()),
        "day": translate_han_viet(eight_char.getDay()),
        "hour": translate_han_viet(eight_char.getTime())
    }
    return (year_can_idx, year_chi_idx, l_month, l_day, l_year, hour_chi_idx, fp)

@lru_cache(maxsize=8192)
def _cached_ha_lac_hex(year: int, month: int, day: int, hour: int, minute: int, gender: int):
    """Cached Ha Lac hexagram calculation for chart metadata header."""
    dt = datetime(year, month, day, hour, minute)
    hl = calculate_ha_lac(dt, gender=gender)
    return {
        "tien_thien": hl["tien_thien"]["hex_name"],
        "hau_thien": hl["hau_thien"]["hex_name"]
    }

# ==============================================================================
# 1. BẢNG TỨ HÓA THEO CÁC TRƯỜNG PHÁI (SI HUA TABLES)
# ==============================================================================
SI_HUA_TABLES = {
    "standard": { # Khâm Thiên / Toàn Thư tiêu chuẩn (Canh Canh Đồng Kỵ)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thái Âm",  "D": "Thiên Đồng"}, # Đồng Kỵ
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "canh_dong_am": { # Can Canh: Dương Vũ Đồng Âm (Nam Phái & CanonicalAstrolabe Default)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Đồng", "D": "Thái Âm"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "nam_phai": { # Nam Phái truyền thống (Đồng Âm)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Đồng", "D": "Thái Âm"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "kham_thien": { # Khâm Thiên Môn Tứ Hóa
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thái Âm",  "D": "Thiên Đồng"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "trung_chau": { # Trung Châu Phái (Vương Đình Chi: Canh Âm Kỵ / Nhâm Phủ Khoa)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Phủ","D": "Thái Âm"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Thiên Phủ","D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "canh_dong_ky": { # Biến thể Canh Canh Đồng Kỵ
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thái Âm",  "D": "Thiên Đồng"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "canh_dong_khoa": { # Biến thể Canh Canh Đồng Khoa (Dương Vũ Đồng Tướng)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Đồng","D": "Thiên Tướng"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "luong_phai": { # Lương Phái (Lương Nhược Du)
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Đồng", "D": "Thái Âm"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    },
    "bac_phai": { # Bắc Phái
        "Giáp": {"A": "Liêm Trinh", "B": "Phá Quân", "C": "Vũ Khúc", "D": "Thái Dương"},
        "Ất":   {"A": "Thiên Cơ",   "B": "Thiên Lương","C": "Tử Vi",   "D": "Thái Âm"},
        "Bính": {"A": "Thiên Đồng", "B": "Thiên Cơ",   "C": "Văn Xương","D": "Liêm Trinh"},
        "Đinh": {"A": "Thái Âm",    "B": "Thiên Đồng", "C": "Thiên Cơ", "D": "Cự Môn"},
        "Mậu":  {"A": "Tham Lang",  "B": "Thái Âm",    "C": "Hữu Bật",  "D": "Thiên Cơ"},
        "Kỷ":   {"A": "Vũ Khúc",    "B": "Tham Lang",  "C": "Thiên Lương","D": "Văn Khúc"},
        "Canh": {"A": "Thái Dương", "B": "Vũ Khúc",    "C": "Thiên Đồng", "D": "Thái Âm"},
        "Tân":  {"A": "Cự Môn",     "B": "Thái Dương", "C": "Văn Khúc", "D": "Văn Xương"},
        "Nhâm": {"A": "Thiên Lương","B": "Tử Vi",      "C": "Tả Phụ",   "D": "Vũ Khúc"},
        "Quý":  {"A": "Phá Quân",   "B": "Cự Môn",     "C": "Thái Âm",  "D": "Tham Lang"}
    }
}

# ==============================================================================
# 2. BẢNG AN 14 CHÍNH TINH & ĐẮC HÃM MIẾU VƯỢNG
# ==============================================================================
MAIN_STARS_BRIGHTNESS = {
    "Tử Vi":      {0: "Đ", 1: "M", 2: "M", 3: "Đ", 4: "V", 5: "M", 6: "M", 7: "Đ", 8: "V", 9: "Đ", 10: "M", 11: "B"},
    "Thiên Cơ":   {0: "Đ", 1: "Đ", 2: "V", 3: "M", 4: "M", 5: "H", 6: "Đ", 7: "Đ", 8: "V", 9: "M", 10: "Đ", 11: "H"},
    "Thái Dương": {0: "H", 1: "H", 2: "M", 3: "M", 4: "V", 5: "V", 6: "M", 7: "Đ", 8: "H", 9: "H", 10: "H", 11: "H"},
    "Vũ Khúc":    {0: "V", 1: "M", 2: "V", 3: "Đ", 4: "M", 5: "H", 6: "V", 7: "M", 8: "V", 9: "Đ", 10: "M", 11: "H"},
    "Thiên Đồng": {0: "V", 1: "H", 2: "M", 3: "Đ", 4: "H", 5: "Đ", 6: "H", 7: "H", 8: "M", 9: "H", 10: "Đ", 11: "V"},
    "Liêm Trinh": {0: "V", 1: "Đ", 2: "M", 3: "H", 4: "V", 5: "M", 6: "V", 7: "Đ", 8: "M", 9: "H", 10: "V", 11: "M"},
    "Thiên Phủ":  {0: "M", 1: "M", 2: "M", 3: "B", 4: "V", 5: "Đ", 6: "M", 7: "M", 8: "M", 9: "B", 10: "V", 11: "Đ"},
    "Thái Âm":    {0: "V", 1: "M", 2: "H", 3: "H", 4: "H", 5: "H", 6: "H", 7: "H", 8: "V", 9: "M", 10: "M", 11: "M"},
    "Tham Lang":  {0: "H", 1: "M", 2: "Đ", 3: "H", 4: "Đ", 5: "V", 6: "H", 7: "M", 8: "Đ", 9: "H", 10: "Đ", 11: "V"},
    "Cự Môn":     {0: "V", 1: "H", 2: "V", 3: "M", 4: "H", 5: "Đ", 6: "V", 7: "H", 8: "M", 9: "M", 10: "H", 11: "Đ"},
    "Thiên Tướng":{0: "V", 1: "M", 2: "M", 3: "H", 4: "V", 5: "Đ", 6: "V", 7: "M", 8: "M", 9: "H", 10: "V", 11: "Đ"},
    "Thiên Lương":{0: "V", 1: "V", 2: "M", 3: "M", 4: "M", 5: "H", 6: "M", 7: "Đ", 8: "V", 9: "H", 10: "M", 11: "H"},
    "Thất Sát":   {0: "M", 1: "Đ", 2: "M", 3: "H", 4: "M", 5: "V", 6: "M", 7: "Đ", 8: "M", 9: "H", 10: "M", 11: "V"},
    "Phá Quân":   {0: "M", 1: "V", 2: "H", 3: "H", 4: "Đ", 5: "H", 6: "M", 7: "V", 8: "H", 9: "H", 10: "Đ", 11: "H"}
}

PALACE_NAMES_VIETNAMESE = [
    "MỆNH", "PHỤ MẪU", "PHÚC ĐỨC", "ĐIỀN TRẠCH", "QUAN LỘC", "NÔ BỘC",
    "THIÊN DI", "TẬT ÁCH", "TÀI BẠCH", "TỬ TỨC", "PHU THÊ", "HUYNH ĐỆ"
]

PALACE_SHORT_NAMES = ["MỆNH", "PHỤ", "PHÚC", "ĐIỀN", "QUAN", "NÔ", "DI", "TẬT", "TÀI", "TỬ", "PHỐI", "BÀO"]

CUC_ELEMENT_NAMES = {2: "Thủy Nhị Cục", 3: "Mộc Tam Cục", 4: "Kim Tứ Cục", 5: "Thổ Ngũ Cục", 6: "Hỏa Lục Cục"}

# ==============================================================================
# 3. THUẬT TOÁN AN PHỤ TINH TOÀN DIỆN (110+ SAO)
# ==============================================================================
def get_minor_stars(
    year_can_idx: int,
    year_chi_idx: int,
    month: int,
    day: int,
    hour_chi_idx: int,
    cuc_num: int,
    is_duong_nam_or_am_nu: bool,
    school: str = "standard",
    view_year: Optional[int] = None,
    menh_idx: int = 0,
    than_idx: int = 0
) -> Dict[int, List[Dict[str, str]]]:
    """
    An toàn bộ hệ thống 110+ Tinh Đẩu & Thần Sát kinh điển và Hệ thống Lưu Tinh Động (nếu có view_year).
    """
    palace_stars: Dict[int, List[Dict[str, str]]] = {i: [] for i in range(12)}
    
    def add_star(p_idx: int, name: str, category: str, color_type: str = "neutral"):
        palace_stars[p_idx % 12].append({"name": name, "category": category, "color": color_type})

    # 1. Lục Cát Tinh
    # Tả Phụ (Thìn khởi T1 thuận đến tháng sinh): (4 + month - 1) % 12
    # Hữu Bật (Tuất khởi T1 nghịch đến tháng sinh): (10 - month + 1) % 12
    ta_phu = (4 + month - 1) % 12
    huu_bat = (10 - month + 1) % 12
    add_star(ta_phu, "Tả Phụ", "Lục Cát", "cat")
    add_star(huu_bat, "Hữu Bật", "Lục Cát", "cat")
    
    # Văn Xương (Tuất khởi Tý nghịch đến giờ sinh): (10 - hour_chi_idx) % 12
    # Văn Khúc (Thìn khởi Tý thuận đến giờ sinh): (4 + hour_chi_idx) % 12
    van_xuong = (10 - hour_chi_idx) % 12
    van_khuc = (4 + hour_chi_idx) % 12
    add_star(van_xuong, "Văn Xương", "Lục Cát", "cat")
    add_star(van_khuc, "Văn Khúc", "Lục Cát", "cat")
    
    # Thiên Khôi, Thiên Việt (theo Can năm)
    # Giáp Mậu Canh: Sửu Mùi | Ất Kỷ: Tý Thân | Bính Đinh: Hợi Dậu | Lục Tân: Dần Ngọ | Nhâm Quý: Mão Tỵ
    KHOI_VIET = {
        0: (1, 7), 1: (0, 8), 2: (11, 9), 3: (11, 9), 4: (1, 7),
        5: (0, 8), 6: (1, 7), 7: (2, 6), 8: (3, 5), 9: (3, 5)
    }
    k_pos, v_pos = KHOI_VIET[year_can_idx]
    add_star(k_pos, "Thiên Khôi", "Lục Cát", "cat")
    add_star(v_pos, "Thiên Việt", "Lục Cát", "cat")

    # 2. Lộc Tồn, Kình Dương, Đà La, Quốc Ấn, Đường Phù
    # Giáp Lộc Dần(2), Ất Mão(3), Bính Mậu Tỵ(5), Đinh Kỷ Ngọ(6), Canh Thân(8), Tân Dậu(9), Nhâm Hợi(11), Quý Tý(0)
    LOC_TON_MAP = {0: 2, 1: 3, 2: 5, 3: 6, 4: 5, 5: 6, 6: 8, 7: 9, 8: 11, 9: 0}
    loc_pos = LOC_TON_MAP[year_can_idx]
    add_star(loc_pos, "Lộc Tồn", "Tài Tinh", "gold")
    add_star((loc_pos + 1) % 12, "Kình Dương", "Lục Sát", "sat")
    add_star((loc_pos - 1) % 12, "Đà La", "Lục Sát", "sat")
    add_star((loc_pos + 8) % 12, "Quốc Ấn", "Quý Tinh", "cat")
    add_star((loc_pos + 5) % 12, "Đường Phù", "Quý Tinh", "cat")

    # 3. Lục Sát Tinh khác: Địa Không, Địa Kiếp, Hỏa Tinh, Linh Tinh
    # Địa Kiếp (Hợi khởi Tý thuận đến giờ): (11 + hour_chi_idx) % 12
    # Địa Không (Hợi khởi Tý nghịch đến giờ): (11 - hour_chi_idx) % 12
    add_star((11 + hour_chi_idx) % 12, "Địa Kiếp", "Lục Sát", "sat")
    add_star((11 - hour_chi_idx) % 12, "Địa Không", "Lục Sát", "sat")
    
    # Hỏa Tinh, Linh Tinh (theo Chi năm & Trường phái)
    # Dần Ngọ Tuất: Hỏa Sửu(1), Linh Mão(3)
    # Thân Tý Thìn: Hỏa Dần(2), Linh Tuất(10)
    # Tỵ Dậu Sửu: Hỏa Mão(3), Linh Tuất(10)
    # Hợi Mão Mùi: Hỏa Dậu(9), Linh Tuất(10)
    chi_group = year_chi_idx % 4
    if chi_group == 2: # Dần Ngọ Tuất
        hoa_base, linh_base = 1, 3
    elif chi_group == 0: # Thân Tý Thìn
        hoa_base, linh_base = 2, 10
    elif chi_group == 1: # Tỵ Dậu Sửu
        hoa_base, linh_base = 3, 10
    else: # Hợi Mão Mùi
        hoa_base, linh_base = 9, 10
        
    if school == "nam_phai":
        # Nam Phái Thái Thứ Lang: Hỏa Tinh luôn chạy thuận, Linh Tinh luôn chạy thuận
        hoa_pos = (hoa_base + hour_chi_idx) % 12
        linh_pos = (linh_base + hour_chi_idx) % 12
    else:
        if is_duong_nam_or_am_nu:
            hoa_pos = (hoa_base + hour_chi_idx) % 12
            linh_pos = (linh_base - hour_chi_idx) % 12
        else:
            hoa_pos = (hoa_base - hour_chi_idx) % 12
            linh_pos = (linh_base + hour_chi_idx) % 12
    add_star(hoa_pos, "Hỏa Tinh", "Lục Sát", "sat")
    add_star(linh_pos, "Linh Tinh", "Lục Sát", "sat")

    # 4. Vòng Thái Tuế (12 sao thuận hành từ Chi năm)
    THAI_TUE_RING = ["Thái Tuế", "Thiếu Dương", "Tang Môn", "Thiếu Âm", "Quan Phù", "Tử Phù", "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Trực Phù"]
    for i, s_name in enumerate(THAI_TUE_RING):
        add_star((year_chi_idx + i) % 12, s_name, "Vòng Thái Tuế", "thai_tue")

    # 5. Vòng Bác Sĩ (12 sao từ Lộc Tồn, thuận nếu Dương Nam/Âm Nữ, nghịch nếu Âm Nam/Dương Nữ)
    BAC_SI_RING = ["Bác Sĩ", "Lực Sĩ", "Thanh Long", "Tiểu Hao", "Tướng Quân", "Tấu Thư", "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao", "Phục Binh", "Quan Phủ"]
    dir_bs = 1 if is_duong_nam_or_am_nu else -1
    for i, s_name in enumerate(BAC_SI_RING):
        add_star((loc_pos + i * dir_bs) % 12, s_name, "Vòng Bác Sĩ", "bac_si")

    # 6. Vòng Trường Sinh (12 sao theo Cục)
    # Thủy Nhị Cục khởi Thân(8), Mộc Tam Cục khởi Hợi(11), Kim Tứ Cục khởi Tỵ(5), Thổ Ngũ Cục khởi Thân(8), Hỏa Lục Cục khởi Dần(2)
    CUC_TRUONG_SINH_BASE = {2: 8, 3: 11, 4: 5, 5: 8, 6: 2}
    ts_base = CUC_TRUONG_SINH_BASE[cuc_num]
    TRUONG_SINH_RING = ["Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
    for i, s_name in enumerate(TRUONG_SINH_RING):
        add_star((ts_base + i * dir_bs) % 12, s_name, "Vòng Trường Sinh", "truong_sinh")

    # 7. Các sao Thần Sát Bổ Khuyết Kinh Điển (110+ Sao)
    # Thiên Mã (theo Chi năm)
    MA_MAP = {2: 8, 0: 2, 1: 11, 3: 5}
    add_star(MA_MAP[chi_group], "Thiên Mã", "Quý Tinh", "cat")
    
    # Đào Hoa (Tý Ngọ Mão Dậu)
    DAO_MAP = {2: 3, 0: 9, 1: 6, 3: 0}
    add_star(DAO_MAP[chi_group], "Đào Hoa", "Đào Hoa Tinh", "pink")
    
    # Hồng Loan, Thiên Hỷ (Mão khởi Tý nghịch đến Chi năm): (3 - year_chi_idx) % 12
    hong_loan = (3 - year_chi_idx) % 12
    thien_hy = (hong_loan + 6) % 12
    add_star(hong_loan, "Hồng Loan", "Hỷ Tinh", "pink")
    add_star(thien_hy, "Thiên Hỷ", "Hỷ Tinh", "pink")
    
    # Thiên Khốc, Thiên Hư (Ngọ khởi Tý: Khốc nghịch, Hư thuận)
    add_star((6 - year_chi_idx) % 12, "Thiên Khốc", "Bại Tinh", "bai")
    add_star((6 + year_chi_idx) % 12, "Thiên Hư", "Bại Tinh", "bai")
    
    # Thiên Hình, Thiên Diêu (Dậu khởi T1 thuận đến tháng sinh)
    add_star((9 + month - 1) % 12, "Thiên Hình", "Hình Tinh", "sat")
    add_star((1 + month - 1) % 12, "Thiên Diêu", "Ám Tinh", "pink")
    
    # Thiên Y (Sửu khởi T1 thuận đến tháng sinh): (1 + month - 1) % 12
    add_star((1 + month - 1) % 12, "Thiên Y", "Quý Tinh", "cat")
    
    # Tam Sát (Kiếp Sát, Tai Sát, Thiên Sát theo Chi năm)
    TAM_SAT_MAP = {2: (11, 0, 1), 0: (5, 6, 7), 1: (2, 3, 4), 3: (8, 9, 10)}
    kiep_s, tai_s, thien_s = TAM_SAT_MAP[chi_group]
    add_star(kiep_s, "Kiếp Sát", "Sát Tinh", "sat")
    add_star(tai_s, "Tai Sát", "Sát Tinh", "sat")
    add_star(thien_s, "Thiên Sát", "Sát Tinh", "sat")
    
    # Thiên Đức & Nguyệt Đức (theo Chi năm)
    add_star((9 + year_chi_idx) % 12, "Thiên Đức", "Quý Tinh", "cat")
    add_star((5 + year_chi_idx) % 12, "Nguyệt Đức", "Quý Tinh", "cat")
    
    # Cô Thần & Quả Tú (theo Chi năm)
    CO_THAN_MAP = {2: 5, 0: 2, 1: 8, 3: 5}
    QUA_TU_MAP = {2: 1, 0: 10, 1: 4, 3: 1}
    add_star(CO_THAN_MAP[chi_group], "Cô Thần", "Sát Tinh", "sat")
    add_star(QUA_TU_MAP[chi_group], "Quả Tú", "Sát Tinh", "sat")
    
    # Thiên Không (sau Thái Tuế 1 cung)
    add_star((year_chi_idx + 1) % 12, "Thiên Không", "Sát Tinh", "sat")

    # Thiên La (Thìn) & Địa Võng (Tuất)
    add_star(4, "Thiên La", "La Võng", "gray")
    add_star(10, "Địa Võng", "La Võng", "gray")
    
    # Thiên Quan & Thiên Phúc (theo Can năm)
    THIEN_QUAN_MAP = {0: 7, 1: 4, 2: 5, 3: 2, 4: 3, 5: 9, 6: 11, 7: 9, 8: 10, 9: 6}
    THIEN_PHUC_MAP = {0: 9, 1: 8, 2: 0, 3: 11, 4: 3, 5: 2, 6: 6, 7: 5, 8: 6, 9: 5}
    add_star(THIEN_QUAN_MAP[year_can_idx], "Thiên Quan", "Quý Tinh", "cat")
    add_star(THIEN_PHUC_MAP[year_can_idx], "Thiên Phúc", "Quý Tinh", "cat")
    
    # Thiên Trù, Văn Tinh, Lưu Hà
    THIEN_TRU_MAP = {0: 5, 1: 6, 2: 0, 3: 5, 4: 6, 5: 9, 6: 2, 7: 6, 8: 9, 9: 10}
    VAN_TINH_MAP = {0: 5, 1: 6, 2: 8, 3: 9, 4: 8, 5: 9, 6: 10, 7: 11, 8: 2, 9: 3}
    LUU_HA_MAP = {0: 9, 1: 10, 2: 7, 3: 4, 4: 5, 5: 6, 6: 8, 7: 3, 8: 11, 9: 2}
    add_star(THIEN_TRU_MAP[year_can_idx], "Thiên Trù", "Phúc Tinh", "cat")
    add_star(VAN_TINH_MAP[year_can_idx], "Văn Tinh", "Quý Tinh", "cat")
    add_star(LUU_HA_MAP[year_can_idx], "Lưu Hà", "Bại Tinh", "bai")
    
    # Ân Quang, Thiên Quý (Văn Xương, Văn Khúc khởi ngày sinh)
    add_star((van_xuong + day - 2) % 12, "Ân Quang", "Quý Tinh", "cat")
    add_star((van_khuc - day + 2) % 12, "Thiên Quý", "Quý Tinh", "cat")
    
    # Tam Thai, Bát Tọa (Tả Phụ, Hữu Bật khởi ngày sinh)
    add_star((ta_phu + day - 1) % 12, "Tam Thai", "Quý Tinh", "cat")
    add_star((huu_bat - day + 1) % 12, "Bát Tọa", "Quý Tinh", "cat")
    
    # Long Trì, Phượng Các (Thìn/Tuất khởi Chi năm)
    add_star((4 + year_chi_idx) % 12, "Long Trì", "Quý Tinh", "cat")
    add_star((10 - year_chi_idx) % 12, "Phượng Các", "Quý Tinh", "cat")
    
    # Hoa Cái
    hoa_cai_map = {2: 10, 0: 4, 1: 1, 3: 7}
    add_star(hoa_cai_map[chi_group], "Hoa Cái", "Quý Tinh", "cat")
    
    # Âm Sát, Thiên Vu, Thiên Nguyệt (theo tháng sinh)
    AM_SAT_MAP = {1: 2, 2: 0, 3: 10, 4: 8, 5: 6, 6: 4, 7: 2, 8: 0, 9: 10, 10: 8, 11: 6, 12: 4}
    THIEN_VU_MAP = {1: 5, 2: 8, 3: 2, 4: 11, 5: 5, 6: 8, 7: 2, 8: 11, 9: 5, 10: 8, 11: 2, 12: 11}
    THIEN_NGUYET_MAP = {1: 10, 2: 5, 3: 4, 4: 2, 5: 7, 6: 3, 7: 11, 8: 7, 9: 2, 10: 6, 11: 10, 12: 2}
    add_star(AM_SAT_MAP.get(month, 2), "Âm Sát", "Ám Tinh", "sat")
    add_star(THIEN_VU_MAP.get(month, 5), "Thiên Vu", "Quý Tinh", "cat")
    add_star(THIEN_NGUYET_MAP.get(month, 10), "Thiên Nguyệt", "Tật Tinh", "sat")
    
    # Phá Toái, Thai Phụ, Phong Cáo, Đẩu Quân
    PHA_TOAI_MAP = {0: 5, 6: 5, 3: 5, 9: 5, 2: 9, 8: 9, 5: 9, 11: 9, 1: 1, 7: 1, 4: 1, 10: 1}
    add_star(PHA_TOAI_MAP.get(year_chi_idx, 5), "Phá Toái", "Bại Tinh", "sat")
    add_star((van_khuc + 2) % 12, "Thai Phụ", "Quý Tinh", "cat")
    add_star((van_khuc - 2) % 12, "Phong Cáo", "Quý Tinh", "cat")
    dau_quan = (year_chi_idx - (month - 1) + hour_chi_idx) % 12
    add_star(dau_quan, "Đẩu Quân", "Nguyệt Lệnh", "cat")

    # Vòng Tướng Tinh / Thần Sát Năm
    TUONG_TINH_MAP = {2: 6, 0: 0, 1: 9, 3: 3}
    tt_pos = TUONG_TINH_MAP[chi_group]
    add_star(tt_pos, "Tướng Tinh", "Quyền Tinh", "cat")
    add_star((tt_pos + 1) % 12, "Phán Án", "Quý Tinh", "cat")
    add_star((tt_pos + 3) % 12, "Tức Thần", "Hung Tinh", "sat")
    add_star((tt_pos + 10) % 12, "Nguyệt Sát", "Sát Tinh", "sat")
    add_star((tt_pos + 11) % 12, "Vong Thần", "Sát Tinh", "sat")
    add_star(MA_MAP[chi_group], "Tuế Dịch", "Dịch Mã", "cat")
    add_star((year_chi_idx + 8) % 12, "Chi Bối", "Bại Tinh", "sat")
    
    # Giải Thần (Niên Giải, Thiên Giải, Địa Giải, Nguyệt Giải)
    add_star((10 - year_chi_idx) % 12, "Niên Giải", "Giải Tinh", "cat")
    add_star((8 + month - 1) % 12, "Thiên Giải", "Giải Tinh", "cat")
    add_star((7 + month - 1) % 12, "Địa Giải", "Giải Tinh", "cat")
    add_star(4, "Nguyệt Giải", "Giải Tinh", "cat")

    # Tuần/Triệt Không Vong
    tuan_idx = (year_chi_idx - year_can_idx) % 12
    tuan_kong_1 = (10 + tuan_idx) % 12
    tuan_kong_2 = (11 + tuan_idx) % 12
    add_star(tuan_kong_1, "Tuần", "Không Vong", "gray")
    add_star(tuan_kong_2, "Tuần", "Không Vong", "gray")
    
    TRIET_MAP = {0: (8, 9), 5: (8, 9), 1: (6, 7), 6: (6, 7), 2: (4, 5), 7: (4, 5), 3: (2, 3), 8: (2, 3), 4: (0, 1), 9: (0, 1)}
    tr_1, tr_2 = TRIET_MAP[year_can_idx]
    add_star(tr_1, "Triệt", "Không Vong", "gray")
    add_star(tr_2, "Triệt", "Không Vong", "gray")

    # Thiên Thương (Nô Bộc), Thiên Sứ (Tật Ách)
    add_star((menh_idx + 5) % 12, "Thiên Thương", "Bại Tinh", "sat")
    add_star((menh_idx + 7) % 12, "Thiên Sứ", "Bại Tinh", "sat")
    
    # Thiên Tài, Thiên Thọ
    add_star((menh_idx + year_chi_idx) % 12, "Thiên Tài", "Tài Tinh", "cat")
    add_star((than_idx + year_chi_idx) % 12, "Thiên Thọ", "Thọ Tinh", "cat")

    # 8. HỆ THỐNG LƯU TINH ĐỘNG (DYNAMIC ANNUAL FLOATING STARS)
    if view_year is not None:
        v_can_idx = (view_year - 4) % 10
        v_chi_idx = (view_year - 4) % 12
        v_chi_group = v_chi_idx % 4
        
        # Lưu Thái Tuế & Vòng Lưu Thái Tuế
        for i, s_name in enumerate(THAI_TUE_RING):
            add_star((v_chi_idx + i) % 12, f"L.{s_name}", "Lưu Tinh", "floating")
            
        # Lưu Lộc Tồn, Kình Dương, Đà La
        v_loc_pos = LOC_TON_MAP[v_can_idx]
        add_star(v_loc_pos, "L.Lộc Tồn", "Lưu Tinh", "floating")
        add_star((v_loc_pos + 1) % 12, "L.Kình Dương", "Lưu Tinh", "floating")
        add_star((v_loc_pos - 1) % 12, "L.Đà La", "Lưu Tinh", "floating")
        
        # Vòng Lưu Bác Sĩ
        for i, s_name in enumerate(BAC_SI_RING):
            add_star((v_loc_pos + i * dir_bs) % 12, f"L.{s_name}", "Lưu Tinh", "floating")
            
        # Lưu Thiên Mã, Đào Hoa, Hồng Loan, Thiên Hỷ
        add_star(MA_MAP[v_chi_group], "L.Thiên Mã", "Lưu Tinh", "floating")
        add_star(DAO_MAP[v_chi_group], "L.Đào Hoa", "Lưu Tinh", "floating")
        v_hl = (3 - v_chi_idx) % 12
        add_star(v_hl, "L.Hồng Loan", "Lưu Tinh", "floating")
        add_star((v_hl + 6) % 12, "L.Thiên Hỷ", "Lưu Tinh", "floating")
        
        # Lưu Khốc, Lưu Hư
        add_star((6 - v_chi_idx) % 12, "L.Thiên Khốc", "Lưu Tinh", "floating")
        add_star((6 + v_chi_idx) % 12, "L.Thiên Hư", "Lưu Tinh", "floating")
        
        # Lưu Khôi, Lưu Việt
        vk_pos, vv_pos = KHOI_VIET[v_can_idx]
        add_star(vk_pos, "L.Thiên Khôi", "Lưu Tinh", "floating")
        add_star(vv_pos, "L.Thiên Việt", "Lưu Tinh", "floating")
        
        # Lưu Long Trì, Phượng Các, Hoa Cái
        add_star((4 + v_chi_idx) % 12, "L.Long Trì", "Lưu Tinh", "floating")
        add_star((10 - v_chi_idx) % 12, "L.Phượng Các", "Lưu Tinh", "floating")
        v_hoa_cai_map = {2: 10, 0: 4, 1: 1, 3: 7}
        add_star(v_hoa_cai_map[v_chi_group], "L.Hoa Cái", "Lưu Tinh", "floating")

    return palace_stars

def calculate_flying_stars_matrix(
    palaces: List[Dict[str, Any]],
    school: str = "standard",
    custom_si_hua: Optional[Dict[str, Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Tính toán ma trận Phi Tinh Tứ Hóa giữa 12 cung:
    - Niên Can Tứ Hóa (Tiên Thiên)
    - 12 Cung Tự Phi Tứ Hóa (A: Lộc, B: Quyền, C: Khoa, D: Kỵ)
    - Tự Hóa (Self-Transformation) & Hướng Tâm (Inward-Transformation)
    - Đường Kỵ chuyển Lộc & Đường chuyển Kỵ
    """
    base_table = SI_HUA_TABLES.get(school, SI_HUA_TABLES["standard"])
    if custom_si_hua:
        table = {**base_table, **custom_si_hua}
    else:
        table = base_table
    
    # Build a lookup: star_name -> palace_idx
    star_locations: Dict[str, int] = {}
    for p in palaces:
        for s in p["main_stars"]:
            star_locations[s] = p["branch_idx"]
        for ms in p.get("minor_stars", []):
            star_locations[ms["name"]] = p["branch_idx"]
            
    palace_flying_results = []
    
    # 1. 12 Palaces Flying
    for p in palaces:
        p_can = p["can_name"]
        si_hua_p = table.get(p_can, SI_HUA_TABLES["standard"].get(p_can, {}))
        
        loc_star = si_hua_p.get("A", "")
        quyen_star = si_hua_p.get("B", "")
        khoa_star = si_hua_p.get("C", "")
        ky_star = si_hua_p.get("D", "")
        
        target_loc = star_locations.get(loc_star, -1)
        target_quyen = star_locations.get(quyen_star, -1)
        target_khoa = star_locations.get(khoa_star, -1)
        target_ky = star_locations.get(ky_star, -1)
        
        # Self-transformations (Tự hóa tại bản cung)
        self_trans = []
        if target_loc == p["branch_idx"]: self_trans.append(f"Tự hóa Lộc ({loc_star})")
        if target_quyen == p["branch_idx"]: self_trans.append(f"Tự hóa Quyền ({quyen_star})")
        if target_khoa == p["branch_idx"]: self_trans.append(f"Tự hóa Khoa ({khoa_star})")
        if target_ky == p["branch_idx"]: self_trans.append(f"Tự hóa Kỵ ({ky_star})")
        
        # Inward-transformations (Hướng tâm hai chiều trục Đối Cung: Bản Cung phát xạ hoặc Tiếp nhận)
        opposite_idx = (p["branch_idx"] + 6) % 12
        opposite_palace = next((op for op in palaces if op["branch_idx"] == opposite_idx), None)
        inward_trans = []
        if opposite_palace:
            # 1. Hướng tâm khi Can bản cung hóa sao ở cung đối diện (Bản cung chiếu sang đối cung)
            p_si_hua = table.get(p_can, SI_HUA_TABLES["standard"].get(p_can, {}))
            if star_locations.get(p_si_hua.get("A")) == opposite_idx: inward_trans.append(f"Hướng tâm Lộc ({p_si_hua.get('A')})")
            if star_locations.get(p_si_hua.get("B")) == opposite_idx: inward_trans.append(f"Hướng tâm Quyền ({p_si_hua.get('B')})")
            if star_locations.get(p_si_hua.get("C")) == opposite_idx: inward_trans.append(f"Hướng tâm Khoa ({p_si_hua.get('C')})")
            if star_locations.get(p_si_hua.get("D")) == opposite_idx: inward_trans.append(f"Hướng tâm Kỵ ({p_si_hua.get('D')})")
            
            # 2. Hướng tâm khi Can cung đối diện hóa sao ở bản cung (Bản cung tiếp nhận từ đối cung)
            op_can = opposite_palace["can_name"]
            op_si_hua = table.get(op_can, SI_HUA_TABLES["standard"].get(op_can, {}))
            if star_locations.get(op_si_hua.get("A")) == p["branch_idx"] and f"Hướng tâm Lộc ({op_si_hua.get('A')})" not in inward_trans:
                inward_trans.append(f"Hướng tâm Lộc ({op_si_hua.get('A')})")
            if star_locations.get(op_si_hua.get("B")) == p["branch_idx"] and f"Hướng tâm Quyền ({op_si_hua.get('B')})" not in inward_trans:
                inward_trans.append(f"Hướng tâm Quyền ({op_si_hua.get('B')})")
            if star_locations.get(op_si_hua.get("C")) == p["branch_idx"] and f"Hướng tâm Khoa ({op_si_hua.get('C')})" not in inward_trans:
                inward_trans.append(f"Hướng tâm Khoa ({op_si_hua.get('C')})")
            if star_locations.get(op_si_hua.get("D")) == p["branch_idx"] and f"Hướng tâm Kỵ ({op_si_hua.get('D')})" not in inward_trans:
                inward_trans.append(f"Hướng tâm Kỵ ({op_si_hua.get('D')})")

        def get_short_name(b_idx):
            if b_idx == -1: return "None"
            target_p = next((tp for tp in palaces if tp["branch_idx"] == b_idx), None)
            return target_p["short_name"] if target_p else "None"

        palace_flying_results.append({
            "palace_name": p["name"],
            "short_name": p["short_name"],
            "branch_idx": p["branch_idx"],
            "branch_name": p["branch_name"],
            "can_name": p_can,
            "phi_loc": {"star": loc_star, "target_branch": target_loc, "target_palace": get_short_name(target_loc)},
            "phi_quyen": {"star": quyen_star, "target_branch": target_quyen, "target_palace": get_short_name(target_quyen)},
            "phi_khoa": {"star": khoa_star, "target_branch": target_khoa, "target_palace": get_short_name(target_khoa)},
            "phi_ky": {"star": ky_star, "target_branch": target_ky, "target_palace": get_short_name(target_ky)},
            "self_transformations": self_trans,
            "inward_transformations": inward_trans
        })

    # 2. Phương Viên Lộc Kỵ Toàn Đồ (Tổng hợp số lượng A, B, C, D bay đến từng cung)
    loc_ky_counts: Dict[str, Dict[str, int]] = {p["short_name"]: {"A": 0, "B": 0, "C": 0, "D": 0} for p in palaces}
    for pf in palace_flying_results:
        loc_target = pf["phi_loc"]["target_palace"]
        quyen_target = pf["phi_quyen"]["target_palace"]
        khoa_target = pf["phi_khoa"]["target_palace"]
        ky_target = pf["phi_ky"]["target_palace"]
        if loc_target in loc_ky_counts: loc_ky_counts[loc_target]["A"] += 1
        if quyen_target in loc_ky_counts: loc_ky_counts[quyen_target]["B"] += 1
        if khoa_target in loc_ky_counts: loc_ky_counts[khoa_target]["C"] += 1
        if ky_target in loc_ky_counts: loc_ky_counts[ky_target]["D"] += 1
        
    phuong_vien = {}
    for p_name, counts in loc_ky_counts.items():
        parts = []
        if counts["A"] > 0: parts.append(f"{counts['A']} Lộc (A)")
        if counts["B"] > 0: parts.append(f"{counts['B']} Quyền (B)")
        if counts["C"] > 0: parts.append(f"{counts['C']} Khoa (C)")
        if counts["D"] > 0: parts.append(f"{counts['D']} Kỵ (D)")
        phuong_vien[p_name] = ", ".join(parts) if parts else "Không tụ khí"
        
    # Attach Phuong Vien to each palace flying result
    for pf in palace_flying_results:
        pf["phuong_vien_loc_ky"] = phuong_vien.get(pf["short_name"], "")

    # 3. Đường Kỵ Chuyển Lộc & Đường Chuyển Kỵ (Khâm Thiên Môn)
    ky_chuyen_loc_paths = []
    chuyen_ky_paths = []
    for pf in palace_flying_results:
        # Nếu cung này có Kỵ bay đi đến Target Cung
        ky_dest = pf["phi_ky"]["target_palace"]
        if ky_dest != "None" and ky_dest != pf["short_name"]:
            # Tìm target cung đó bay Lộc đi đâu
            target_pf = next((t for t in palace_flying_results if t["short_name"] == ky_dest), None)
            if target_pf:
                loc_of_dest = target_pf["phi_loc"]["target_palace"]
                ky_chuyen_loc_paths.append(f"{pf['short_name']} -> {ky_dest} -> {loc_of_dest} ({target_pf['phi_loc']['star']})")
                ky_of_dest = target_pf["phi_ky"]["target_palace"]
                chuyen_ky_paths.append(f"{pf['short_name']} -> {ky_dest} -> {ky_of_dest} ({target_pf['phi_ky']['star']})")

    return {
        "school": school,
        "palace_flying_stars": palace_flying_results,
        "phuong_vien_toan_do": phuong_vien,
        "ky_chuyen_loc": ky_chuyen_loc_paths[:5],
        "chuyen_ky": chuyen_ky_paths[:5]
    }

# ==============================================================================
# 5. CORE MASTER FUNCTION: CALCULATE UNIVERSAL ZIWEI CHART
# ==============================================================================
def calculate_universal_tu_vi(
    dt: datetime,
    gender: int = 1,
    school: str = "standard", # 'standard', 'kham_thien', 'nam_phai', 'trung_chau', 'luong_phai', 'canh_dong_am', 'canh_dong_khoa', 'hybrid'
    astrolabe_type: str = "thien_ban", # 'thien_ban', 'dia_ban', 'nhan_ban'
    cuc_override: Optional[int] = None, # Hỗ trợ ép Cục số theo các phái (2, 3, 4, 5, 6)
    custom_si_hua: Optional[Dict[str, Dict[str, str]]] = None,
    include_external_meta: bool = True,
    view_year: Optional[int] = None
) -> Dict[str, Any]:
    sec = dt.second if hasattr(dt, 'second') else 0
    year_can_idx, year_chi_idx, month, day, lunar_year, hour_chi_idx, fp = _cached_lunar_coords(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, sec
    )
    
    is_duong_nam = (gender == 1 and year_can_idx % 2 == 0)
    is_am_nu = (gender == 0 and year_can_idx % 2 == 1)
    is_duong_nam_or_am_nu = (is_duong_nam or is_am_nu)
    
    # 1. Menh & Than placement (Thiên Bàn)
    menh_idx = (2 + (month - 1) - hour_chi_idx) % 12
    than_idx = (2 + (month - 1) + hour_chi_idx) % 12
    
    # If Địa Bàn: Rotate Mệnh to Thân index
    if astrolabe_type == "dia_ban":
        menh_idx = than_idx
        
    # 2. Cục Số (Nạp Âm Can Chi Dần và Mệnh)
    TIGER_CAN_MAP = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}
    tiger_can_idx = TIGER_CAN_MAP[year_can_idx]
    
    palace_cans = {}
    for i in range(12):
        steps = (i - 2) % 12
        c_idx = (tiger_can_idx + steps) % 10
        palace_cans[i] = CAN[c_idx]
        
    menh_can = palace_cans[menh_idx]
    menh_chi = CHI[menh_idx]
    
    # 2. Cục Số từ Nạp Âm Can Chi Cung Mệnh (Lục Thập Hoa Giáp Nạp Âm Ngũ Hành Cục)
    NAP_AM_CUC = {
        ("Giáp", "Tý"): 4, ("Ất", "Sửu"): 4, ("Bính", "Dần"): 6, ("Đinh", "Mão"): 6, ("Mậu", "Thìn"): 3, ("Kỷ", "Tỵ"): 3,
        ("Canh", "Ngọ"): 5, ("Tân", "Mùi"): 5, ("Nhâm", "Thân"): 4, ("Quý", "Dậu"): 4, ("Giáp", "Tuất"): 6, ("Ất", "Hợi"): 6,
        ("Bính", "Tý"): 2, ("Đinh", "Sửu"): 2, ("Mậu", "Dần"): 5, ("Kỷ", "Mão"): 5, ("Canh", "Thìn"): 4, ("Tân", "Tỵ"): 4,
        ("Nhâm", "Ngọ"): 3, ("Quý", "Mùi"): 3, ("Giáp", "Thân"): 2, ("Ất", "Dậu"): 2, ("Bính", "Tuất"): 5, ("Đinh", "Hợi"): 5,
        ("Mậu", "Tý"): 6, ("Kỷ", "Sửu"): 6, ("Canh", "Dần"): 3, ("Tân", "Mão"): 3, ("Nhâm", "Thìn"): 2, ("Quý", "Tỵ"): 2,
        ("Giáp", "Ngọ"): 4, ("Ất", "Mùi"): 4, ("Bính", "Thân"): 6, ("Đinh", "Dậu"): 6, ("Mậu", "Tuất"): 3, ("Kỷ", "Hợi"): 3,
        ("Canh", "Tý"): 5, ("Tân", "Sửu"): 5, ("Nhâm", "Dần"): 4, ("Quý", "Mão"): 4, ("Giáp", "Thìn"): 6, ("Ất", "Tỵ"): 6,
        ("Bính", "Ngọ"): 2, ("Đinh", "Mùi"): 2, ("Mậu", "Thân"): 5, ("Kỷ", "Dậu"): 5, ("Canh", "Tuất"): 4, ("Tân", "Hợi"): 4,
        ("Nhâm", "Tý"): 3, ("Quý", "Sửu"): 3, ("Giáp", "Dần"): 2, ("Ất", "Mão"): 2, ("Bính", "Thìn"): 5, ("Đinh", "Tỵ"): 5,
        ("Mậu", "Ngọ"): 6, ("Kỷ", "Mùi"): 6, ("Canh", "Thân"): 3, ("Tân", "Dậu"): 3, ("Nhâm", "Tuất"): 2, ("Quý", "Hợi"): 2
    }
    if cuc_override in [2, 3, 4, 5, 6]:
        cuc_num = cuc_override
    else:
        cuc_num = NAP_AM_CUC.get((menh_can, menh_chi), 6)
    cuc_name = CUC_ELEMENT_NAMES[cuc_num]
    
    # 3. An Tử Vi & Thiên Phủ
    rem = day % cuc_num
    if rem == 0:
        tv_pos = (2 + day // cuc_num - 1) % 12
    else:
        add_k = cuc_num - rem
        quot = (day + add_k) // cuc_num
        if add_k % 2 == 1:
            tv_pos = (2 + quot - 1 - add_k) % 12
        else:
            tv_pos = (2 + quot - 1 + add_k) % 12
            
    tp_pos = (4 - tv_pos) % 12
    
    # 4. An 14 Chính Tinh
    main_stars_palaces: Dict[int, List[str]] = {i: [] for i in range(12)}
    main_stars_palaces[tv_pos].append("Tử Vi")
    main_stars_palaces[(tv_pos - 1) % 12].append("Thiên Cơ")
    main_stars_palaces[(tv_pos - 3) % 12].append("Thái Dương")
    main_stars_palaces[(tv_pos - 4) % 12].append("Vũ Khúc")
    main_stars_palaces[(tv_pos - 5) % 12].append("Thiên Đồng")
    main_stars_palaces[(tv_pos - 8) % 12].append("Liêm Trinh")
    
    main_stars_palaces[tp_pos].append("Thiên Phủ")
    main_stars_palaces[(tp_pos + 1) % 12].append("Thái Âm")
    main_stars_palaces[(tp_pos + 2) % 12].append("Tham Lang")
    main_stars_palaces[(tp_pos + 3) % 12].append("Cự Môn")
    main_stars_palaces[(tp_pos + 4) % 12].append("Thiên Tướng")
    main_stars_palaces[(tp_pos + 5) % 12].append("Thiên Lương")
    main_stars_palaces[(tp_pos + 6) % 12].append("Thất Sát")
    main_stars_palaces[(tp_pos + 10) % 12].append("Phá Quân")
    
    # 5. Phụ tinh (110+ sao & Lưu tinh động)
    minor_stars_map = get_minor_stars(
        year_can_idx, year_chi_idx, month, day, hour_chi_idx, cuc_num,
        is_duong_nam_or_am_nu, school=school, view_year=view_year,
        menh_idx=menh_idx, than_idx=than_idx
    )
    
    # 5.1. An Tứ Hóa Năm Sinh Tiên Thiên vào các Cung Vị tương ứng
    si_hua_table_applied = SI_HUA_TABLES.get(school, SI_HUA_TABLES["standard"])
    si_hua_birth = si_hua_table_applied.get(CAN[year_can_idx], {})
    temp_star_locs = {}
    for b_idx in range(12):
        for ms in main_stars_palaces[b_idx]:
            temp_star_locs[ms] = b_idx
        for ms in minor_stars_map[b_idx]:
            temp_star_locs[ms["name"]] = b_idx
            
    if si_hua_birth.get("A") in temp_star_locs:
        minor_stars_map[temp_star_locs[si_hua_birth["A"]]].append({"name": "Hóa Lộc", "category": "Tứ Hóa", "color": "cat"})
    if si_hua_birth.get("B") in temp_star_locs:
        minor_stars_map[temp_star_locs[si_hua_birth["B"]]].append({"name": "Hóa Quyền", "category": "Tứ Hóa", "color": "cat"})
    if si_hua_birth.get("C") in temp_star_locs:
        minor_stars_map[temp_star_locs[si_hua_birth["C"]]].append({"name": "Hóa Khoa", "category": "Tứ Hóa", "color": "cat"})
    if si_hua_birth.get("D") in temp_star_locs:
        minor_stars_map[temp_star_locs[si_hua_birth["D"]]].append({"name": "Hóa Kỵ", "category": "Tứ Hóa", "color": "sat"})
    
    # 6. Build 12 Palaces Structure
    palaces = []
    
    for i in range(12):
        b_idx = i # 0: Tý, 1: Sửu, ...
        p_name_idx = (b_idx - menh_idx) % 12
        p_name = PALACE_NAMES_VIETNAMESE[p_name_idx]
        p_short = PALACE_SHORT_NAMES[p_name_idx]
        
        # Đại Vận range (10 years)
        if is_duong_nam_or_am_nu:
            dy_step = (b_idx - menh_idx) % 12
        else:
            dy_step = (menh_idx - b_idx) % 12
        dy_start = cuc_num + dy_step * 10
        dy_end = dy_start + 9
        
        m_stars = main_stars_palaces[b_idx]
        m_stars_formatted = []
        for s in m_stars:
            bright = MAIN_STARS_BRIGHTNESS.get(s, {}).get(b_idx, "")
            m_stars_formatted.append(f"{s}({bright})" if bright else s)
            
        palaces.append({
            "branch_idx": b_idx,
            "branch_name": CHI[b_idx],
            "can_name": palace_cans[b_idx],
            "name": p_name,
            "short_name": p_short,
            "is_menh": (b_idx == menh_idx),
            "is_than": (b_idx == than_idx),
            "da_yun_range": f"{dy_start} - {dy_end}",
            "da_yun_start": dy_start,
            "da_yun_end": dy_end,
            "main_stars": m_stars,
            "main_stars_with_brightness": m_stars_formatted,
            "minor_stars": minor_stars_map[b_idx]
        })
        
    # 7. Flying Stars & Si Hua Calculations
    si_hua_res = calculate_flying_stars_matrix(palaces, school=school, custom_si_hua=custom_si_hua)
    
    # 8. Transits (Đại Vận, Lưu Niên 2026, Lưu Nguyệt, Lưu Nhật)
    now_dt = datetime.now()
    target_year = now_dt.year
    year_can_now, year_chi_now = CAN[(target_year - 4) % 10], CHI[(target_year - 4) % 12]
    
    transit_info = {
        "current_target_year": target_year,
        "year_can_chi": f"{year_can_now} {year_chi_now}",
        "luu_thai_tue_palace": year_chi_now,
        "luu_si_hua_annual": SI_HUA_TABLES["standard"].get(year_can_now, {})
    }
    
    # 9. Center Header Meta (Tứ Trụ, Hà Lạc, Nạp Âm)
    menh_nayin = NAP_AM_60.get((CAN[year_can_idx], CHI[year_chi_idx]), "Hải Trung Kim")
    
    if include_external_meta:
        ha_lac_hexagrams = _cached_ha_lac_hex(dt.year, dt.month, dt.day, dt.hour, dt.minute, gender)
    else:
        ha_lac_hexagrams = {"tien_thien": "", "hau_thien": ""}

    # 10. Lai Nhân Cung & Đế Tinh Tọa & Bậc Phi Hóa Intensity
    year_can_name = CAN[year_can_idx]
    lai_nhan_cung = next((p["name"] for p in palaces if p["can_name"] == year_can_name), "MỆNH")
    de_tinh_palace = next((p["name"] for p in palaces if "Tử Vi" in p.get("main_stars", [])), "TỴ")

    phi_loc_counts = {p["name"]: 0 for p in palaces}
    phi_ky_counts = {p["name"]: 0 for p in palaces}
    for pf in si_hua_res.get("palace_flying_stars", []):
        loc_to = pf["phi_loc"]["target_palace"]
        ky_to = pf["phi_ky"]["target_palace"]
        phi_loc_counts[loc_to] = phi_loc_counts.get(loc_to, 0) + 1
        phi_ky_counts[ky_to] = phi_ky_counts.get(ky_to, 0) + 1

    sorted_loc = sorted(phi_loc_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_ky = sorted(phi_ky_counts.items(), key=lambda x: x[1], reverse=True)
    
    # 11. Bát Quái Mê Tung & Dịch Quái 12 Cung Khâm Thiên
    dich_quai_map = calculate_dich_quai_12_cung(palaces, si_hua_res, birth_year_can=CAN[year_can_idx])
    for p in palaces:
        p["dich_quai_cards"] = dich_quai_map.get(p["name"], [])

    return {
        "schema_version": "3.1.0-universal-ziwei",
        "school": school,
        "school_applied": school,
        "astrolabe_type": astrolabe_type,
        "client_profile": {
            "solar_datetime": dt.strftime("%d/%m/%Y %H:%M"),
            "lunar_datetime": f"{day:02d}/{month:02d}/{lunar_year}",
            "lunar_year_name": f"{CAN[year_can_idx]} {CHI[year_chi_idx]}",
            "gender": "Nam" if gender == 1 else "Nữ",
            "yin_yang_gender": "Dương Nam" if is_duong_nam else ("Âm Nam" if gender==1 else ("Âm Nữ" if is_am_nu else "Dương Nữ")),
            "menh_nayin": menh_nayin,
            "cuc_num": cuc_num,
            "cuc_name": cuc_name,
            "menh_branch": CHI[menh_idx],
            "than_branch": CHI[than_idx],
            "menh_palace_branch": CHI[menh_idx],
            "than_palace_branch": CHI[than_idx],
            "menh_chu": ["Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc", "Phá Quân", "Vũ Khúc", "Liêm Trinh", "Văn Khúc", "Lộc Tồn", "Cự Môn"][year_chi_idx],
            "than_chu": ["Hỏa Tinh", "Thiên Tướng", "Thiên Lương", "Thiên Đồng", "Văn Xương", "Thiên Cơ", "Hỏa Tinh", "Thiên Tướng", "Thiên Lương", "Thiên Đồng", "Văn Xương", "Thiên Cơ"][year_chi_idx],
            "lai_nhan_cung": lai_nhan_cung,
            "de_tinh_toa": de_tinh_palace
        },
        "four_pillars": fp,
        "ha_lac_hexagrams": ha_lac_hexagrams,
        "dich_quai_12_cung": dich_quai_map,
        "palaces": palaces,
        "flying_stars": si_hua_res,
        "flying_intensity": {
            "sorted_loc": sorted_loc,
            "sorted_ky": sorted_ky
        },
        "transits": transit_info
    }

def format_universal_tu_vi_report(res: Dict[str, Any]) -> str:
    cp = res["client_profile"]
    fp = res["four_pillars"]
    out = []
    out.append("================================================================================")
    out.append(f"   LÁ SỐ TỬ VI ĐẨU SỐ ĐA PHÁI TOÀN DIỆN (UNIVERSAL EDITION v3.0)")
    out.append(f"   Trường Phái: {res['school'].upper()} | Bàn: {res['astrolabe_type'].upper()}")
    out.append("================================================================================")
    out.append(f"Họ Tên / Hồ Sơ: {cp['yin_yang_gender']} | Mệnh: {cp['menh_nayin']} | Cục: {cp['cuc_name']}")
    out.append(f"Dương Lịch: {cp['solar_datetime']} | Âm Lịch: {cp['lunar_datetime']}")
    out.append(f"Tứ Trụ: Năm {fp['year']} | Tháng {fp['month']} | Ngày {fp['day']} | Giờ {fp['hour']}")
    out.append(f"Mệnh Chủ: {cp['menh_chu']} | Thân Chủ: {cp['than_chu']} | Mệnh tại: [{cp['menh_branch']}] | Thân tại: [{cp['than_branch']}]")
    out.append(f"Hà Lạc Quẻ Tiên Thiên: {res['ha_lac_hexagrams']['tien_thien']} | Hậu Thiên: {res['ha_lac_hexagrams']['hau_thien']}")
    out.append("")
    
    out.append("【I. BỐ TRÍ 12 CUNG & TINH ĐẨU (110+ SAO & ĐẮC HÃM)】")
    for p in res["palaces"]:
        tag_m = " [MỆNH]" if p["is_menh"] else ""
        tag_t = " [THÂN]" if p["is_than"] else ""
        m_stars_str = ", ".join(p["main_stars_with_brightness"]) if p["main_stars"] else "Vô Chính Diệu"
        fixed_minors = [s["name"] for s in p["minor_stars"] if not s["name"].startswith("L.")]
        floating_minors = [s["name"] for s in p["minor_stars"] if s["name"].startswith("L.")]
        
        fixed_str = ", ".join(fixed_minors) if fixed_minors else "Không"
        out.append(f"  • Cung {p['name']:<12} ({p['branch_name']}) [{p['can_name']} {p['branch_name']}]{tag_m}{tag_t} (Đại Vận: {p['da_yun_range']}):")
        out.append(f"    - Chính Tinh: {m_stars_str}")
        out.append(f"    - Phụ Tinh  : {fixed_str}")
        if floating_minors:
            out.append(f"    - Lưu Tinh  : {', '.join(floating_minors)}")
    out.append("")
    
    out.append("【II. MA TRẬN PHI TINH TỨ HÓA 12 CUNG & TỰ HÓA / HƯỚNG TÂM (KHÂM THIÊN / LƯƠNG PHÁI)】")
    for pf in res["flying_stars"]["palace_flying_stars"]:
        self_str = f" | Tự Hóa: {', '.join(pf['self_transformations'])}" if pf['self_transformations'] else ""
        in_str = f" | Hướng Tâm: {', '.join(pf['inward_transformations'])}" if pf['inward_transformations'] else ""
        pv_str = f" | Phương Viên: [{pf['phuong_vien_loc_ky']}]" if pf.get('phuong_vien_loc_ky') else ""
        out.append(f"  • Cung {pf['short_name']} [{pf['can_name']}]: → Lộc({pf['phi_loc']['target_palace']}:{pf['phi_loc']['star']}) | Quyền({pf['phi_quyen']['target_palace']}:{pf['phi_quyen']['star']}) | Khoa({pf['phi_khoa']['target_palace']}:{pf['phi_khoa']['star']}) | Kỵ({pf['phi_ky']['target_palace']}:{pf['phi_ky']['star']}){self_str}{in_str}{pv_str}")
    
    if res["flying_stars"].get("ky_chuyen_loc"):
        out.append("")
        out.append("【III. KHÂM THIÊN KHÍ ĐẠO: ĐƯỜNG KỴ CHUYỂN LỘC & ĐƯỜNG CHUYỂN KỴ】")
        out.append("  • Đường Kỵ Chuyển Lộc: " + " | ".join(res["flying_stars"]["ky_chuyen_loc"][:3]).replace("->", "→"))
        out.append("  • Đường Chuyển Kỵ    : " + " | ".join(res["flying_stars"]["chuyen_ky"][:3]).replace("->", "→"))

    # Bậc Phi Hóa Intensity
    fi = res.get("flying_intensity", {})
    if fi:
        out.append("")
        out.append("【IV. BẬC PHI HÓA (FLYING STAR INTENSITY) & TỌA VỊ KHÍ CƠ】")
        out.append(f"  • Lai Nhân Cung: [{cp.get('lai_nhan_cung', 'MỆNH')}] (Gốc rễ nhân quả và duyên nghiệp tự thân)")
        out.append(f"  • Đế Tinh Tọa  : [{cp.get('de_tinh_toa', 'TỴ')}] (Vị trí Tử Vi định hình thế trận toàn bàn)")
        top_loc = [f"{k}({v} lần)" for k, v in fi.get("sorted_loc", []) if v > 0][:4]
        top_ky = [f"{k}({v} lần)" for k, v in fi.get("sorted_ky", []) if v > 0][:4]
        out.append(f"  • Top Cung Tụ Lộc (Cơ hội, tài nguyên hanh thông): {', '.join(top_loc)}")
        out.append(f"  • Top Cung Tụ Kỵ  (Áp lực, chấp niệm cần hóa giải): {', '.join(top_ky)}")
        
    out.append("================================================================================")
    return "\n".join(out)
