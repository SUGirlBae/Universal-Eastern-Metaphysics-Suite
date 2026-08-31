from typing import Dict, Any, List, Tuple

PALACE_RANK_MAP = {
    1: "Bát Thuần (Bản Cung)",
    2: "Nhất Thế",
    3: "Nhị Thế",
    4: "Tam Thế",
    5: "Tứ Thế",
    6: "Ngũ Thế",
    7: "Du Hồn",
    8: "Quy Hồn"
}

LUC_XUNG_HEX = {
    (1, 1), (8, 8), (6, 6), (3, 3), (4, 4), (7, 7), (2, 2), (5, 5),
    (1, 4), # Thiên Lôi Vô Vọng
    (4, 1)  # Lôi Thiên Đại Tráng
}

LUC_HOP_HEX = {
    (8, 1), # Địa Thiên Thái
    (1, 8), # Thiên Địa Bĩ
    (8, 4), # Địa Lôi Phục
    (7, 1), # Sơn Thiên Đại Súc
    (6, 2), # Thủy Trạch Tiết
    (2, 6), # Trạch Thủy Khốn
    (3, 7), # Hỏa Sơn Lữ
    (7, 3)  # Sơn Hỏa Bí
}

TU_DAI_NAN_HEX = {
    (6, 4), # Thủy Lôi Truân
    (6, 6), # Khảm Vi Thủy
    (6, 7), # Thủy Sơn Kiển
    (2, 6)  # Trạch Thủy Khốn
}

def get_hex_classifications(u: int, l: int, rank_id: int) -> List[str]:
    tags = []
    rank_name = PALACE_RANK_MAP.get(rank_id, f"Thế Hào {rank_id}")
    tags.append(rank_name)
    
    if (u, l) in LUC_XUNG_HEX:
        tags.append("Lục Xung Quái")
    if (u, l) in LUC_HOP_HEX:
        tags.append("Lục Hợp Quái")
    if (u, l) in TU_DAI_NAN_HEX:
        tags.append("Tứ Đại Nan Quái")
    return tags

"""
Unified Liu Yao (Lục Hào Nạp Giáp Toàn Thư) Engine
100% Calibrated with Dã Hạc Toàn Thư, Bốc Phệ Chính Tông & EsotericNumerology Divination Standards
"""

HEXAGRAMS_64 = {
    (1, 1): ("Thuần Càn", "Càn Vi Thiên", 1, 6, 3, 1),
    (1, 2): ("Thiên Trạch Lý", "Thiên Trạch Lý", 7, 5, 2, 6),
    (1, 3): ("Thiên Hỏa Đồng Nhân", "Thiên Hỏa Đồng Nhân", 3, 3, 6, 8),
    (1, 4): ("Thiên Lôi Vô Vọng", "Thiên Lôi Vô Vọng", 5, 4, 1, 5),
    (1, 5): ("Thiên Phong Cấu", "Thiên Phong Cấu", 1, 1, 4, 2),
    (1, 6): ("Thiên Thủy Tụng", "Thiên Thủy Tụng", 3, 4, 1, 7),
    (1, 7): ("Thiên Sơn Độn", "Thiên Sơn Độn", 1, 2, 5, 3),
    (1, 8): ("Thiên Địa Bĩ", "Thiên Địa Bĩ", 1, 3, 6, 4),
    (2, 1): ("Trạch Thiên Quải", "Trạch Thiên Quải", 8, 5, 2, 6),
    (2, 2): ("Thuần Đoài", "Đoài Vi Trạch", 2, 6, 3, 1),
    (2, 3): ("Trạch Hỏa Cách", "Trạch Hỏa Cách", 6, 4, 1, 5),
    (2, 4): ("Trạch Lôi Tùy", "Trạch Lôi Tùy", 4, 3, 6, 8),
    (2, 5): ("Trạch Phong Đại Quá", "Trạch Phong Đại Quá", 4, 4, 1, 7),
    (2, 6): ("Trạch Thủy Khốn", "Trạch Thủy Khốn", 2, 1, 4, 2),
    (2, 7): ("Trạch Sơn Hàm", "Trạch Sơn Hàm", 2, 3, 6, 4),
    (2, 8): ("Trạch Địa Tụy", "Trạch Địa Tụy", 2, 2, 5, 3),
    (3, 1): ("Hỏa Thiên Đại Hữu", "Hỏa Thiên Đại Hữu", 1, 3, 6, 8),
    (3, 2): ("Hỏa Trạch Khuê", "Hỏa Trạch Khuê", 7, 4, 1, 5),
    (3, 3): ("Thuần Ly", "Ly Vi Hỏa", 3, 6, 3, 1),
    (3, 4): ("Hỏa Lôi Phệ Hạp", "Hỏa Lôi Phệ Hạp", 5, 5, 2, 6),
    (3, 5): ("Hỏa Phong Đỉnh", "Hỏa Phong Đỉnh", 3, 2, 5, 3),
    (3, 6): ("Hỏa Thủy Vị Tế", "Hỏa Thủy Vị Tế", 3, 3, 6, 4),
    (3, 7): ("Hỏa Sơn Lữ", "Hỏa Sơn Lữ", 3, 1, 4, 2),
    (3, 8): ("Hỏa Địa Tấn", "Hỏa Địa Tấn", 1, 4, 1, 7),
    (4, 1): ("Lôi Thiên Đại Tráng", "Lôi Thiên Đại Tráng", 8, 4, 1, 5),
    (4, 2): ("Lôi Trạch Quy Muội", "Lôi Trạch Quy Muội", 2, 3, 6, 8),
    (4, 3): ("Lôi Hỏa Phong", "Lôi Hỏa Phong", 6, 5, 2, 6),
    (4, 4): ("Thuần Chấn", "Chấn Vi Lôi", 4, 6, 3, 1),
    (4, 5): ("Lôi Phong Hằng", "Lôi Phong Hằng", 4, 3, 6, 4),
    (4, 6): ("Lôi Thủy Giải", "Lôi Thủy Giải", 4, 2, 5, 3),
    (4, 7): ("Lôi Sơn Tiểu Quá", "Lôi Sơn Tiểu Quá", 2, 4, 1, 7),
    (4, 8): ("Lôi Địa Dự", "Lôi Địa Dự", 4, 1, 4, 2),
    (5, 1): ("Phong Thiên Tiểu Súc", "Phong Thiên Tiểu Súc", 5, 1, 4, 2),
    (5, 2): ("Phong Trạch Trung Phù", "Phong Trạch Trung Phù", 7, 4, 1, 7),
    (5, 3): ("Phong Hỏa Gia Nhân", "Phong Hỏa Gia Nhân", 5, 2, 5, 3),
    (5, 4): ("Phong Lôi Ích", "Phong Lôi Ích", 5, 3, 6, 4),
    (5, 5): ("Thuần Tốn", "Tốn Vi Phong", 5, 6, 3, 1),
    (5, 6): ("Phong Thủy Hoán", "Phong Thủy Hoán", 3, 5, 2, 6),
    (5, 7): ("Phong Sơn Tiệm", "Phong Sơn Tiệm", 7, 3, 6, 8),
    (5, 8): ("Phong Địa Quan", "Phong Địa Quan", 1, 4, 1, 5),
    (6, 1): ("Thủy Thiên Nhu", "Thủy Thiên Nhu", 8, 4, 1, 7),
    (6, 2): ("Thủy Trạch Tiết", "Thủy Trạch Tiết", 6, 1, 4, 2),
    (6, 3): ("Thủy Hỏa Ký Tế", "Thủy Hỏa Ký Tế", 6, 3, 6, 4),
    (6, 4): ("Thủy Lôi Truân", "Thủy Lôi Truân", 6, 2, 5, 3),
    (6, 5): ("Thủy Phong Tỉnh", "Thủy Phong Tỉnh", 4, 5, 2, 6),
    (6, 6): ("Thuần Khảm", "Khảm Vi Thủy", 6, 6, 3, 1),
    (6, 7): ("Thủy Sơn Kiển", "Thủy Sơn Kiển", 2, 4, 1, 5),
    (6, 8): ("Thủy Địa Tỷ", "Thủy Địa Tỷ", 8, 3, 6, 8),
    (7, 1): ("Sơn Thiên Đại Súc", "Sơn Thiên Đại Súc", 7, 2, 5, 3),
    (7, 2): ("Sơn Trạch Tổn", "Sơn Trạch Tổn", 7, 3, 6, 4),
    (7, 3): ("Sơn Hỏa Bí", "Sơn Hỏa Bí", 7, 1, 4, 2),
    (7, 4): ("Sơn Lôi Di", "Sơn Lôi Di", 5, 4, 1, 7),
    (7, 5): ("Sơn Phong Cổ", "Sơn Phong Cổ", 5, 3, 6, 8),
    (7, 6): ("Sơn Thủy Mông", "Sơn Thủy Mông", 3, 4, 1, 5),
    (7, 7): ("Thuần Cấn", "Cấn Vi Sơn", 7, 6, 3, 1),
    (7, 8): ("Sơn Địa Bác", "Sơn Địa Bác", 1, 5, 2, 6),
    (8, 1): ("Địa Thiên Thái", "Địa Thiên Thái", 8, 3, 6, 4),
    (8, 2): ("Địa Trạch Lâm", "Địa Trạch Lâm", 8, 2, 5, 3),
    (8, 3): ("Địa Hỏa Minh Di", "Địa Hỏa Minh Di", 6, 4, 1, 7),
    (8, 4): ("Địa Lôi Phục", "Địa Lôi Phục", 8, 1, 4, 2),
    (8, 5): ("Địa Phong Thăng", "Địa Phong Thăng", 4, 4, 1, 5),
    (8, 6): ("Địa Thủy Sư", "Địa Thủy Sư", 6, 3, 6, 8),
    (8, 7): ("Địa Sơn Khiêm", "Địa Sơn Khiêm", 2, 5, 2, 6),
    (8, 8): ("Thuần Khôn", "Khôn Vi Địa", 8, 6, 3, 1),
}

PALACE_INFO = {
    1: {"name": "Càn", "element": "Kim", "symbol": "Càn"},
    2: {"name": "Đoài", "element": "Kim", "symbol": "Trạch"},
    3: {"name": "Ly", "element": "Hỏa", "symbol": "Ly"},
    4: {"name": "Chấn", "element": "Mộc", "symbol": "Chấn"},
    5: {"name": "Tốn", "element": "Mộc", "symbol": "Tốn"},
    6: {"name": "Khảm", "element": "Thủy", "symbol": "Khảm"},
    7: {"name": "Cấn", "element": "Thổ", "symbol": "Cấn"},
    8: {"name": "Khôn", "element": "Thổ", "symbol": "Khôn"},
}

PALACE_QUAI_THAN = {
    1: "Tỵ", 2: "Dần", 3: "Hợi", 4: "Thân", 5: "Dậu", 6: "Mão", 7: "Tý", 8: "Hợi"
}

# Na Giap: (Can_Inner, Branches_Inner, Can_Outer, Branches_Outer)
# Quái Khôn uses Can Ất for both Inner and Outer
TRIGRAM_NA_GIAP = {
    1: ("Giáp", ["Tý", "Dần", "Thìn"], "Nhâm", ["Ngọ", "Thân", "Tuất"]),
    2: ("Đinh", ["Tỵ", "Mão", "Sửu"], "Đinh", ["Hợi", "Dậu", "Mùi"]),
    3: ("Kỷ", ["Mão", "Sửu", "Hợi"], "Kỷ", ["Dậu", "Mùi", "Tỵ"]),
    4: ("Canh", ["Tý", "Dần", "Thìn"], "Canh", ["Ngọ", "Thân", "Tuất"]),
    5: ("Tân", ["Sửu", "Hợi", "Dậu"], "Tân", ["Mùi", "Tỵ", "Mão"]),
    6: ("Mậu", ["Dần", "Thìn", "Ngọ"], "Mậu", ["Thân", "Tuất", "Tý"]),
    7: ("Bính", ["Thìn", "Ngọ", "Thân"], "Bính", ["Tuất", "Tý", "Dần"]),
    8: ("Ất", ["Mùi", "Tỵ", "Mão"], "Ất", ["Sửu", "Hợi", "Dậu"]),
}

BRANCH_ELEMENTS = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"
}

ELEMENT_RELATIONS = {
    "Kim": {"Kim": "Huynh Đệ", "Thủy": "Tử Tôn", "Mộc": "Thê Tài", "Hỏa": "Quan Quỷ", "Thổ": "Phụ Mẫu"},
    "Mộc": {"Mộc": "Huynh Đệ", "Hỏa": "Tử Tôn", "Thổ": "Thê Tài", "Kim": "Quan Quỷ", "Thủy": "Phụ Mẫu"},
    "Thủy": {"Thủy": "Huynh Đệ", "Mộc": "Tử Tôn", "Hỏa": "Thê Tài", "Thổ": "Quan Quỷ", "Kim": "Phụ Mẫu"},
    "Hỏa": {"Hỏa": "Huynh Đệ", "Thổ": "Tử Tôn", "Kim": "Thê Tài", "Thủy": "Quan Quỷ", "Mộc": "Phụ Mẫu"},
    "Thổ": {"Thổ": "Huynh Đệ", "Kim": "Tử Tôn", "Thủy": "Thê Tài", "Mộc": "Quan Quỷ", "Hỏa": "Phụ Mẫu"},
}

SIX_BEASTS_BY_DAY_CAN = {
    "Giáp": ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"],
    "Ất": ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"],
    "Bính": ["Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ", "Thanh Long"],
    "Đinh": ["Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ", "Thanh Long"],
    "Mậu": ["Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ", "Thanh Long", "Chu Tước"],
    "Kỷ": ["Đằng Xà", "Bạch Hổ", "Huyền Vũ", "Thanh Long", "Chu Tước", "Câu Trần"],
    "Canh": ["Bạch Hổ", "Huyền Vũ", "Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà"],
    "Tân": ["Bạch Hổ", "Huyền Vũ", "Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà"],
    "Nhâm": ["Huyền Vũ", "Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ"],
    "Quý": ["Huyền Vũ", "Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ"],
}

ZODIAC = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

def get_empty_branches(day_can: str, day_chi: str):
    can_i = CAN_LIST.index(day_can)
    chi_i = ZODIAC.index(day_chi)
    start_chi_i = (chi_i - can_i) % 12
    return [ZODIAC[(start_chi_i + 10) % 12], ZODIAC[(start_chi_i + 11) % 12]]

def get_vuong_suy(branch_elem: str, month_branch_elem: str) -> str:
    if branch_elem == month_branch_elem:
        return "Vượng"
    
    sinh = {"Kim": "Thủy", "Thủy": "Mộc", "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim"}
    khac = {"Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim"}
    
    if sinh[month_branch_elem] == branch_elem:
        return "Tướng"
    elif sinh[branch_elem] == month_branch_elem:
        return "Hưu"
    elif khac[branch_elem] == month_branch_elem:
        return "Tù"
    elif khac[month_branch_elem] == branch_elem:
        return "Tử"
    return "Bình"

def get_than_sat(day_can: str, day_chi: str, branch: str) -> list:
    stars = []
    
    # 1. Quý Nhân
    quy_nhan_map = {
        "Giáp": ["Sửu", "Mùi"], "Mậu": ["Sửu", "Mùi"], "Canh": ["Sửu", "Mùi"],
        "Ất": ["Tý", "Thân"], "Kỷ": ["Tý", "Thân"],
        "Bính": ["Hợi", "Dậu"], "Đinh": ["Hợi", "Dậu"],
        "Nhâm": ["Mão", "Tỵ"], "Quý": ["Mão", "Tỵ"],
        "Tân": ["Ngọ", "Dần"]
    }
    if branch in quy_nhan_map.get(day_can, []):
        stars.append("Quý Nhân")
        
    # 2. Lộc Thần
    loc_map = {
        "Giáp": "Dần", "Ất": "Mão", "Bính": "Tỵ", "Đinh": "Ngọ",
        "Mậu": "Tỵ", "Kỷ": "Ngọ", "Canh": "Thân", "Tân": "Dậu",
        "Nhâm": "Hợi", "Quý": "Tý"
    }
    if branch == loc_map.get(day_can):
        stars.append("Lộc")
        
    # 3. Dịch Mã
    ma_map = {
        "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
        "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
        "Tỵ": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi",
        "Hợi": "Tỵ", "Mão": "Tỵ", "Mùi": "Tỵ"
    }
    if branch == ma_map.get(day_chi):
        stars.append("Mã")
        
    # 4. Đào Hoa
    dao_map = {
        "Thân": "Dậu", "Tý": "Dậu", "Thìn": "Dậu",
        "Dần": "Mão", "Ngọ": "Mão", "Tuất": "Mão",
        "Tỵ": "Ngọ", "Dậu": "Ngọ", "Sửu": "Ngọ",
        "Hợi": "Tý", "Mão": "Tý", "Mùi": "Tý"
    }
    if branch == dao_map.get(day_chi):
        stars.append("Đào Hoa")
        
    return stars

def build_hexagram_lines(upper_id: int, lower_id: int):
    l_can, l_branches, _, _ = TRIGRAM_NA_GIAP[lower_id]
    _, _, u_can, u_branches = TRIGRAM_NA_GIAP[upper_id]
    
    lines = []
    for i in range(3):
        lines.append({
            "line_idx": i,
            "can": l_can,
            "chi": l_branches[i],
            "elem": BRANCH_ELEMENTS[l_branches[i]]
        })
    for i in range(3):
        lines.append({
            "line_idx": i + 3,
            "can": u_can,
            "chi": u_branches[i],
            "elem": BRANCH_ELEMENTS[u_branches[i]]
        })
    return lines

def calculate_full_luc_hao(mai_hoa_res: dict, time_coords: dict):
    u_id = mai_hoa_res["upper_id"]
    l_id = mai_hoa_res["lower_id"]
    mov_l = mai_hoa_res["moving_line"]
    
    t_u_id = mai_hoa_res["trans_upper_id"]
    t_l_id = mai_hoa_res["trans_lower_id"]
    
    hex_info = HEXAGRAMS_64[(u_id, l_id)]
    hex_name, hex_symbol, palace_id, the_l, ung_l, gen_seq = hex_info
    palace_data = PALACE_INFO[palace_id]
    palace_elem = palace_data["element"]
    
    t_hex_info = HEXAGRAMS_64[(t_u_id, t_l_id)]
    t_hex_name, t_hex_symbol, t_palace_id, _, _, _ = t_hex_info
    
    m_u_id = mai_hoa_res["mutual_upper_id"]
    m_l_id = mai_hoa_res["mutual_lower_id"]
    m_hex_info = HEXAGRAMS_64[(m_u_id, m_l_id)]
    m_hex_name, m_hex_symbol, m_palace_id, _, _, _ = m_hex_info
    
    day_can = time_coords["day_can"]
    day_chi = time_coords["day_chi"]
    month_chi = time_coords["month_chi"]
    month_elem = time_coords["month_elem"]
    
    empty_branches = get_empty_branches(day_can, day_chi)
    six_beasts = SIX_BEASTS_BY_DAY_CAN[day_can]
    
    primary_lines_raw = build_hexagram_lines(u_id, l_id)
    trans_lines_raw = build_hexagram_lines(t_u_id, t_l_id)
    
    pure_lines_raw = build_hexagram_lines(palace_id, palace_id)
    
    existing_relations = set()
    for l_data in primary_lines_raw:
        rel = ELEMENT_RELATIONS[palace_elem][l_data["elem"]]
        existing_relations.add(rel)
        
    all_relations = ["Phụ Mẫu", "Huynh Đệ", "Tử Tôn", "Thê Tài", "Quan Quỷ"]
    missing_relations = [r for r in all_relations if r not in existing_relations]
    
    lines = []
    for i in range(6):
        l_raw = primary_lines_raw[i]
        t_raw = trans_lines_raw[i]
        pos = i + 1
        is_moving = (pos == mov_l)
        is_the = (pos == the_l)
        is_ung = (pos == ung_l)
        
        rel = ELEMENT_RELATIONS[palace_elem][l_raw["elem"]]
        vs = get_vuong_suy(l_raw["elem"], month_elem)
        is_kv = l_raw["chi"] in empty_branches
        beast = six_beasts[i]
        stars = get_than_sat(day_can, day_chi, l_raw["chi"])
        
        # Quải Thần
        is_quai = False
        target_quai_chi = PALACE_QUAI_THAN.get(palace_id)
        if target_quai_chi and l_raw["chi"] == target_quai_chi:
            if palace_id == 7 and i == 4: # Hào 5 in Họ Cấn
                is_quai = True
            elif palace_id == 6 and i == 0: # Hào 1 in Họ Khảm
                is_quai = True
            elif palace_id not in [6, 7]:
                is_quai = True
                
        # Phục Thần
        phuc = "Không có"
        pure_l = pure_lines_raw[i]
        pure_rel = ELEMENT_RELATIONS[palace_elem][pure_l["elem"]]
        if pure_rel in missing_relations:
            clean_rel = pure_rel.replace(" ", "")
            phuc = f"{clean_rel}-{pure_l['chi']}"
            
        # Transformed line details
        t_rel = ELEMENT_RELATIONS[palace_elem][t_raw["elem"]]
        t_vs = get_vuong_suy(t_raw["elem"], month_elem)
        t_is_kv = t_raw["chi"] in empty_branches
        t_stars = get_than_sat(day_can, day_chi, t_raw["chi"])
        
        pos_str = "Thế" if is_the else ("Ứng" if is_ung else "")
        is_yin = (mai_hoa_res["primary_lines"][i] == 0)
        
        lines.append({
            "line_num": pos,
            "pos_str": pos_str,
            "is_yin": is_yin,
            "is_dong": is_moving,
            "luc_than": rel,
            "can_chi": f"{l_raw['can']} {l_raw['chi']}-{l_raw['elem']}",
            "vuong_suy": vs,
            "is_khong": is_kv,
            "phuc_than": phuc,
            "is_quai_than": is_quai,
            "stars": stars,
            "trans_luc_than": t_rel,
            "trans_can_chi": f"{t_raw['can']} {t_raw['chi']}-{t_raw['elem']}",
            "trans_vuong_suy": t_vs,
            "trans_is_khong": t_is_kv,
            "luc_thu": beast,
            "trans_stars": t_stars
        })
        
    hex_tags = get_hex_classifications(u_id, l_id, hex_info[5])
    t_hex_tags = get_hex_classifications(t_u_id, t_l_id, t_hex_info[5])
    h_hex_tags = get_hex_classifications(m_u_id, m_l_id, m_hex_info[5])
    
    return {
        "hex_name": hex_name,
        "hex_symbol": hex_symbol,
        "palace_id": palace_id,
        "palace_name": palace_data["symbol"],
        "palace_elem": palace_elem,
        "palace_rank": hex_info[5],
        "palace_rank_name": PALACE_RANK_MAP.get(hex_info[5], ""),
        "hex_tags": hex_tags,
        "the_line": the_l,
        "ung_line": ung_l,
        "t_hex_name": t_hex_name,
        "t_hex_symbol": t_hex_symbol,
        "t_palace_name": PALACE_INFO[t_palace_id]["symbol"],
        "t_palace_rank": t_hex_info[5],
        "t_palace_rank_name": PALACE_RANK_MAP.get(t_hex_info[5], ""),
        "t_hex_tags": t_hex_tags,
        "h_hex_name": m_hex_name,
        "h_hex_symbol": m_hex_symbol,
        "h_palace_name": PALACE_INFO[m_palace_id]["symbol"],
        "h_palace_rank": m_hex_info[5],
        "h_palace_rank_name": PALACE_RANK_MAP.get(m_hex_info[5], ""),
        "h_hex_tags": h_hex_tags,
        "lines": lines,
        "moving_line": mov_l
    }


# ==============================================================================
# BẢNG THẦN SÁT TOÀN DIỆN (FULL DAILY SHEN SHA ENGINE)
# ==============================================================================

THIEN_AT_QUY_NHAN = {
    "Giáp": ["Sửu", "Mùi"],
    "Mậu": ["Sửu", "Mùi"],
    "Canh": ["Sửu", "Mùi"],
    "Ất": ["Tý", "Thân"],
    "Kỷ": ["Tý", "Thân"],
    "Bính": ["Hợi", "Dậu"],
    "Đinh": ["Hợi", "Dậu"],
    "Nhâm": ["Tỵ", "Mão"],
    "Quý": ["Tỵ", "Mão"],
    "Tân": ["Ngọ", "Dần"]
}

LOC_THAN = {
    "Giáp": "Dần", "Ất": "Mão", "Bính": "Tỵ", "Đinh": "Ngọ",
    "Mậu": "Tỵ", "Kỷ": "Ngọ", "Canh": "Thân", "Tân": "Dậu",
    "Nhâm": "Hợi", "Quý": "Tý"
}

DICH_MA = {
    "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
    "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
    "Tỵ": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi",
    "Hợi": "Tỵ", "Mão": "Tỵ", "Mùi": "Tỵ"
}

DAO_HOA = {
    "Thân": "Dậu", "Tý": "Dậu", "Thìn": "Dậu",
    "Dần": "Mão", "Ngọ": "Mão", "Tuất": "Mão",
    "Tỵ": "Ngọ", "Dậu": "Ngọ", "Sửu": "Ngọ",
    "Hợi": "Tý", "Mão": "Tý", "Mùi": "Tý"
}

HOA_CAI = {
    "Thân": "Thìn", "Tý": "Thìn", "Thìn": "Thìn",
    "Dần": "Tuất", "Ngọ": "Tuất", "Tuất": "Tuất",
    "Tỵ": "Sửu", "Dậu": "Sửu", "Sửu": "Sửu",
    "Hợi": "Mùi", "Mão": "Mùi", "Mùi": "Mùi"
}

TUONG_TINH = {
    "Thân": "Tý", "Tý": "Tý", "Thìn": "Tý",
    "Dần": "Ngọ", "Ngọ": "Ngọ", "Tuất": "Ngọ",
    "Tỵ": "Dậu", "Dậu": "Dậu", "Sửu": "Dậu",
    "Hợi": "Mão", "Mão": "Mão", "Mùi": "Mão"
}

KIEP_SAT = {
    "Thân": "Tỵ", "Tý": "Tỵ", "Thìn": "Tỵ",
    "Dần": "Hợi", "Ngọ": "Hợi", "Tuất": "Hợi",
    "Tỵ": "Dần", "Dậu": "Dần", "Sửu": "Dần",
    "Hợi": "Thân", "Mão": "Thân", "Mùi": "Thân"
}

TAI_SAT = {
    "Thân": "Ngọ", "Tý": "Ngọ", "Thìn": "Ngọ",
    "Dần": "Tý", "Ngọ": "Tý", "Tuất": "Tý",
    "Tỵ": "Mão", "Dậu": "Mão", "Sửu": "Mão",
    "Hợi": "Dậu", "Mão": "Dậu", "Mùi": "Dậu"
}

VAN_XUONG = {
    "Giáp": "Tỵ", "Ất": "Ngọ", "Bính": "Thân", "Đinh": "Dậu",
    "Mậu": "Thân", "Kỷ": "Dậu", "Canh": "Hợi", "Tân": "Tý",
    "Nhâm": "Dần", "Quý": "Mão"
}

THIEN_Y = {
    "Tý": "Hợi", "Sửu": "Tý", "Dần": "Sửu", "Mão": "Dần",
    "Thìn": "Mão", "Tỵ": "Thìn", "Ngọ": "Tỵ", "Mùi": "Ngọ",
    "Thân": "Mùi", "Dậu": "Thân", "Tuất": "Dậu", "Hợi": "Tuất"
}

def get_full_daily_than_sat(day_can: str, day_chi: str, month_chi: str = "Tý") -> dict:
    """Trả về toàn bộ bảng Thần Sát Nhật Thần và Nguyệt Thần."""
    return {
        "quy_nhan": THIEN_AT_QUY_NHAN.get(day_can, []),
        "loc_than": LOC_THAN.get(day_can, ""),
        "dich_ma": DICH_MA.get(day_chi, ""),
        "dao_hoa": DAO_HOA.get(day_chi, ""),
        "hoa_cai": HOA_CAI.get(day_chi, ""),
        "tuong_tinh": TUONG_TINH.get(day_chi, ""),
        "kiep_sat": KIEP_SAT.get(day_chi, ""),
        "tai_sat": TAI_SAT.get(day_chi, ""),
        "van_xuong": VAN_XUONG.get(day_can, ""),
        "thien_y": THIEN_Y.get(month_chi, "")
    }

def get_line_than_sat_list(day_can: str, day_chi: str, line_chi: str, month_chi: str = "Tý") -> list:
    """Kiểm tra các Thần Sát tọa thủ tại một Địa Chi cụ thể của hào."""
    res = []
    if line_chi in THIEN_AT_QUY_NHAN.get(day_can, []): res.append("Quý Nhân")
    if line_chi == LOC_THAN.get(day_can, ""): res.append("Lộc Thần")
    if line_chi == DICH_MA.get(day_chi, ""): res.append("Dịch Mã")
    if line_chi == DAO_HOA.get(day_chi, ""): res.append("Đào Hoa")
    if line_chi == HOA_CAI.get(day_chi, ""): res.append("Hoa Cái")
    if line_chi == TUONG_TINH.get(day_chi, ""): res.append("Tướng Tinh")
    if line_chi == KIEP_SAT.get(day_chi, ""): res.append("Kiếp Sát")
    if line_chi == TAI_SAT.get(day_chi, ""): res.append("Tai Sát")
    if line_chi == VAN_XUONG.get(day_can, ""): res.append("Văn Xương")
    if line_chi == THIEN_Y.get(month_chi, ""): res.append("Thiên Y")
    return res
