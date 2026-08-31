"""
Stars Placement Module for Tu Vi Occult Engine
High-precision placement of 14 Main Stars (Chính Tinh), 6 Auspicious (Lục Cát), 6 Inauspicious (Lục Sát),
Tràng Sinh Ring, Thái Tuế Ring, Bác Sĩ Ring, and All Auxiliary Stars.
"""
from typing import Dict, Any, List, Tuple
try:
    from .tu_vi_astronomy import CAN, CHI
    from .tu_vi_cuc_so import PALACE_NAMES
except (ImportError, ValueError):
    from tu_vi_astronomy import CAN, CHI
    from tu_vi_cuc_so import PALACE_NAMES

# 14 Chính Tinh
MAIN_STARS = [
    "Tử Vi", "Thiên Cơ", "Thái Dương", "Vũ Khúc", "Thiên Đồng", "Liêm Trinh",
    "Thiên Phủ", "Thái Âm", "Tham Lang", "Cự Môn", "Thiên Tướng", "Thiên Lương", "Thất Sát", "Phá Quân"
]

# Miếu Vượng Đắc Bình Hãm Matrix (14 Stars across 12 Branches 0=Tý ... 11=Hợi)
STAR_BRIGHTNESS = {
    "Tử Vi": ["B", "Đ", "M", "B", "V", "M", "M", "Đ", "M", "B", "V", "B"],
    "Thiên Cơ": ["M", "H", "Đ", "V", "B", "B", "M", "H", "Đ", "V", "B", "B"],
    "Thái Dương": ["H", "H", "V", "V", "V", "M", "M", "Đ", "B", "H", "H", "H"],
    "Vũ Khúc": ["V", "M", "B", "Đ", "V", "B", "V", "M", "B", "Đ", "V", "B"],
    "Thiên Đồng": ["V", "H", "M", "B", "H", "Đ", "H", "H", "M", "B", "H", "Đ"],
    "Liêm Trinh": ["V", "Đ", "M", "B", "B", "H", "V", "Đ", "M", "B", "B", "H"],
    "Thiên Phủ": ["M", "M", "M", "B", "M", "Đ", "V", "Đ", "M", "B", "M", "Đ"],
    "Thái Âm": ["M", "M", "H", "H", "H", "H", "H", "H", "Đ", "V", "M", "M"],
    "Tham Lang": ["H", "M", "B", "Đ", "H", "H", "H", "M", "B", "Đ", "H", "H"],
    "Cự Môn": ["V", "H", "M", "M", "H", "H", "V", "H", "M", "M", "H", "Đ"],
    "Thiên Tướng": ["M", "M", "M", "H", "V", "Đ", "V", "Đ", "M", "H", "V", "Đ"],
    "Thiên Lương": ["M", "V", "M", "M", "V", "H", "M", "V", "H", "H", "V", "H"],
    "Thất Sát": ["M", "M", "M", "H", "H", "V", "M", "M", "M", "H", "H", "V"],
    "Phá Quân": ["M", "V", "H", "H", "Đ", "H", "M", "V", "H", "H", "Đ", "H"]
}

def place_tu_vi(lunar_day: int, cuc_num: int) -> int:
    d = lunar_day
    c = cuc_num
    if d % c == 0:
        q = d // c
        return (2 + q - 1) % 12
    else:
        x = c - (d % c)
        q = (d + x) // c
        base_pos = (2 + q - 1) % 12
        if x % 2 == 1:
            return (base_pos - x) % 12
        else:
            return (base_pos + x) % 12

def place_14_main_stars(tu_vi_pos: int) -> Dict[str, int]:
    stars = {}
    
    # Tử Vi Tinh Hệ (Counter-clockwise / Lùi)
    stars["Tử Vi"] = tu_vi_pos
    stars["Thiên Cơ"] = (tu_vi_pos - 1) % 12
    stars["Thái Dương"] = (tu_vi_pos - 3) % 12
    stars["Vũ Khúc"] = (tu_vi_pos - 4) % 12
    stars["Thiên Đồng"] = (tu_vi_pos - 5) % 12
    stars["Liêm Trinh"] = (tu_vi_pos - 8) % 12
    
    # Thiên Phủ Tinh Hệ (Symmetric across Dần - Thân: sum = 4 mod 12)
    thien_phu_pos = (4 - tu_vi_pos) % 12
    stars["Thiên Phủ"] = thien_phu_pos
    stars["Thái Âm"] = (thien_phu_pos + 1) % 12
    stars["Tham Lang"] = (thien_phu_pos + 2) % 12
    stars["Cự Môn"] = (thien_phu_pos + 3) % 12
    stars["Thiên Tướng"] = (thien_phu_pos + 4) % 12
    stars["Thiên Lương"] = (thien_phu_pos + 5) % 12
    stars["Thất Sát"] = (thien_phu_pos + 6) % 12
    stars["Phá Quân"] = (thien_phu_pos + 10) % 12
    
    return stars

def place_luc_cat(lunar_month: int, hour_branch_idx: int, year_can: str) -> Dict[str, int]:
    stars = {}
    # Tả Hữu
    stars["Tả Phụ"] = (4 + lunar_month - 1) % 12
    stars["Hữu Bật"] = (10 - (lunar_month - 1)) % 12
    
    # Xương Khúc
    stars["Văn Xương"] = (10 - hour_branch_idx) % 12
    stars["Văn Khúc"] = (4 + hour_branch_idx) % 12
    
    # Khôi Việt
    khoi_viet_map = {
        "Giáp": (1, 7), "Mậu": (1, 7), "Canh": (1, 7),
        "Ất": (0, 8), "Kỷ": (0, 8),
        "Bính": (11, 9), "Đinh": (11, 9),
        "Nhâm": (3, 5), "Quý": (3, 5),
        "Tân": (6, 2)
    }
    k_pos, v_pos = khoi_viet_map.get(year_can, (1, 7))
    stars["Thiên Khôi"] = k_pos
    stars["Thiên Việt"] = v_pos
    return stars

def place_luc_sat(year_can: str, year_chi_idx: int, hour_branch_idx: int, is_thuan: bool = True) -> Dict[str, int]:
    stars = {}
    
    # Lộc Tồn position by year Can
    loc_ton_map = {
        "Giáp": 2, "Ất": 3, "Bính": 5, "Đinh": 5, "Mậu": 5, "Kỷ": 6,
        "Canh": 8, "Tân": 9, "Nhâm": 11, "Quý": 0
    }
    loc_pos = loc_ton_map.get(year_can, 2)
    stars["Lộc Tồn"] = loc_pos
    stars["Kình Dương"] = (loc_pos + 1) % 12
    stars["Đà La"] = (loc_pos - 1) % 12
    
    # Không Kiếp
    stars["Địa Không"] = (11 - hour_branch_idx) % 12
    stars["Địa Kiếp"] = (11 + hour_branch_idx) % 12
    
    # Hỏa Tinh & Linh Tinh
    # Dần Ngọ Tuất (2, 6, 10): Hỏa Sửu (1), Linh Mão (3)
    # Thân Tý Thìn (8, 0, 4): Hỏa Dần (2), Linh Tuất (10)
    # Tỵ Dậu Sửu (5, 9, 1): Hỏa Mão (3), Linh Tuất (10)
    # Hợi Mão Mùi (11, 3, 7): Hỏa Dậu (9), Linh Tuất (10)
    if year_chi_idx in [2, 6, 10]:
        if is_thuan:
            h_pos = (1 + hour_branch_idx) % 12
            l_pos = (3 - hour_branch_idx) % 12
        else:
            h_pos = (1 - hour_branch_idx) % 12
            l_pos = (3 + hour_branch_idx) % 12
    elif year_chi_idx in [8, 0, 4]:
        if is_thuan:
            h_pos = (2 + hour_branch_idx) % 12
            l_pos = (10 - hour_branch_idx) % 12
        else:
            h_pos = (2 - hour_branch_idx) % 12
            l_pos = (10 + hour_branch_idx) % 12
    elif year_chi_idx in [5, 9, 1]:
        if is_thuan:
            h_pos = (3 + hour_branch_idx) % 12
            l_pos = (10 - hour_branch_idx) % 12
        else:
            h_pos = (3 - hour_branch_idx) % 12
            l_pos = (10 + hour_branch_idx) % 12
    else: # Hợi Mão Mùi
        h_pos = (9 + hour_branch_idx) % 12
        l_pos = (10 + hour_branch_idx) % 12
        
    stars["Hỏa Tinh"] = h_pos
    stars["Linh Tinh"] = l_pos
    return stars

def place_thai_tue_ring(year_chi_idx: int) -> Dict[str, int]:
    names = [
        "Thái Tuế", "Thiếu Dương", "Tang Môn", "Thiếu Âm", "Quan Phù", "Tử Phù",
        "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Trực Phù"
    ]
    res = {}
    for i, name in enumerate(names):
        res[name] = (year_chi_idx + i) % 12
    return res

def place_bac_si_ring(loc_ton_pos: int, is_thuan: bool) -> Dict[str, int]:
    names = [
        "Bác Sĩ", "Lực Sĩ", "Thanh Long", "Tiểu Hao", "Tướng Quân", "Tấu Thư",
        "Phi Liêm", "Hỷ Thần", "Bệnh Phù", "Đại Hao", "Phục Binh", "Quan Phủ"
    ]
    res = {}
    direction = 1 if is_thuan else -1
    for i, name in enumerate(names):
        res[name] = (loc_ton_pos + i * direction) % 12
    return res

def place_trang_sinh_ring(cuc_num: int, is_thuan: bool) -> Dict[str, int]:
    start_map = {2: 8, 3: 11, 4: 5, 5: 8, 6: 2}
    start_pos = start_map.get(cuc_num, 8)
    names = [
        "Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy",
        "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"
    ]
    res = {}
    direction = 1 if is_thuan else -1
    for i, name in enumerate(names):
        res[name] = (start_pos + i * direction) % 12
    return res

def place_auxiliary_stars(year_can: str, year_chi_idx: int, lunar_month: int, hour_branch_idx: int, lunar_day: int) -> Dict[str, int]:
    stars = {}
    
    # Thiên Mã
    ma_map = {
        2: 8, 6: 8, 10: 8,
        8: 2, 0: 2, 4: 2,
        5: 11, 9: 11, 1: 11,
        11: 5, 3: 5, 7: 5
    }
    stars["Thiên Mã"] = ma_map.get(year_chi_idx, 2)
    
    # Đào Hoa & Hoa Cái & Kiếp Sát
    if year_chi_idx in [11, 3, 7]:
        stars["Đào Hoa"] = 0; stars["Hoa Cái"] = 7; stars["Kiếp Sát"] = 8
    elif year_chi_idx in [8, 0, 4]:
        stars["Đào Hoa"] = 9; stars["Hoa Cái"] = 4; stars["Kiếp Sát"] = 5
    elif year_chi_idx in [2, 6, 10]:
        stars["Đào Hoa"] = 3; stars["Hoa Cái"] = 10; stars["Kiếp Sát"] = 11
    else:
        stars["Đào Hoa"] = 6; stars["Hoa Cái"] = 1; stars["Kiếp Sát"] = 2
        
    # Hồng Loan & Thiên Hỷ
    hl = (3 - year_chi_idx) % 12
    stars["Hồng Loan"] = hl
    stars["Thiên Hỷ"] = (hl + 6) % 12
    
    # Thiên Khốc & Thiên Hư
    stars["Thiên Khốc"] = (6 - year_chi_idx) % 12
    stars["Thiên Hư"] = (6 + year_chi_idx) % 12
    
    # Thiên Hình & Thiên Diêu
    stars["Thiên Hình"] = (9 + lunar_month - 1) % 12
    stars["Thiên Diêu"] = (1 + lunar_month - 1) % 12
    
    # Cô Thần & Quả Tú
    if year_chi_idx in [11, 0, 1]:
        stars["Cô Thần"] = 2; stars["Quả Tú"] = 10
    elif year_chi_idx in [2, 3, 4]:
        stars["Cô Thần"] = 5; stars["Quả Tú"] = 1
    elif year_chi_idx in [5, 6, 7]:
        stars["Cô Thần"] = 8; stars["Quả Tú"] = 4
    else:
        stars["Cô Thần"] = 11; stars["Quả Tú"] = 7
        
    # Thiên La & Địa Võng
    stars["Thiên La"] = 4
    stars["Địa Võng"] = 10
    
    # Thiên Không
    stars["Thiên Không"] = (year_chi_idx + 1) % 12
    
    # Phá Toái
    if year_chi_idx in [0, 6, 3, 9]:
        stars["Phá Toái"] = 5
    elif year_chi_idx in [2, 8, 5, 11]:
        stars["Phá Toái"] = 9
    else:
        stars["Phá Toái"] = 1
        
    # Thai Phụ & Phong Cáo
    vk = (4 + hour_branch_idx) % 12
    stars["Thai Phụ"] = (vk + 2) % 12
    stars["Phong Cáo"] = (vk - 2) % 12
    
    # Tam Thai & Bát Tọa
    tp = (4 + lunar_month - 1) % 12
    hb = (10 - (lunar_month - 1)) % 12
    stars["Tam Thai"] = (tp + lunar_day - 1) % 12
    stars["Bát Tọa"] = (hb - (lunar_day - 1)) % 12
    
    # Ân Quang & Thiên Quý
    vx = (10 - hour_branch_idx) % 12
    stars["Ân Quang"] = (vx + lunar_day - 2) % 12
    stars["Thiên Quý"] = (vk - (lunar_day - 2)) % 12
    
    # Đẩu Quân
    stars["Đẩu Quân"] = (year_chi_idx - (lunar_month - 1) + hour_branch_idx) % 12
    
    return stars

def populate_all_stars(palaces: Dict[int, Any], year_can_chi: str, lunar_month: int, hour_branch_idx: int, lunar_day: int, cuc_num: int, is_thuan: bool):
    year_can = year_can_chi.split()[0]
    year_chi = year_can_chi.split()[1]
    year_chi_idx = CHI.index(year_chi)
    
    # 1. 14 Main stars
    tu_vi_pos = place_tu_vi(lunar_day, cuc_num)
    main_stars = place_14_main_stars(tu_vi_pos)
    for s_name, pos in main_stars.items():
        brightness = STAR_BRIGHTNESS.get(s_name, [""]*12)[pos]
        palaces[pos]["main_stars"].append({
            "name": s_name,
            "brightness": brightness,
            "display": f"{s_name} ({brightness})" if brightness else s_name
        })
        
    # 2. Luc Cat & Luc Sat
    luc_cat = place_luc_cat(lunar_month, hour_branch_idx, year_can)
    luc_sat = place_luc_sat(year_can, year_chi_idx, hour_branch_idx, is_thuan)
    
    # 3. Rings
    thai_tue = place_thai_tue_ring(year_chi_idx)
    bac_si = place_bac_si_ring(luc_sat["Lộc Tồn"], is_thuan)
    trang_sinh = place_trang_sinh_ring(cuc_num, is_thuan)
    
    # 4. Aux stars
    aux = place_auxiliary_stars(year_can, year_chi_idx, lunar_month, hour_branch_idx, lunar_day)
    
    all_subs = {**luc_cat, **luc_sat, **thai_tue, **bac_si, **trang_sinh, **aux}
    for s_name, pos in all_subs.items():
        if s_name not in [s["name"] for s in palaces[pos]["main_stars"]]:
            palaces[pos]["sub_stars"].append(s_name)
