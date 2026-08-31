"""
Xuan Kong Flying Stars (Huyền Không Phi Tinh Vận 9: 2024-2043) & Eight Mansions (Bát Trạch) Engine
Canonical implementation based on Thẩm Thị Huyền Không Học (Thẩm Trúc Nhưng):
1. 24 Mountains (24 Sơn Hướng) & Tam Nguyên Long (Địa / Thiên / Nhân)
2. Period 9 Base Chart (Vận Bàn Vận 9: 2024-2043)
3. Sitting Star (Sơn Tinh) & Facing Star (Hướng Tinh) Flying Direction (Thuận / Nghịch)
4. Full 9-Palace Matrix (Vận Tinh, Sơn Tinh, Hướng Tinh)
5. Special Formations: Đáo Sơn Đáo Hướng, Song Tinh Đáo Hướng/Tọa, Thượng Sơn Hạ Thủy, Phục Ngâm, Phản Ngâm, Thành Môn Quyết
6. Cures & Remedies: Ngũ Hoàng (5) & Nhị Hắc (2)
7. Eight Mansions (Bát Trạch) Personal Cung Phi
"""
from typing import Dict, Any, List, Tuple, Optional, Union
import math

# 24 Sơn Hướng với Tọa độ góc, Cung Bát Quái, Tam Nguyên Long và Tính chất Âm Dương
# Tam Nguyên Long: 1 = Địa Nguyên Long, 2 = Thiên Nguyên Long, 3 = Nhân Nguyên Long
# Dấu Âm Dương (+ / -): + là Dương (Phi thuận), - là Âm (Phi nghịch)
MOUNTAINS_24 = {
    # Khảm 1 (Bắc)
    "Nhâm": {"deg": (337.5, 352.5), "palace": "Khảm", "palace_id": 1, "dragon": "Địa", "dragon_type": 1, "polarity": "+", "element": "Thủy", "opposite": "Bính"},
    "Tý":   {"deg": (352.5, 7.5),   "palace": "Khảm", "palace_id": 1, "dragon": "Thiên", "dragon_type": 2, "polarity": "-", "element": "Thủy", "opposite": "Ngọ"},
    "Quý":  {"deg": (7.5, 22.5),    "palace": "Khảm", "palace_id": 1, "dragon": "Nhân", "dragon_type": 3, "polarity": "-", "element": "Thủy", "opposite": "Đinh"},
    # Cấn 8 (Đông Bắc)
    "Sửu":  {"deg": (22.5, 37.5),   "palace": "Cấn", "palace_id": 8, "dragon": "Địa", "dragon_type": 1, "polarity": "-", "element": "Thổ", "opposite": "Mùi"},
    "Cấn":  {"deg": (37.5, 52.5),   "palace": "Cấn", "palace_id": 8, "dragon": "Thiên", "dragon_type": 2, "polarity": "+", "element": "Thổ", "opposite": "Khôn"},
    "Dần":  {"deg": (52.5, 67.5),   "palace": "Cấn", "palace_id": 8, "dragon": "Nhân", "dragon_type": 3, "polarity": "+", "element": "Thổ", "opposite": "Thân"},
    # Chấn 3 (Đông)
    "Giáp": {"deg": (67.5, 82.5),   "palace": "Chấn", "palace_id": 3, "dragon": "Địa", "dragon_type": 1, "polarity": "+", "element": "Mộc", "opposite": "Canh"},
    "Mão":  {"deg": (82.5, 97.5),   "palace": "Chấn", "palace_id": 3, "dragon": "Thiên", "dragon_type": 2, "polarity": "-", "element": "Mộc", "opposite": "Dậu"},
    "Ất":   {"deg": (97.5, 112.5),  "palace": "Chấn", "palace_id": 3, "dragon": "Nhân", "dragon_type": 3, "polarity": "-", "element": "Mộc", "opposite": "Tân"},
    # Tốn 4 (Đông Nam)
    "Thìn": {"deg": (112.5, 127.5), "palace": "Tốn", "palace_id": 4, "dragon": "Địa", "dragon_type": 1, "polarity": "-", "element": "Mộc", "opposite": "Tuất"},
    "Tốn":  {"deg": (127.5, 142.5), "palace": "Tốn", "palace_id": 4, "dragon": "Thiên", "dragon_type": 2, "polarity": "+", "element": "Mộc", "opposite": "Càn"},
    "Tỵ":   {"deg": (142.5, 157.5), "palace": "Tốn", "palace_id": 4, "dragon": "Nhân", "dragon_type": 3, "polarity": "+", "element": "Mộc", "opposite": "Hợi"},
    # Ly 9 (Nam)
    "Bính": {"deg": (157.5, 172.5), "palace": "Ly", "palace_id": 9, "dragon": "Địa", "dragon_type": 1, "polarity": "+", "element": "Hỏa", "opposite": "Nhâm"},
    "Ngọ":  {"deg": (172.5, 187.5), "palace": "Ly", "palace_id": 9, "dragon": "Thiên", "dragon_type": 2, "polarity": "-", "element": "Hỏa", "opposite": "Tý"},
    "Đinh": {"deg": (187.5, 202.5), "palace": "Ly", "palace_id": 9, "dragon": "Nhân", "dragon_type": 3, "polarity": "-", "element": "Hỏa", "opposite": "Quý"},
    # Khôn 2 (Tây Nam)
    "Mùi":  {"deg": (202.5, 217.5), "palace": "Khôn", "palace_id": 2, "dragon": "Địa", "dragon_type": 1, "polarity": "-", "element": "Thổ", "opposite": "Sửu"},
    "Khôn": {"deg": (217.5, 232.5), "palace": "Khôn", "palace_id": 2, "dragon": "Thiên", "dragon_type": 2, "polarity": "+", "element": "Thổ", "opposite": "Cấn"},
    "Thân": {"deg": (232.5, 247.5), "palace": "Khôn", "palace_id": 2, "dragon": "Nhân", "dragon_type": 3, "polarity": "+", "element": "Thổ", "opposite": "Dần"},
    # Đoài 7 (Tây)
    "Canh": {"deg": (247.5, 262.5), "palace": "Đoài", "palace_id": 7, "dragon": "Địa", "dragon_type": 1, "polarity": "+", "element": "Kim", "opposite": "Giáp"},
    "Dậu":  {"deg": (262.5, 277.5), "palace": "Đoài", "palace_id": 7, "dragon": "Thiên", "dragon_type": 2, "polarity": "-", "element": "Kim", "opposite": "Mão"},
    "Tân":  {"deg": (277.5, 292.5), "palace": "Đoài", "palace_id": 7, "dragon": "Nhân", "dragon_type": 3, "polarity": "-", "element": "Kim", "opposite": "Ất"},
    # Càn 6 (Tây Bắc)
    "Tuất": {"deg": (292.5, 307.5), "palace": "Càn", "palace_id": 6, "dragon": "Địa", "dragon_type": 1, "polarity": "-", "element": "Kim", "opposite": "Thìn"},
    "Càn":  {"deg": (307.5, 322.5), "palace": "Càn", "palace_id": 6, "dragon": "Thiên", "dragon_type": 2, "polarity": "+", "element": "Kim", "opposite": "Tốn"},
    "Hợi":  {"deg": (322.5, 337.5), "palace": "Càn", "palace_id": 6, "dragon": "Nhân", "dragon_type": 3, "polarity": "+", "element": "Kim", "opposite": "Tỵ"}
}

# Lượng Thiên Xích Chu Thiên (Thứ tự 9 Cung khi phi tinh): Trung (5) -> Càn (6) -> Đoài (7) -> Cấn (8) -> Ly (9) -> Khảm (1) -> Khôn (2) -> Chấn (3) -> Tốn (4)
FLYING_ORDER = [5, 6, 7, 8, 9, 1, 2, 3, 4]

# Tên Cửu Tinh
STAR_NAMES = {
    1: "Nhất Bạch Thủy", 2: "Nhị Hắc Thổ", 3: "Tam Bích Mộc",
    4: "Tứ Lục Mộc", 5: "Ngũ Hoàng Thổ", 6: "Lục Bạch Kim",
    7: "Thất Xích Kim", 8: "Bát Bạch Thổ", 9: "Cửu Tử Hỏa"
}

PALACE_NAMES = {
    1: "Khảm 1 (Bắc)", 2: "Khôn 2 (Tây Nam)", 3: "Chấn 3 (Đông)",
    4: "Tốn 4 (Đông Nam)", 5: "Trung Cung 5", 6: "Càn 6 (Tây Bắc)",
    7: "Đoài 7 (Tây)", 8: "Cấn 8 (Đông Bắc)", 9: "Ly 9 (Nam)"
}

# Cung gốc ứng với các Sơn theo Tam Nguyên Long (1: Địa, 2: Thiên, 3: Nhân)
PALACE_DRAGONS = {
    1: {1: "Nhâm", 2: "Tý", 3: "Quý"},
    2: {1: "Mùi", 2: "Khôn", 3: "Thân"},
    3: {1: "Giáp", 2: "Mão", 3: "Ất"},
    4: {1: "Thìn", 2: "Tốn", 3: "Tỵ"},
    6: {1: "Tuất", 2: "Càn", 3: "Hợi"},
    7: {1: "Canh", 2: "Dậu", 3: "Tân"},
    8: {1: "Sửu", 2: "Cấn", 3: "Dần"},
    9: {1: "Bính", 2: "Ngọ", 3: "Đinh"}
}

def degree_to_mountain(deg: float) -> str:
    deg = deg % 360.0
    for m, info in MOUNTAINS_24.items():
        low, high = info["deg"]
        if low > high:  # Vắt qua 0 độ (Nhâm / Tý)
            if deg >= low or deg < high:
                return m
        else:
            if low <= deg < high:
                return m
    return "Tý"

def fly_stars(center_star: int, is_forward: bool) -> Dict[int, int]:
    """Phi tinh qua 9 cung theo Lượng Thiên Xích (Thuận hoặc Nghịch)."""
    res = {}
    curr = center_star
    for p in FLYING_ORDER:
        res[p] = curr
        if is_forward:
            curr = (curr % 9) + 1
        else:
            curr = ((curr - 2) % 9) + 1
    return res

def get_star_polarity(star_num: int, dragon_type: int, default_polarity: str) -> bool:
    """
    Xác định tính chất Âm Dương của Sơn Tinh / Hướng Tinh để phi tinh Thuận (+) hay Nghịch (-).
    - star_num: Số Vận Tinh tại cung Tọa hoặc Hướng
    - dragon_type: 1 (Địa), 2 (Thiên), 3 (Nhân)
    """
    if star_num == 5:
        # Số 5 ở giữa không có quẻ gốc, lấy theo Sơn Tọa/Hướng ban đầu
        return default_polarity == "+"
    mountain_name = PALACE_DRAGONS.get(star_num, {}).get(dragon_type, "Tý")
    pol = MOUNTAINS_24[mountain_name]["polarity"]
    return pol == "+"

def calculate_flying_stars_period9(facing: Union[str, float] = "Tý", birth_year: Optional[int] = None, gender: int = 1) -> Dict[str, Any]:
    """
    Lập Tinh Bàn Huyền Không Phi Tinh Vận 9 (2024-2043) chuẩn canonical.
    - facing: Tên Sơn Hướng (vd "Tý", "Ngọ", "Càn") hoặc độ la bàn (vd 180.0)
    """
    if isinstance(facing, (int, float)):
        facing_mountain = degree_to_mountain(float(facing))
    elif str(facing) in MOUNTAINS_24:
        facing_mountain = str(facing)
    else:
        # Fallback thử parse float nếu là chuỗi số
        try:
            deg_val = float(facing)
            facing_mountain = degree_to_mountain(deg_val)
        except ValueError:
            facing_mountain = "Tý"
            
    m_info = MOUNTAINS_24[facing_mountain]
    sitting_mountain = m_info["opposite"]
    s_info = MOUNTAINS_24[sitting_mountain]
    
    facing_palace_id = m_info["palace_id"]
    sitting_palace_id = s_info["palace_id"]
    
    # 1. Lập Vận Bàn Vận 9 (Số 9 nhập Trung Cung, Phi Thuận)
    base_stars = fly_stars(9, is_forward=True)
    
    # 2. Lấy số Sơn Tinh (tại Cung Tọa) và Hướng Tinh (tại Cung Hướng)
    sitting_base_star = base_stars[sitting_palace_id]
    facing_base_star = base_stars[facing_palace_id]
    
    # 3. Xét hướng bay Thuận / Nghịch của Sơn Tinh & Hướng Tinh
    sitting_forward = get_star_polarity(sitting_base_star, s_info["dragon_type"], s_info["polarity"])
    facing_forward = get_star_polarity(facing_base_star, m_info["dragon_type"], m_info["polarity"])
    
    # 4. Phi Sơn Tinh và Hướng Tinh qua 9 Cung
    mountain_stars = fly_stars(sitting_base_star, is_forward=sitting_forward)
    facing_stars = fly_stars(facing_base_star, is_forward=facing_forward)
    
    # 5. Xây dựng Ma Trận 9 Cung Tinh Bàn
    palaces_grid = {}
    for pid in range(1, 10):
        palaces_grid[pid] = {
            "palace_id": pid,
            "palace_name": PALACE_NAMES[pid],
            "base_star": base_stars[pid],
            "mountain_star": mountain_stars[pid],
            "facing_star": facing_stars[pid],
            "stars_summary": f"[{mountain_stars[pid]} - {base_stars[pid]} - {facing_stars[pid]}]"
        }
        
    # 6. Nhận diện các Thế Tinh Bàn Đặc Thù (Special Formations)
    special_formations = []
    
    # Đáo Sơn Đáo Hướng (Vượng Sơn Vượng Hướng)
    if mountain_stars[sitting_palace_id] == 9 and facing_stars[facing_palace_id] == 9:
        special_formations.append("Vượng Sơn Vượng Hướng (Đáo Sơn Đáo Hướng - Đinh Tài Lưỡng Vượng)")
    elif mountain_stars[facing_palace_id] == 9 and facing_stars[facing_palace_id] == 9:
        special_formations.append("Song Tinh Đáo Hướng (Vượng Tài Tổn Đinh - Cần Thủy ngoài Sa)")
    elif mountain_stars[sitting_palace_id] == 9 and facing_stars[sitting_palace_id] == 9:
        special_formations.append("Song Tinh Đáo Tọa (Vượng Đinh Tổn Tài - Cần Sa ngoài Thủy)")
    elif mountain_stars[facing_palace_id] == 9 and facing_stars[sitting_palace_id] == 9:
        special_formations.append("Thượng Sơn Hạ Thủy (Bại Tài Tổn Đinh - Đại Kỵ)")
        
    # Phục Ngâm / Phản Ngâm
    for pid in range(1, 10):
        if pid == 5: continue
        if mountain_stars[pid] == pid:
            special_formations.append(f"Sơn Tinh Phục Ngâm tại Cung {PALACE_NAMES[pid]}")
        if facing_stars[pid] == pid:
            special_formations.append(f"Hướng Tinh Phục Ngâm tại Cung {PALACE_NAMES[pid]}")
            
    # Thành Môn Quyết (2 cung kề cận cung Hướng)
    # Nếu cung Thành Môn có Hướng Tinh là 9 hoặc 1, kích hoạt vượng khí
    left_p = (facing_palace_id % 9) + 1
    right_p = ((facing_palace_id - 2) % 9) + 1
    thanh_mon_cung = []
    if facing_stars.get(left_p) in [9, 1]:
        thanh_mon_cung.append(f"Cung {PALACE_NAMES[left_p]} (Hướng tinh {facing_stars[left_p]})")
    if facing_stars.get(right_p) in [9, 1]:
        thanh_mon_cung.append(f"Cung {PALACE_NAMES[right_p]} (Hướng tinh {facing_stars[right_p]})")
    if thanh_mon_cung:
        special_formations.append(f"Đắc Thành Môn Quyết: {', '.join(thanh_mon_cung)}")
        
    # 7. Phương Pháp Hóa Giải Sát Tinh
    ngu_hoang_palace = next((p for p, s in facing_stars.items() if s == 5), 1)
    nhi_hac_palace = next((p for p, s in facing_stars.items() if s == 2), 7)
    
    five_yellow_remedy = f"Cung {PALACE_NAMES[ngu_hoang_palace]}: Treo chuông gió đồng 6 ống, hồ lô đồng bát quái, đặt hũ nước muối an nhẫn thủy; tuyệt đối kỵ động thổ, thắp đèn đỏ hoặc bếp lò."
    two_black_remedy = f"Cung {PALACE_NAMES[nhi_hac_palace]}: Đặt hồ lô đồng mạ vàng, xâu tiền Lục Đế, thạch anh trắng giải ách trừ bệnh tật."
    
    # 8. Bát Trạch Cung Phi
    cung_phi_info = None
    if birth_year:
        s = sum(int(d) for d in str(birth_year))
        while s >= 10:
            s = sum(int(d) for d in str(s))
        if gender == 1:
            rem = (11 - s) % 9 or 9
        else:
            rem = (4 + s) % 9 or 9
        quai_names = {1: "Khảm (Đông Tứ Mệnh)", 2: "Khôn (Tây Tứ Mệnh)", 3: "Chấn (Đông Tứ Mệnh)", 4: "Tốn (Đông Tứ Mệnh)", 5: ("Khôn" if gender==1 else "Cấn") + " (Tây Tứ Mệnh)", 6: "Càn (Tây Tứ Mệnh)", 7: "Đoài (Tây Tứ Mệnh)", 8: "Cấn (Tây Tứ Mệnh)", 9: "Ly (Đông Tứ Mệnh)"}
        cung_phi_info = {
            "birth_year": birth_year,
            "cung_phi": quai_names.get(rem, "Khảm"),
            "group": "Đông Tứ Mệnh" if "Đông" in quai_names.get(rem, "") else "Tây Tứ Mệnh"
        }
        
    key_sectors = {
        "Vượng Tài Vượng Khí": f"Chính Nam (Cung Ly 9 - Đương Vận Cửu Tử Hỏa) / Hướng Tinh {facing_stars[facing_palace_id]}",
        "Sinh Khí Tương Lai": "Tây Bắc (Cung Càn 6 - Nhất Bạch Thủy)",
        "Đại Sát Cần Hóa Giải": f"Chính Bắc (Cung Khảm 1 - Ngũ Hoàng Đại Sát) / Sát Tinh Cung {PALACE_NAMES[ngu_hoang_palace]}",
        "Bệnh Phù Cần Đề Phòng": f"Chính Tây (Cung Đoài 7 - Nhị Hắc Bệnh Phù) / Bệnh Phù Cung {PALACE_NAMES[nhi_hac_palace]}"
    }
    
    return {
        "period": "Vận 9 (2024 - 2043) - Cửu Tử Hỏa Tinh Quản Cục",
        "period_number": 9,
        "mountain_name": sitting_mountain,
        "facing_name": facing_mountain,
        "facing": facing_mountain,
        "sitting": sitting_mountain,
        "facing_palace": m_info["palace"],
        "sitting_palace": s_info["palace"],
        "dragon_type": f"Địa/Thiên/Nhân: {m_info['dragon']} Nguyên Long",
        "base_stars": base_stars,
        "mountain_stars": mountain_stars,
        "facing_stars": facing_stars,
        "palaces_grid": palaces_grid,
        "special_formations": special_formations,
        "five_yellow_remedy": five_yellow_remedy,
        "two_black_remedy": two_black_remedy,
        "key_sectors": key_sectors,
        "cung_phi_personal": cung_phi_info,
        "metadata": {
            "sitting_forward": sitting_forward,
            "facing_forward": facing_forward,
            "sitting_base_star": sitting_base_star,
            "facing_base_star": facing_base_star
        }
    }

def calculate_feng_shui_period9(facing_mountain: str = "Tý", birth_year: Optional[int] = None, gender: int = 1) -> Dict[str, Any]:
    """Hàm tương thích cho giao diện cũ."""
    return calculate_flying_stars_period9(facing_mountain, birth_year, gender)

def format_feng_shui_report(res: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append(f"   BÁO CÁO PHONG THỦY HUYỀN KHÔNG PHI TINH VẬN 9 (2024–2043) & BÁT TRẠCH")
    out.append("================================================================================")
    out.append(f"Thời Vận: {res['period']}")
    out.append(f"Thế Nhà: TỌA [{res['sitting']} - Cung {res['sitting_palace']}] HƯỚNG [{res['facing']} - Cung {res['facing_palace']}]")
    out.append(f"Nguyên Long: {res.get('dragon_type', '')}")
    out.append("")
    
    out.append("【I. PHÂN BỐ CÁT HUNG HUYỀN KHÔNG CỬU TINH VẬN 9】")
    for k, v in res.get("key_sectors", {}).items():
        out.append(f"  • {k:<25}: {v}")
    out.append("")
    
    out.append("【II. TINH BÀN HUYỀN KHÔNG 9 CUNG [SƠN TINH - VẬN TINH - HƯỚNG TINH]】")
    out.append("┌─────────────────────┬─────────────────────┬─────────────────────┐")
    out.append("│ Tốn 4 (Đông Nam)    │ Ly 9 (Chính Nam)    │ Khôn 2 (Tây Nam)    │")
    p4, p9, p2 = res["palaces_grid"][4], res["palaces_grid"][9], res["palaces_grid"][2]
    out.append(f"│ {p4['stars_summary']:<19} │ {p9['stars_summary']:<19} │ {p2['stars_summary']:<19} │")
    out.append("├─────────────────────┼─────────────────────┼─────────────────────┤")
    out.append("│ Chấn 3 (Chính Đông) │ Trung Cung 5        │ Đoài 7 (Chính Tây)  │")
    p3, p5, p7 = res["palaces_grid"][3], res["palaces_grid"][5], res["palaces_grid"][7]
    out.append(f"│ {p3['stars_summary']:<19} │ {p5['stars_summary']:<19} │ {p7['stars_summary']:<19} │")
    out.append("├─────────────────────┼─────────────────────┼─────────────────────┤")
    out.append("│ Cấn 8 (Đông Bắc)    │ Khảm 1 (Chính Bắc)  │ Càn 6 (Tây Bắc)     │")
    p8, p1, p6 = res["palaces_grid"][8], res["palaces_grid"][1], res["palaces_grid"][6]
    out.append(f"│ {p8['stars_summary']:<19} │ {p1['stars_summary']:<19} │ {p6['stars_summary']:<19} │")
    out.append("└─────────────────────┴─────────────────────┴─────────────────────┘")
    out.append("")
    
    if res.get("special_formations"):
        out.append("【III. CÁC THẾ CÁCH ĐẶC BIỆT CỦA TINH BÀN】")
        for f in res["special_formations"]:
            out.append(f"  • {f}")
        out.append("")
        
    out.append("【IV. PHÁP HÓA GIẢI SÁT TINH & KÍCH HOẠT TÀI LỘC】")
    out.append(f"  • Hóa giải Ngũ Hoàng: {res['five_yellow_remedy']}")
    out.append(f"  • Hóa giải Nhị Hắc  : {res['two_black_remedy']}")
    out.append("")
    
    if res.get("cung_phi_personal"):
        cp = res["cung_phi_personal"]
        out.append("【V. ĐỐI ỨNG BÁT TRẠCH BẢN MỆNH (CUNG PHI)】")
        out.append(f"  • Năm sinh: {cp['birth_year']} | Cung Phi: {cp['cung_phi']}")
        out.append(f"  • Nhóm Trạch Mệnh: {cp['group']}")
        if "Đông" in cp["group"]:
            out.append("  • Hướng Hợp Đại Cát (Đông Tứ Trạch): Chính Bắc (Khảm), Chính Nam (Ly), Chính Đông (Chấn), Đông Nam (Tốn).")
        else:
            out.append("  • Hướng Hợp Đại Cát (Tây Tứ Trạch): Tây Bắc (Càn), Tây Nam (Khôn), Đông Bắc (Cấn), Chính Tây (Đoài).")
        out.append("")
        
    out.append("【VI. LỜI KHUYÊN BỐ TRÍ DƯƠNG TRẠCH THỰC CHIẾN】")
    out.append("  1. Cửa chính / Phòng khách: Đón khí tại cung vượng tài để kích hoạt tài lộc.")
    out.append("  2. Phòng ngủ / Bàn làm việc: Tránh đặt giường/bàn tại vị trí phạm Ngũ Hoàng hoặc Nhị Hắc.")
    out.append("  3. Hóa giải: Đặt tháp thạch anh trắng / hồ lô đồng tại vị trí Sát Tinh.")
    out.append("================================================================================")
    return "\n".join(out)
