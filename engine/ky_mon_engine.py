"""
Qi Men Dun Jia Calculation Engine (Kỳ Môn Độn Giáp Thời Gia Bàn)
Comprehensive canonical implementation based on Kỳ Môn Toàn Thư:
1. 18 Dun Ju (9 Dương Độn + 9 Âm Độn) via 24 Solar Terms (Tiết Khí) & Tam Nguyên (Thượng/Trung/Hạ)
2. Earth Plate (Địa Bàn: Tam Kỳ Lục Nghi)
3. Xun Shou (Tuần Thủ), Lead Star (Trực Phù), Lead Gate (Trực Sử)
4. Heaven Plate (Thiên Bàn: Cửu Tinh & Kỳ Nghi Thiên Bàn)
5. Gate Plate (Nhân Bàn: Bát Môn)
6. Spirit Plate (Thần Bàn: Bát Thần)
7. Auspicious & Inauspicious Strategic Formations (Cát Hung Cách Cục)
"""
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

try:
    from .lunar_solar import calculate_time_coordinates, translate_han_viet, CAN, CHI
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, translate_han_viet, CAN, CHI

# 9 Cung Lạc Thư & Bát Quái
PALACES_9 = {
    1: {"name": "Khảm 1", "direction": "Chính Bắc", "element": "Thủy", "gua": "Khảm", "original_star": "Thiên Bồng", "original_gate": "Hưu Môn"},
    2: {"name": "Khôn 2", "direction": "Tây Nam", "element": "Thổ", "gua": "Khôn", "original_star": "Thiên Nhuệ", "original_gate": "Tử Môn"},
    3: {"name": "Chấn 3", "direction": "Chính Đông", "element": "Mộc", "gua": "Chấn", "original_star": "Thiên Xung", "original_gate": "Thương Môn"},
    4: {"name": "Tốn 4", "direction": "Đông Nam", "element": "Mộc", "gua": "Tốn", "original_star": "Thiên Phụ", "original_gate": "Đỗ Môn"},
    5: {"name": "Trung 5", "direction": "Trung Cung", "element": "Thổ", "gua": "Thái Cực", "original_star": "Thiên Cầm", "original_gate": "Tử Môn"},
    6: {"name": "Càn 6", "direction": "Tây Bắc", "element": "Kim", "gua": "Càn", "original_star": "Thiên Tâm", "original_gate": "Khai Môn"},
    7: {"name": "Đoài 7", "direction": "Chính Tây", "element": "Kim", "gua": "Đoài", "original_star": "Thiên Trụ", "original_gate": "Kinh Môn"},
    8: {"name": "Cấn 8", "direction": "Đông Bắc", "element": "Thổ", "gua": "Cấn", "original_star": "Thiên Nhậm", "original_gate": "Sinh Môn"},
    9: {"name": "Ly 9", "direction": "Chính Nam", "element": "Hỏa", "gua": "Ly", "original_star": "Thiên Anh", "original_gate": "Cảnh Môn"}
}

# 8 Cung Chu Thiên (Vòng 8 Cung Lạc Thư bỏ Trung Cung 5)
CIRCLE_8 = [1, 8, 3, 4, 9, 2, 7, 6]

# Đối cung Lạc Thư
OPPOSITE_PALACES = {1: 9, 9: 1, 2: 8, 8: 2, 3: 7, 7: 3, 4: 6, 6: 4, 5: 5}

# Bát Môn chuẩn theo thứ tự
EIGHT_GATES_SEQ = ["Hưu Môn", "Sinh Môn", "Thương Môn", "Đỗ Môn", "Cảnh Môn", "Tử Môn", "Kinh Môn", "Khai Môn"]

# Cửu Tinh theo vòng 8 cung
NINE_STARS_SEQ = ["Thiên Bồng", "Thiên Nhậm", "Thiên Xung", "Thiên Phụ", "Thiên Anh", "Thiên Nhuệ", "Thiên Trụ", "Thiên Tâm"]

# Bát Thần
EIGHT_SPIRITS = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]

# Tam Kỳ Lục Nghi
QI_YI_ORDER = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]

# 24 Tiết Khí Tam Nguyên Khởi Cục: (is_yang, thượng_nguyên, trung_nguyên, hạ_nguyên)
TIET_KHI_TAM_NGUYEN = {
    # Dương Độn (Đông Chí -> Mang Chủng)
    "Đông Chí": (True, 1, 7, 4), "Tiểu Hàn": (True, 2, 8, 5), "Đại Hàn": (True, 3, 9, 6),
    "Lập Xuân": (True, 8, 5, 2), "Vũ Thủy": (True, 9, 6, 3), "Kinh Trập": (True, 1, 7, 4),
    "Xuân Phân": (True, 3, 9, 6), "Thanh Minh": (True, 4, 1, 7), "Cốc Vũ": (True, 5, 2, 8),
    "Lập Hạ": (True, 4, 1, 7), "Tiểu Mãn": (True, 5, 2, 8), "Mang Chủng": (True, 6, 3, 9),
    # Âm Độn (Hạ Chí -> Đại Tuyết)
    "Hạ Chí": (False, 9, 3, 6), "Tiểu Thử": (False, 8, 2, 5), "Đại Thử": (False, 7, 1, 4),
    "Lập Thu": (False, 2, 5, 8), "Xử Thử": (False, 1, 4, 7), "Bạch Lộ": (False, 9, 3, 6),
    "Thu Phân": (False, 7, 1, 4), "Hàn Lộ": (False, 6, 9, 3), "Sương Giáng": (False, 5, 8, 2),
    "Lập Đông": (False, 6, 9, 3), "Tiểu Tuyết": (False, 5, 8, 2), "Đại Tuyết": (False, 4, 7, 1)
}

# Lục Giáp Tuần Thủ mapping
TUAN_THU_MAP = {
    0: ("Giáp Tý", "Mậu"),
    10: ("Giáp Tuất", "Kỷ"),
    8: ("Giáp Thân", "Canh"),
    6: ("Giáp Ngọ", "Tân"),
    4: ("Giáp Thìn", "Nhâm"),
    2: ("Giáp Dần", "Quý")
}

CAN_INDICES = {"Giáp": 0, "Ất": 1, "Bính": 2, "Đinh": 3, "Mậu": 4, "Kỷ": 5, "Canh": 6, "Tân": 7, "Nhâm": 8, "Quý": 9}
CHI_INDICES = {"Tý": 0, "Sửu": 1, "Dần": 2, "Mão": 3, "Thìn": 4, "Tỵ": 5, "Ngọ": 6, "Mùi": 7, "Thân": 8, "Dậu": 9, "Tuất": 10, "Hợi": 11}

def get_tam_nguyen_by_day_chi(day_chi: str) -> int:
    """1: Thượng Nguyên, 2: Trung Nguyên, 3: Hạ Nguyên"""
    if day_chi in ["Tý", "Ngọ", "Mão", "Dậu"]:
        return 1
    elif day_chi in ["Dần", "Thân", "Tỵ", "Hợi"]:
        return 2
    else: # Thìn, Tuất, Sửu, Mùi
        return 3

def determine_dun_ju_canonical(tiet_khi: str, day_can: str, day_chi: str) -> Tuple[bool, int, str]:
    matched_tk = "Đông Chí"
    for tk in TIET_KHI_TAM_NGUYEN:
        if tk in tiet_khi:
            matched_tk = tk
            break
            
    is_yang, thuong, trung, ha = TIET_KHI_TAM_NGUYEN[matched_tk]
    nguyen_idx = get_tam_nguyen_by_day_chi(day_chi)
    
    if nguyen_idx == 1:
        ju_num = thuong
        nguyen_name = "Thượng Nguyên"
    elif nguyen_idx == 2:
        ju_num = trung
        nguyen_name = "Trung Nguyên"
    else:
        ju_num = ha
        nguyen_name = "Hạ Nguyên"
        
    return is_yang, ju_num, f"{matched_tk} ({nguyen_name})"

def calculate_ky_mon_chart(dt: datetime) -> Dict[str, Any]:
    """
    Tính toán Bàn Kỳ Môn Độn Giáp toàn diện 4 lớp.
    """
    time_coords = calculate_time_coordinates(dt)
    day_can = time_coords["day_can"]
    day_chi = time_coords["day_chi"]
    hour_can = time_coords["hour_can"]
    hour_chi = time_coords["hour_chi"]
    
    is_yang, ju_num, tiet_khi_full = determine_dun_ju_canonical(time_coords["tiet_khi"], day_can, day_chi)
    dun_type_str = "Duong" if is_yang else "Am"
    dun_type_viet = f"Dương Độn {ju_num} Cục" if is_yang else f"Âm Độn {ju_num} Cục"
    
    # 1. Bố trí Địa Bàn (Tam Kỳ Lục Nghi qua 9 Cung)
    di_ban = {}
    current_p = ju_num
    step = 1 if is_yang else -1
    for yi in QI_YI_ORDER:
        di_ban[current_p] = yi
        current_p = ((current_p - 1 + step) % 9) + 1
        
    # 2. Tìm Tuần Thủ & Cung Gốc của Trực Phù / Trực Sử
    h_can_idx = CAN_INDICES.get(hour_can, 0)
    h_chi_idx = CHI_INDICES.get(hour_chi, 0)
    tuan_offset = (h_chi_idx - h_can_idx) % 12
    tuan_thu_leader, tuan_thu_yi = TUAN_THU_MAP.get(tuan_offset, ("Giáp Tý", "Mậu"))
    
    # Cung gốc chứa Nghi của Tuần Thủ trên Địa Bàn
    lead_palace_origin = next((p for p, yi in di_ban.items() if yi == tuan_thu_yi), 1)
    
    # Sao và Cửa Trực Phù / Trực Sử gốc
    orig_star = PALACES_9[lead_palace_origin]["original_star"]
    orig_gate = PALACES_9[lead_palace_origin]["original_gate"]
    if lead_palace_origin == 5:
        orig_star = "Thiên Cầm"
        orig_gate = "Tử Môn"
        
    # 3. Thiên Bàn & Cửu Tinh
    # Cung đích của Sao Trực Phù: Cung Địa Bàn có Can Giờ
    # Nếu Can Giờ là Giáp -> Lấy theo Nghi của Tuần Thủ
    target_hour_yi = tuan_thu_yi if hour_can == "Giáp" else hour_can
    target_star_palace = next((p for p, yi in di_ban.items() if yi == target_hour_yi), 1)
    if target_star_palace == 5:
        target_star_palace = 2 # Ký Khôn 2
        
    # Xoay Cửu Tinh dọc theo vòng 8 cung CIRCLE_8
    start_star_idx = CIRCLE_8.index(2 if lead_palace_origin == 5 else lead_palace_origin)
    target_star_idx = CIRCLE_8.index(target_star_palace)
    star_shift = (target_star_idx - start_star_idx) % 8
    
    thien_ban = {}
    star_in_palace = {}
    for i, p in enumerate(CIRCLE_8):
        orig_p = CIRCLE_8[(i - star_shift) % 8]
        star_name = PALACES_9[orig_p]["original_star"]
        if orig_p == 2:
            star_name = "Thiên Nhuệ / Thiên Cầm"
        star_in_palace[p] = star_name
        thien_ban[p] = di_ban[orig_p]
    star_in_palace[5] = "Thiên Cầm (Ký Khôn)"
    thien_ban[5] = di_ban[5]
    
    # 4. Bát Môn (Nhân Bàn)
    # Trực Sử đi từ Cung Tuần Thủ theo số bước của Can Giờ
    gate_step_count = h_can_idx
    start_gate_p = 2 if lead_palace_origin == 5 else lead_palace_origin
    if is_yang:
        target_gate_p = ((start_gate_p - 1 + gate_step_count) % 9) + 1
    else:
        target_gate_p = ((start_gate_p - 1 - gate_step_count) % 9) + 1
    if target_gate_p == 5:
        target_gate_p = 2
        
    start_g_idx = CIRCLE_8.index(start_gate_p)
    target_g_idx = CIRCLE_8.index(target_gate_p)
    gate_shift = (target_g_idx - start_g_idx) % 8
    
    gate_in_palace = {}
    for i, p in enumerate(CIRCLE_8):
        orig_g_p = CIRCLE_8[(i - gate_shift) % 8]
        gate_in_palace[p] = PALACES_9[orig_g_p]["original_gate"]
    gate_in_palace[5] = "Trung Cung (Không Cửa)"
    
    # 5. Bát Thần (Thần Bàn)
    # Thần Trực Phù đặt tại target_star_palace. Dương thuận, Âm nghịch.
    target_spirit_idx = CIRCLE_8.index(target_star_palace)
    spirit_in_palace = {}
    for i in range(8):
        s_name = EIGHT_SPIRITS[i]
        if is_yang:
            p_idx = CIRCLE_8[(target_spirit_idx + i) % 8]
        else:
            p_idx = CIRCLE_8[(target_spirit_idx - i) % 8]
        spirit_in_palace[p_idx] = s_name
    spirit_in_palace[5] = "Trung Cung"
    
    # 6. Tổng hợp Cung Ma Trận 9 Cung
    palaces_data = {}
    for pid in range(1, 10):
        p_info = PALACES_9[pid]
        palaces_data[pid] = {
            "palace_id": pid,
            "palace_info": p_info,
            "name": p_info["name"],
            "direction": p_info["direction"],
            "element": p_info["element"],
            "di_ban": di_ban.get(pid, ""),
            "thien_ban": thien_ban.get(pid, ""),
            "star": star_in_palace.get(pid, ""),
            "gate": gate_in_palace.get(pid, ""),
            "spirit": spirit_in_palace.get(pid, "")
        }
        
    # 7. Nhận diện Cát Hung Cách Cục
    auspicious = []
    inauspicious = []
    
    for pid, p in palaces_data.items():
        if pid == 5: continue
        tb, db, gate, star, spirit = p["thien_ban"], p["di_ban"], p["gate"], p["star"], p["spirit"]
        p_dir = p["direction"]
        
        # Cát cách
        if tb == "Mậu" and db == "Bính":
            auspicious.append(f"Thanh Long Đắc Quang tại {p_dir} (Mậu + Bính): Đại cát, mưu sự hanh thông, tài lộc dồi dào.")
        if tb == "Bính" and db == "Mậu":
            auspicious.append(f"Phi Điểu Điệt Huyệt tại {p_dir} (Bính + Mậu): Đại cát, không cầu tự đến, vạn sự thành tựu.")
        if "Đinh" in db and gate == orig_gate:
            auspicious.append(f"Ngọc Nữ Thủ Môn tại {p_dir} (Đinh Kỳ + Trực Sử): Bí mật mưu sự, đàm phán riêng tư đại lợi.")
        if tb == "Bính" and "Sinh Môn" in gate:
            auspicious.append(f"Thiên Độn tại {p_dir} (Bính Kỳ + Sinh Môn): Thần trợ uy lực, xuất hành, lập nghiệp thắng lớn.")
        if tb == "Ất" and db == "Kỷ" and "Khai Môn" in gate:
            auspicious.append(f"Địa Độn tại {p_dir} (Ất Kỳ + Kỷ Nghi + Khai Môn): Ẩn tàng phòng thủ, điền sản vững vàng.")
        if tb == "Đinh" and "Thái Âm" in spirit and "Hưu Môn" in gate:
            auspicious.append(f"Nhân Độn tại {p_dir} (Đinh + Thái Âm + Hưu Môn): Quý nhân tương trợ, hòa hợp viên mãn.")
        if tb == "Bính" and "Cửu Thiên" in spirit and "Sinh Môn" in gate:
            auspicious.append(f"Thần Độn tại {p_dir} (Bính + Cửu Thiên + Sinh Môn): Dương khí dũng mãnh, danh tiếng lẫy lừng.")
            
        # Hung cách
        if tb == "Tân" and db == "Ất":
            inauspicious.append(f"Bạch Hổ Xương Cuồng tại {p_dir} (Tân + Ất): Chủ thương tích, đao kiếm sát thương, kỵ hành động liều lĩnh.")
        if tb == "Ất" and db == "Tân":
            inauspicious.append(f"Thanh Long Đào Tẩu tại {p_dir} (Ất + Tân): Hao tài tốn của, trộm cắp, phá sản, kỵ cho vay mượn.")
        if tb == "Bính" and db == "Canh":
            inauspicious.append(f"Huỳnh Hoặc Nhập Thái Bạch tại {p_dir} (Bính + Canh): Kẻ gian dòm ngó, hỏa hoạn thị phi.")
        if tb == "Canh" and db == "Bính":
            inauspicious.append(f"Thái Bạch Nhập Huỳnh Hoặc tại {p_dir} (Canh + Bính): Tai bay vạ gió, trộm cướp, thị phi kiện tụng.")
        if tb == "Canh" and db == "Mậu":
            inauspicious.append(f"Phục Cung Cách tại {p_dir} (Canh + Mậu): Chủ khách đều bất lợi, kỵ khởi sự.")
        if tb == "Mậu" and db == "Canh":
            inauspicious.append(f"Phi Cung Cách tại {p_dir} (Mậu + Canh): Phá tán tiền của, đổi chỗ dời nhà.")
            
        # Phục Ngâm / Phản Ngâm
        if gate == PALACES_9[pid]["original_gate"]:
            inauspicious.append(f"Cửa {gate} Phục Ngâm tại {p_dir}: Trì trệ, bất động là hơn.")
        if gate == PALACES_9[OPPOSITE_PALACES[pid]]["original_gate"]:
            inauspicious.append(f"Cửa {gate} Phản Ngâm tại {p_dir}: Biến động dữ dội, tráo trở khó lường.")
            
    if not auspicious:
        auspicious.append(f"Trực Phù lâm {PALACES_9[target_star_palace]['direction']} (Quý nhân bảo trợ, hóa hung vi cát)")
        auspicious.append(f"Sinh Môn lâm {next((p['direction'] for p in palaces_data.values() if 'Sinh Môn' in p.get('gate', '')), 'Cấn')} (Cầu tài đắc lợi)")
        
    return {
        "solar_datetime": dt.strftime("%d/%m/%Y %H:%M"),
        "time_can_chi": f"{time_coords['can_chi_year']} - {time_coords['can_chi_month']} - {time_coords['can_chi_day']} - {time_coords['can_chi_hour']}",
        "cuc_so": ju_num,
        "don_type": dun_type_str,
        "dun_type": dun_type_str,
        "don_type_viet": dun_type_viet,
        "dun_type_viet": dun_type_viet,
        "tiet_khi": tiet_khi_full,
        "lead_star": {
            "name": orig_star,
            "current_palace": target_star_palace,
            "direction": PALACES_9[target_star_palace]["direction"]
        },
        "lead_gate": {
            "name": orig_gate,
            "current_palace": target_gate_p,
            "direction": PALACES_9[target_gate_p]["direction"]
        },
        "truc_phu": {
            "star": orig_star,
            "palace": target_star_palace,
            "direction": PALACES_9[target_star_palace]["direction"]
        },
        "truc_su": {
            "gate": orig_gate,
            "palace": target_gate_p,
            "direction": PALACES_9[target_gate_p]["direction"]
        },
        "tuan_thu": f"{tuan_thu_leader} ({tuan_thu_yi})",
        "palaces": palaces_data,
        "auspicious_patterns": auspicious,
        "inauspicious_patterns": inauspicious,
        "metadata": {
            "is_yang_dun": is_yang,
            "ju_number": ju_num,
            "tuan_offset": tuan_offset,
            "lead_palace_origin": lead_palace_origin
        }
    }

def calculate_ky_mon(dt: datetime) -> Dict[str, Any]:
    """Tương thích ngược với các caller cũ."""
    res = calculate_ky_mon_chart(dt)
    return {
        "solar_datetime": res["solar_datetime"],
        "time_can_chi": res["time_can_chi"],
        "tiet_khi": res["tiet_khi"],
        "dun_type": res["dun_type_viet"],
        "lead_star": f"{res['lead_star']['name']} (lâm {res['lead_star']['direction']})",
        "lead_gate": f"{res['lead_gate']['name']} (lâm {res['lead_gate']['direction']})",
        "palaces": res["palaces"],
        "auspicious_patterns": res["auspicious_patterns"],
        "inauspicious_patterns": res["inauspicious_patterns"]
    }

def format_ky_mon_report(km: Dict[str, Any]) -> str:
    out = []
    out.append("=== BÀN KỲ MÔN ĐỘN GIÁP THỜI GIA (QI MEN DUN JIA) ===")
    out.append(f"Thời gian: {km['solar_datetime']} | Can Chi: {km['time_can_chi']}")
    out.append(f"Tiết Khí: {km['tiet_khi']} | Cục Số: 【{km.get('dun_type', km.get('dun_type_viet', '')).upper()}】")
    out.append(f"• Trực Phù: {km['lead_star']} | Trực Sử: {km['lead_gate']}")
    out.append("")
    out.append("┌──────────┬─────────────────┬───────────────────┬───────────────────────┬──────────────┬──────────────┐")
    out.append("│ Cung Vị  │ Phương Vị       │ Thiên Bàn / Nghi  │ Cửu Tinh              │ Bát Môn      │ Bát Thần     │")
    out.append("├──────────┼─────────────────┼───────────────────┼───────────────────────┼──────────────┼──────────────┤")
    for pid in [4, 9, 2, 3, 5, 7, 8, 1, 6]:
        p = km["palaces"].get(pid, {})
        p_name = p.get("name", f"Cung {pid}")
        p_dir = p.get("direction", "")
        p_yi = f"{p.get('thien_ban', '')} / {p.get('di_ban', '')}"
        p_star = p.get("star", "")
        p_gate = p.get("gate", "")
        p_spirit = p.get("spirit", "")
        out.append(f"│ {p_name:<8} │ {p_dir:<15} │ {p_yi:<17} │ {p_star:<21} │ {p_gate:<12} │ {p_spirit:<12} │")
    out.append("└──────────┴─────────────────┴───────────────────┴───────────────────────┴──────────────┴──────────────┘")
    out.append("")
    out.append("=== CÁT CỤC CHIẾN LƯỢC KỲ MÔN ===")
    for a in km.get("auspicious_patterns", []):
        out.append(f"  • [CÁT] {a}")
    if km.get("inauspicious_patterns"):
        out.append("")
        out.append("=== HUNG SÁT CÁCH CỤC CẦN PHÒNG ===")
        for i in km.get("inauspicious_patterns", []):
            out.append(f"  • [HUNG] {i}")
    return "\n".join(out)
