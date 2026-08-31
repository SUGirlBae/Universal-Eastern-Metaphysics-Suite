"""
Unified Lunar-Solar Calendar & Can Chi Module
Powered by production-grade lunar-python engine with Sino-Vietnamese mappings.
"""
from datetime import datetime, timezone, timedelta

LOCAL_TZ = timezone(timedelta(hours=7))

# Sino-Vietnamese Mappings
HAN_VIET_MAP = {
    # Can
    "甲": "Giáp", "乙": "Ất", "丙": "Bính", "丁": "Đinh", "戊": "Mậu",
    "己": "Kỷ", "庚": "Canh", "辛": "Tân", "壬": "Nhâm", "癸": "Quý",
    # Chi
    "子": "Tý", "丑": "Sửu", "寅": "Dần", "卯": "Mão", "辰": "Thìn", "巳": "Tỵ",
    "午": "Ngọ", "未": "Mùi", "申": "Thân", "酉": "Dậu", "戌": "Tuất", "亥": "Hợi",
    # Tiết Khí
    "春分": "Xuân Phân", "清明": "Thanh Minh", "谷雨": "Cốc Vũ", "立夏": "Lập Hạ",
    "小满": "Tiểu Mãn", "芒种": "Mang Chủng", "夏至": "Hạ Chí", "小暑": "Tiểu Thử",
    "大暑": "Đại Thử", "立秋": "Lập Thu", "处暑": "Xử Thử", "白露": "Bạch Lộ",
    "秋分": "Thu Phân", "寒露": "Hàn Lộ", "霜降": "Sương Giáng", "立冬": "Lập Đông",
    "小雪": "Tiểu Tuyết", "大雪": "Đại Tuyết", "冬至": "Đông Chí", "小寒": "Tiểu Hàn",
    "大寒": "Đại Hàn", "立春": "Lập Xuân", "雨水": "Vũ Thủy", "惊蛰": "Kinh Trập"
}

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

CHI_ELEMENT = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"
}

def translate_han_viet(text):
    if not text:
        return ""
    if text in HAN_VIET_MAP:
        return HAN_VIET_MAP[text]
    # Translate char by char (e.g. "甲子" -> "Giáp Tý")
    res = []
    for char in text:
        res.append(HAN_VIET_MAP.get(char, char))
    return " ".join(res)


NAP_AM_60_HOA_GIAP = {
    "Giáp Tý": "Hải Trung Kim", "Ất Sửu": "Hải Trung Kim", "Bính Dần": "Lư Trung Hỏa", "Đinh Mão": "Lư Trung Hỏa",
    "Mậu Thìn": "Đại Lâm Mộc", "Kỷ Tỵ": "Đại Lâm Mộc", "Canh Ngọ": "Lộ Bàng Thổ", "Tân Mùi": "Lộ Bàng Thổ",
    "Nhâm Thân": "Kiếm Phong Kim", "Quý Dậu": "Kiếm Phong Kim", "Giáp Tuất": "Sơn Đầu Hỏa", "Ất Hợi": "Sơn Đầu Hỏa",
    "Bính Tý": "Giản Hạ Thủy", "Đinh Sửu": "Giản Hạ Thủy", "Mậu Dần": "Thành Đầu Thổ", "Kỷ Mão": "Thành Đầu Thổ",
    "Canh Thìn": "Bạch Lạp Kim", "Tân Tỵ": "Bạch Lạp Kim", "Nhâm Ngọ": "Dương Liễu Mộc", "Quý Mùi": "Dương Liễu Mộc",
    "Giáp Thân": "Tuyền Trung Thủy", "Ất Dậu": "Tuyền Trung Thủy", "Bính Tuất": "Ốc Thượng Thổ", "Đinh Hợi": "Ốc Thượng Thổ",
    "Mậu Tý": "Tích Lịch Hỏa", "Kỷ Sửu": "Tích Lịch Hỏa", "Canh Dần": "Tùng Bách Mộc", "Tân Mão": "Tùng Bách Mộc",
    "Nhâm Thìn": "Trường Lưu Thủy", "Quý Tỵ": "Trường Lưu Thủy", "Giáp Ngọ": "Sa Trung Kim", "Ất Mùi": "Sa Trung Kim",
    "Bính Thân": "Sơn Hạ Hỏa", "Đinh Dậu": "Sơn Hạ Hỏa", "Mậu Tuất": "Bình Địa Mộc", "Kỷ Hợi": "Bình Địa Mộc",
    "Canh Tý": "Bích Thượng Thổ", "Tân Sửu": "Bích Thượng Thổ", "Nhâm Dần": "Kim Bạch Kim", "Quý Mão": "Kim Bạch Kim",
    "Giáp Thìn": "Phú Đăng Hỏa", "Ất Tỵ": "Phú Đăng Hỏa", "Bính Ngọ": "Thiên Hà Thủy", "Đinh Mùi": "Thiên Hà Thủy",
    "Mậu Thân": "Đại Trạch Thổ", "Kỷ Dậu": "Đại Trạch Thổ", "Canh Tuất": "Thoa Xuyến Kim", "Tân Hợi": "Thoa Xuyến Kim",
    "Nhâm Tý": "Tang Đố Mộc", "Quý Sửu": "Tang Đố Mộc", "Giáp Dần": "Đại Khê Thủy", "Ất Mão": "Đại Khê Thủy",
    "Bính Thìn": "Sa Trung Thổ", "Đinh Tỵ": "Sa Trung Thổ", "Mậu Ngọ": "Thiên Thượng Hỏa", "Kỷ Mùi": "Thiên Thượng Hỏa",
    "Canh Thân": "Thạch Lựu Mộc", "Tân Dậu": "Thạch Lựu Mộc", "Nhâm Tuất": "Đại Hải Thủy", "Quý Hợi": "Đại Hải Thủy"
}

def get_nap_am(can_chi: str) -> str:
    return NAP_AM_60_HOA_GIAP.get(can_chi.strip(), "Ngũ Hành Khí")

def calculate_time_coordinates(dt: datetime, manual_lunar=None):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    else:
        dt = dt.astimezone(LOCAL_TZ)
        
    s_day = dt.day
    s_month = dt.month
    s_year = dt.year
    s_hour = dt.hour
    s_minute = dt.minute
    
    try:
        from lunar_python import Solar
        solar = Solar.fromYmdHms(s_year, s_month, s_day, s_hour, s_minute, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        
        l_day = lunar.getDay()
        l_month = abs(lunar.getMonth())
        l_year = lunar.getYear()
        is_leap = lunar.getMonth() < 0
        
        # Tiết khí hiện tại
        jieqi = lunar.getPrevJieQi(True)
        tiet_khi = translate_han_viet(jieqi.getName()) if jieqi else "Xử Thử"
        
        can_chi_year = translate_han_viet(eight_char.getYear())
        can_chi_month = translate_han_viet(eight_char.getMonth())
        can_chi_day = translate_han_viet(eight_char.getDay())
        can_chi_hour = translate_han_viet(eight_char.getTime())
        
    except ImportError:
        # Fallback to local astronomical engine
        from hond_calendar import convertSolar2Lunar, getSolarTerm
        l_day, l_month, l_year, is_leap = convertSolar2Lunar(s_day, s_month, s_year)
        tiet_khi = getSolarTerm(s_day, s_month, s_year)
        
        year_can_idx = (l_year + 6) % 10
        can_chi_year = f"{CAN[year_can_idx]} {CHI[(l_year + 8) % 12]}"
        start_can = (year_can_idx * 2 + 2) % 10
        can_chi_month = f"{CAN[(start_can + (l_month - 1)) % 10]} {CHI[(l_month + 1) % 12]}"
        
        # Day Can Chi via JDN
        from hond_calendar import jdFromDate
        jdn = jdFromDate(s_day, s_month, s_year)
        day_can_idx = int((jdn + 9.5) % 10)
        can_chi_day = f"{CAN[day_can_idx]} {CHI[int((jdn + 1.5) % 12)]}"
        
        hour_chi_idx = int((s_hour + 1) // 2) % 12
        can_chi_hour = f"{CAN[((day_can_idx * 2) + hour_chi_idx) % 10]} {CHI[hour_chi_idx]}"
        
    year_can = can_chi_year.split()[0]
    year_chi = can_chi_year.split()[1]
    month_can = can_chi_month.split()[0]
    month_chi = can_chi_month.split()[1]
    day_can = can_chi_day.split()[0]
    day_chi = can_chi_day.split()[1]
    hour_can = can_chi_hour.split()[0]
    hour_chi = can_chi_hour.split()[1]
    
    return {
        "solar": f"{s_day:02d}/{s_month:02d}/{s_year} {s_hour:02d}:{s_minute:02d}",
        "solar_day": s_day,
        "solar_month": s_month,
        "solar_year": s_year,
        "solar_hour": s_hour,
        "solar_minute": s_minute,
        "lunar": f"{l_day:02d}/{l_month:02d}/{l_year}{' (Nhuận)' if is_leap else ''}",
        "lunar_day": l_day,
        "lunar_month": l_month,
        "lunar_year": l_year,
        "is_leap": is_leap,
        "tiet_khi": tiet_khi,
        "can_chi_year": can_chi_year,
        "nap_am_year": get_nap_am(can_chi_year),
        "can_chi_month": can_chi_month,
        "nap_am_month": get_nap_am(can_chi_month),
        "can_chi_day": can_chi_day,
        "nap_am_day": get_nap_am(can_chi_day),
        "can_chi_hour": can_chi_hour,
        "nap_am_hour": get_nap_am(can_chi_hour),
        "year_can": year_can,
        "year_chi": year_chi,
        "month_can": month_can,
        "month_chi": month_chi,
        "month_elem": CHI_ELEMENT[month_chi],
        "day_can": day_can,
        "day_chi": day_chi,
        "day_elem": CHI_ELEMENT[day_chi],
        "hour_can": hour_can,
        "hour_chi": hour_chi
    }
# ==============================================================================
# TỌA ĐỘ ĐỊA LÝ & GIỜ MẶT TRỜI THỰC (TRUE SOLAR TIME)
# ==============================================================================
LOCATION_LONGITUDE_MAP = {
    "hà nội": 105.85, "ha noi": 105.85, "hanoi": 105.85,
    "tp.hồ chí minh": 106.66, "hồ chí minh": 106.66, "ho chi minh": 106.66, "sài gòn": 106.66, "sai gon": 106.66, "tphcm": 106.66, "hcm": 106.66,
    "đà nẵng": 108.20, "da nang": 108.20, "danang": 108.20,
    "hải phòng": 106.68, "hai phong": 106.68,
    "cần thơ": 105.78, "can tho": 105.78,
    "bạc liêu": 105.72, "bac lieu": 105.72,
    "huế": 107.59, "hue": 107.59, "thừa thiên huế": 107.59,
    "nha trang": 109.19, "khánh hòa": 109.19,
    "vũng tàu": 107.08, "bà rịa - vũng tàu": 107.08,
    "quy nhơn": 109.22, "bình định": 109.22,
    "buôn ma thuột": 108.04, "đắk lắk": 108.04,
    "đà lạt": 108.44, "lâm đồng": 108.44,
    "nam định": 106.17, "thái bình": 106.33, "hải dương": 106.32,
    "nghệ an": 105.68, "vinh": 105.68, "thanh hóa": 105.78,
    "quảng ninh": 107.07, "hạ long": 107.07,
    "cà mau": 105.15, "kiên giang": 105.08, "phú quốc": 103.96,
    "an giang": 105.12, "đồng tháp": 105.63, "vĩnh long": 105.97,
    "bến tre": 106.38, "tiền giang": 106.36, "long an": 106.41,
    "bắc ninh": 106.07, "bắc giang": 106.20, "vĩnh phúc": 105.60,
    "phú thọ": 105.22, "thái nguyên": 105.84, "lạng sơn": 106.76,
    "hà giang": 104.98, "lào cai": 103.97, "yên bái": 104.87,
    "sơn la": 103.91, "điện biên": 103.02, "lai châu": 103.46, "hòa bình": 105.34
}

def get_longitude_by_location(location: str) -> float:
    """Trả về kinh độ địa lý chuẩn của địa điểm (mặc định 105.0 cho múi giờ UTC+7)."""
    if not location:
        return 105.0
    loc_clean = location.strip().lower()
    for name, lng in LOCATION_LONGITUDE_MAP.items():
        if name in loc_clean:
            return lng
    return 105.0

def calculate_true_solar_time(dt: datetime, longitude: float = 105.0, standard_meridian: float = 105.0) -> datetime:
    """
    Tính Giờ Mặt Trời Thực (True Solar Time / Local Apparent Solar Time).
    Phương trình thời gian (Equation of Time - EOT) + Chênh lệch kinh độ (Longitude Offset).
    Delta = 4 phút / 1 độ kinh độ chênh lệch + EOT.
    """
    import math
    
    # 1. Day of year (N)
    day_of_year = dt.timetuple().tm_yday
    
    # 2. Equation of Time (EOT) approximation in minutes
    # B = 360 * (N - 81) / 365 in degrees
    b_rad = math.radians(360.0 * (day_of_year - 81) / 365.0)
    eot_minutes = 9.87 * math.sin(2 * b_rad) - 7.53 * math.cos(b_rad) - 1.5 * math.sin(b_rad)
    
    # 3. Longitude Correction: 4 minutes per degree difference from standard meridian
    long_corr_minutes = 4.0 * (longitude - standard_meridian)
    
    # 4. Total correction
    total_delta_minutes = long_corr_minutes + eot_minutes
    
    return dt + timedelta(minutes=total_delta_minutes)
