"""
Cuc So & 12 Palaces Setup Module
Calculates Menh (Life Palace), Than (Body Palace), 12 Palaces layout, 5 Elements Cuc,
and 10-year Da Yun (Đại Vận) for both Thuan/Nghich directions.
"""
from typing import Dict, Any, List, Tuple
try:
    from .tu_vi_astronomy import CAN, CHI, NA_YIN_MAP
except (ImportError, ValueError):
    from tu_vi_astronomy import CAN, CHI, NA_YIN_MAP

PALACE_NAMES = [
    "MỆNH", "BÀO", "PHỐI", "TỬ", "TÀI", "TẬT",
    "DI", "NÔ", "QUAN", "ĐIỀN", "PHÚC", "PHỤ"
]

PALACE_FULL_NAMES = [
    "Mệnh", "Huynh Đệ", "Phu Thê", "Tử Tức", "Tài Bạch", "Tật Ách",
    "Thiên Di", "Nô Bộc", "Quan Lộc", "Điền Trạch", "Phúc Đức", "Phụ Mẫu"
]

CUC_NAMES = {
    2: "Thủy Nhị Cục",
    3: "Mộc Tam Cục",
    4: "Kim Tứ Cục",
    5: "Thổ Ngũ Cục",
    6: "Hỏa Lục Cục"
}

CUC_ELEMENT = {
    2: "Thủy",
    3: "Mộc",
    4: "Kim",
    5: "Thổ",
    6: "Hỏa"
}

def get_palace_can_chi(year_can: str) -> List[str]:
    """
    Returns list of 12 Can Chi for palaces from Tý (index 0) to Hợi (index 11).
    Uses Ngũ Hổ Độn Giáp starting from Dần (index 2).
    """
    # Can khởi Dần
    # Giáp Kỷ -> Bính Dần (2)
    # Ất Canh -> Mậu Dần (4)
    # Bính Tân -> Canh Dần (6)
    # Đinh Nhâm -> Nhâm Dần (8)
    # Mậu Quý -> Giáp Dần (0)
    year_can_idx = CAN.index(year_can)
    start_can_idx = ((year_can_idx % 5) * 2 + 2) % 10
    
    palace_can_chi = [""] * 12
    # Set from Dần (2) to Hợi (11) then Tý (0) to Sửu (1)
    for i in range(12):
        branch_idx = (2 + i) % 12
        can_idx = (start_can_idx + i) % 10
        palace_can_chi[branch_idx] = f"{CAN[can_idx]} {CHI[branch_idx]}"
        
    return palace_can_chi

def calculate_menh_than_positions(lunar_month: int, hour_branch_idx: int) -> Tuple[int, int]:
    """
    Calculates the branch indices (0=Tý, ..., 11=Hợi) of Menh and Than palaces.
    Start at Dần (2), count forward to lunar_month:
      pos_month = (2 + lunar_month - 1) % 12
    From pos_month:
      Count backward to hour_branch_idx -> Menh
      Count forward to hour_branch_idx -> Than
    """
    pos_month = (2 + lunar_month - 1) % 12
    menh_idx = (pos_month - hour_branch_idx) % 12
    than_idx = (pos_month + hour_branch_idx) % 12
    return menh_idx, than_idx

def determine_cuc(menh_can_chi: str) -> int:
    """
    Determines Ngũ Hành Cục from Na Yin of Menh Palace Can Chi.
    """
    nayin = NA_YIN_MAP.get(menh_can_chi, "")
    if "Thủy" in nayin:
        return 2
    elif "Mộc" in nayin:
        return 3
    elif "Kim" in nayin:
        return 4
    elif "Thổ" in nayin:
        return 5
    elif "Hỏa" in nayin:
        return 6
    return 2

def build_12_palaces(year_can_chi: str, lunar_month: int, hour_branch_idx: int, gender: int = 1) -> Dict[str, Any]:
    """
    Builds the 12 Palaces structure including Can Chi, Cuc, Menh, Than, and Da Yun ranges.
    gender: 1=Nam, 0=Nữ
    """
    year_can = year_can_chi.split()[0]
    year_can_idx = CAN.index(year_can)
    is_yang_year = (year_can_idx % 2 == 0) # Giáp, Bính, Mậu, Canh, Nhâm
    
    # Direction:
    # Dương Nam / Âm Nữ -> Thuận (+1)
    # Âm Nam / Dương Nữ -> Nghịch (-1)
    is_thuan = (is_yang_year and gender == 1) or (not is_yang_year and gender == 0)
    direction = 1 if is_thuan else -1
    
    menh_branch_idx, than_branch_idx = calculate_menh_than_positions(lunar_month, hour_branch_idx)
    palace_can_chi = get_palace_can_chi(year_can)
    
    menh_can_chi = palace_can_chi[menh_branch_idx]
    cuc_num = determine_cuc(menh_can_chi)
    
    # Setup 12 palaces
    palaces = {}
    for i in range(12):
        # Index of palace branch on the 12-branch board
        branch_idx = (menh_branch_idx - i) % 12 if not is_thuan else (menh_branch_idx + i) % 12 # Palace names always go counter-clockwise (Nghịch) from Mệnh
        # Note: In standard Tu Vi, the sequence of Palaces: Mệnh -> Phụ -> Phúc -> Điền -> Quan -> Nô -> Di -> Tật -> Tài -> Tử -> Phối -> Bào
        # always runs COUNTER-CLOCKWISE (Nghịch chiều kim đồng hồ) on the 12-palace grid.
        # Menh (i=0), Phụ (i=1 at Menh-1), Phúc (i=2 at Menh-2), etc.
        p_branch_idx = (menh_branch_idx - i) % 12
        p_name = PALACE_NAMES[i]
        p_full_name = PALACE_FULL_NAMES[i]
        p_can_chi = palace_can_chi[p_branch_idx]
        
        # Calculate Da Yun age range for this branch
        # Da Yun starts at Menh Palace, and moves by `direction` (+1 if Thuận, -1 if Nghịch)
        if direction == 1:
            step_from_menh = (p_branch_idx - menh_branch_idx) % 12
        else:
            step_from_menh = (menh_branch_idx - p_branch_idx) % 12
            
        da_yun_start_age = cuc_num + step_from_menh * 10
        da_yun_end_age = da_yun_start_age + 9
        
        palaces[p_branch_idx] = {
            "branch_idx": p_branch_idx,
            "branch_name": CHI[p_branch_idx],
            "palace_code": p_name,
            "palace_name": p_full_name,
            "can_chi": p_can_chi,
            "is_menh": (p_branch_idx == menh_branch_idx),
            "is_than": (p_branch_idx == than_branch_idx),
            "da_yun_range": f"{da_yun_start_age} - {da_yun_end_age}",
            "da_yun_start": da_yun_start_age,
            "da_yun_end": da_yun_end_age,
            "main_stars": [],
            "sub_stars": [],
            "transformations": []
        }
        
    return {
        "menh_branch_idx": menh_branch_idx,
        "than_branch_idx": than_branch_idx,
        "menh_branch_name": CHI[menh_branch_idx],
        "than_branch_name": CHI[than_branch_idx],
        "cuc_num": cuc_num,
        "cuc_name": CUC_NAMES[cuc_num],
        "cuc_element": CUC_ELEMENT[cuc_num],
        "is_thuan": is_thuan,
        "direction_str": "Dương Nam/Âm Nữ - Vận Thuận" if is_thuan else "Âm Nam/Dương Nữ - Vận Nghịch",
        "palaces": palaces,
        "palace_can_chi_list": palace_can_chi
    }
