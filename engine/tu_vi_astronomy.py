"""
Astronomy & Calendar Module for Tu Vi Occult Engine
Calculates True Solar Time (Chân Thái Dương Thời), Longitude offsets, Equation of Time (EoT),
Lunar-Solar Coordinates, 60 Sexagenary Cycle (Lục Thập Hoa Giáp) & Na Yin (Nạp Âm).
"""
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple

LOCAL_TZ = timezone(timedelta(hours=7))

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# 30 Nạp Âm Lục Thập Hoa Giáp
NA_YIN_MAP = {
    "Giáp Tý": "Hải Trung Kim", "Ất Sửu": "Hải Trung Kim",
    "Bính Dần": "Lư Trung Hỏa", "Đinh Mão": "Lư Trung Hỏa",
    "Mậu Thìn": "Đại Lâm Mộc", "Kỷ Tỵ": "Đại Lâm Mộc",
    "Canh Ngọ": "Lộ Bàng Thổ", "Tân Mùi": "Lộ Bàng Thổ",
    "Nhâm Thân": "Kiếm Phong Kim", "Quý Dậu": "Kiếm Phong Kim",
    "Giáp Tuất": "Sơn Đầu Hỏa", "Ất Hợi": "Sơn Đầu Hỏa",
    "Bính Tý": "Giản Hạ Thủy", "Đinh Sửu": "Giản Hạ Thủy",
    "Mậu Dần": "Thành Đầu Thổ", "Kỷ Mão": "Thành Đầu Thổ",
    "Canh Thìn": "Bạch Lạp Kim", "Tân Tỵ": "Bạch Lạp Kim",
    "Nhâm Ngọ": "Dương Liễu Mộc", "Quý Mùi": "Dương Liễu Mộc",
    "Giáp Thân": "Tuyền Trung Thủy", "Ất Dậu": "Tuyền Trung Thủy",
    "Bính Tuất": "Ốc Thượng Thổ", "Đinh Hợi": "Ốc Thượng Thổ",
    "Mậu Tý": "Tích Lịch Hỏa", "Kỷ Sửu": "Tích Lịch Hỏa",
    "Canh Dần": "Tùng Bách Mộc", "Tân Mão": "Tùng Bách Mộc",
    "Nhâm Thìn": "Trường Lưu Thủy", "Quý Tỵ": "Trường Lưu Thủy",
    "Giáp Ngọ": "Sa Trung Kim", "Ất Mùi": "Sa Trung Kim",
    "Bính Thân": "Sơn Hạ Hỏa", "Đinh Dậu": "Sơn Hạ Hỏa",
    "Mậu Tuất": "Bình Địa Mộc", "Kỷ Hợi": "Bình Địa Mộc",
    "Canh Tý": "Bích Thượng Thổ", "Tân Sửu": "Bích Thượng Thổ",
    "Nhâm Dần": "Kim Bạch Kim", "Quý Mão": "Kim Bạch Kim",
    "Giáp Thìn": "Phúc Đăng Hỏa", "Ất Tỵ": "Phúc Đăng Hỏa",
    "Bính Ngọ": "Thiên Hà Thủy", "Đinh Mùi": "Thiên Hà Thủy",
    "Mậu Thân": "Đại Dịch Thổ", "Kỷ Dậu": "Đại Trạch Thổ",
    "Canh Tuất": "Thoa Xuyến Kim", "Tân Hợi": "Thoa Xuyến Kim",
    "Nhâm Tý": "Tang Đố Mộc", "Quý Sửu": "Tang Đố Mộc",
    "Giáp Dần": "Đại Khê Thủy", "Ất Mão": "Đại Khê Thủy",
    "Bính Thìn": "Sa Trung Thổ", "Đinh Tỵ": "Sa Trung Thổ",
    "Mậu Ngọ": "Thiên Thượng Hỏa", "Kỷ Mùi": "Thiên Thượng Hỏa",
    "Canh Thân": "Thạch Lựu Mộc", "Tân Dậu": "Thạch Lựu Mộc",
    "Nhâm Tuất": "Đại Hải Thủy", "Quý Hợi": "Đại Hải Thủy"
}

HAN_VIET_MAP = {
    "甲": "Giáp", "乙": "Ất", "丙": "Bính", "丁": "Đinh", "戊": "Mậu",
    "己": "Kỷ", "庚": "Canh", "辛": "Tân", "壬": "Nhâm", "癸": "Quý",
    "子": "Tý", "丑": "Sửu", "寅": "Dần", "卯": "Mão", "辰": "Thìn", "巳": "Tỵ",
    "午": "Ngọ", "未": "Mùi", "申": "Thân", "酉": "Dậu", "戌": "Tuất", "亥": "Hợi"
}

def translate_han_viet(text: str) -> str:
    res = []
    for char in text:
        translated = HAN_VIET_MAP.get(char, char)
        res.append(translated)
    return " ".join(res).strip()

def calculate_equation_of_time(day_of_year: int) -> float:
    """Calculates the Equation of Time (in minutes) for a given day of the year."""
    b = (360.0 / 365.0) * (day_of_year - 81)
    b_rad = math.radians(b)
    eot = 9.87 * math.sin(2 * b_rad) - 7.53 * math.cos(b_rad) - 1.5 * math.sin(b_rad)
    return eot

def calculate_true_solar_time(dt: datetime, longitude: float = 105.720, standard_meridian: float = 105.0) -> Tuple[datetime, float]:
    """
    Calculates True Solar Time (Chân Thái Dương Thời) given Civil Time and Longitude.
    Returns (solar_datetime, total_offset_minutes).
    """
    day_of_year = dt.timetuple().tm_yday
    eot_minutes = calculate_equation_of_time(day_of_year)
    lon_offset_minutes = (longitude - standard_meridian) * 4.0
    total_offset_minutes = lon_offset_minutes + eot_minutes
    solar_dt = dt + timedelta(minutes=total_offset_minutes)
    return solar_dt, total_offset_minutes

def get_hour_branch_index(hour: int, minute: int) -> int:
    """
    Maps hour (0-23) and minute to 12 Chi indices (0=Tý, 1=Sửu, ..., 11=Hợi).
    23:00 - 00:59 -> Tý (0)
    01:00 - 02:59 -> Sửu (1)
    ...
    """
    total_minutes = hour * 60 + minute
    if total_minutes >= 23 * 60 or total_minutes < 1 * 60:
        return 0 # Tý
    return (total_minutes + 60) // 120

def get_hour_can_chi(day_can: str, hour_branch_idx: int) -> str:
    """Calculates Can Chi of the hour given the Day Can and Hour Branch Index."""
    # Khởi giờ Tý theo Can Ngày (Ngũ Thử Độn Giáp)
    # Giáp Kỷ -> Giáp Tý (0)
    # Ất Canh -> Bính Tý (2)
    # Bính Tân -> Mậu Tý (4)
    # Đinh Nhâm -> Canh Tý (6)
    # Mậu Quý -> Nhâm Tý (8)
    day_can_idx = CAN.index(day_can)
    start_can_idx = (day_can_idx % 5) * 2
    hour_can = CAN[(start_can_idx + hour_branch_idx) % 10]
    hour_chi = CHI[hour_branch_idx]
    return f"{hour_can} {hour_chi}"

def get_astronomical_profile(dt: datetime, longitude: float = 105.720, use_solar_time: bool = True) -> Dict[str, Any]:
    from lunar_python import Solar
    
    if use_solar_time:
        solar_dt, offset = calculate_true_solar_time(dt, longitude)
    else:
        solar_dt, offset = dt, 0.0
        
    s = Solar.fromYmdHms(solar_dt.year, solar_dt.month, solar_dt.day, solar_dt.hour, solar_dt.minute, solar_dt.second)
    l = s.getLunar()
    
    y_gz = translate_han_viet(l.getYearInGanZhi())
    m_gz = translate_han_viet(l.getMonthInGanZhi())
    d_gz = translate_han_viet(l.getDayInGanZhi())
    
    # Hour Chi and Can calculation
    h_idx = get_hour_branch_index(solar_dt.hour, solar_dt.minute)
    day_can = d_gz.split()[0]
    h_gz = get_hour_can_chi(day_can, h_idx)
    
    l_day = l.getDay()
    l_month = l.getMonth()
    l_year = l.getYear()
    is_leap = l_month < 0
    l_month_abs = abs(l_month)
    
    return {
        "civil_time": dt.strftime("%d/%m/%Y %H:%M:%S"),
        "solar_time": solar_dt.strftime("%d/%m/%Y %H:%M:%S"),
        "longitude": longitude,
        "offset_minutes": round(offset, 2),
        "lunar_day": l_day,
        "lunar_month": l_month_abs,
        "lunar_year": l_year,
        "is_leap_month": is_leap,
        "year_can_chi": y_gz,
        "month_can_chi": m_gz,
        "day_can_chi": d_gz,
        "hour_can_chi": h_gz,
        "hour_chi_idx": h_idx,
        "na_yin_year": NA_YIN_MAP.get(y_gz, ""),
        "na_yin_month": NA_YIN_MAP.get(m_gz, ""),
        "na_yin_day": NA_YIN_MAP.get(d_gz, ""),
        "na_yin_hour": NA_YIN_MAP.get(h_gz, ""),
        "solar_object": s,
        "lunar_object": l
    }
