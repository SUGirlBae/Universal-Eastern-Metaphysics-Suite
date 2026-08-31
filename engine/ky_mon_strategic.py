"""
Strategic Qi Men Dun Jia Engine (Kỳ Môn Độn Giáp Chiến Lược Đa Bộ Môn)
Integrates canonical 18 Dun cycles with cross-disciplinary strategic guidance
(Tu Vi, Bazi, I Ching, Feng Shui, Dan Dao).
"""
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from .ky_mon_engine import calculate_ky_mon_chart, PALACES_9
except (ImportError, ValueError):
    from ky_mon_engine import calculate_ky_mon_chart, PALACES_9

PALACE_DIRECTIONS = {
    1: {"name": "Khảm", "dir": "Bắc", "element": "Thủy", "gua": "Khảm"},
    2: {"name": "Khôn", "dir": "Tây Nam", "element": "Thổ", "gua": "Khôn"},
    3: {"name": "Chấn", "dir": "Đông", "element": "Mộc", "gua": "Chấn"},
    4: {"name": "Tốn", "dir": "Đông Nam", "element": "Mộc", "gua": "Tốn"},
    5: {"name": "Trung", "dir": "Trung Cung", "element": "Thổ", "gua": "Thái Cực"},
    6: {"name": "Càn", "dir": "Tây Bắc", "element": "Kim", "gua": "Càn"},
    7: {"name": "Đoài", "dir": "Tây", "element": "Kim", "gua": "Đoài"},
    8: {"name": "Cấn", "dir": "Đông Bắc", "element": "Thổ", "gua": "Cấn"},
    9: {"name": "Ly", "dir": "Nam", "element": "Hỏa", "gua": "Ly"}
}

EIGHT_DOORS = {
    "Khai Môn": {"type": "Cát", "meaning": "Khai trương, xuất hành, thăng quan tiến chức, ký kết hợp đồng, mưu sự đại thành", "element": "Kim", "base_palace": 6},
    "Hưu Môn": {"type": "Cát", "meaning": "Nghỉ dưỡng, hòa giải, cầu quý nhân, hôn nhân hòa hợp, an định tâm thần", "element": "Thủy", "base_palace": 1},
    "Sinh Môn": {"type": "Đại Cát", "meaning": "Cầu tài đắc lợi, mua bán bất động sản, đầu tư khởi nghiệp, sinh sôi phát triển", "element": "Thổ", "base_palace": 8},
    "Thương Môn": {"type": "Hung", "meaning": "Thu hồi nợ, bắt trộm, tranh chấp kiện tụng, xuất binh chinh phạt", "element": "Mộc", "base_palace": 3},
    "Đỗ Môn": {"type": "Bình", "meaning": "Ẩn nấp, bảo mật thông tin, bế quan tu luyện, phòng thủ cẩn trọng", "element": "Mộc", "base_palace": 4},
    "Cảnh Môn": {"type": "Thứ Cát", "meaning": "Văn thư, quảng bá, thi cử, phỏng vấn, truyền thông, tiệc tùng vui vẻ", "element": "Hỏa", "base_palace": 9},
    "Tử Môn": {"type": "Đại Hung", "meaning": "Tang chế, chôn cất, đi săn, kết liễu sự vụ xấu, tránh mưu đại sự", "element": "Thổ", "base_palace": 2},
    "Kinh Môn": {"type": "Hung", "meaning": "Khẩu thiệt thị phi, nghi kỵ lo âu, làm trò kinh động, bắt giữ", "element": "Kim", "base_palace": 7}
}

NINE_STARS = {
    "Thiên Bồng": {"element": "Thủy", "nature": "Đại Hung/Đại Trí", "desc": "Mưu trí sâu kín, dũng cảm mạo hiểm"},
    "Thiên Nhuệ": {"element": "Thổ", "nature": "Hung tinh", "desc": "Bệnh tinh, thầy trò kết giao, học tập nghiên cứu"},
    "Thiên Nhuệ / Thiên Cầm": {"element": "Thổ", "nature": "Cát tinh", "desc": "Bao dung trung chính, học tập nghiên cứu"},
    "Thiên Xung": {"element": "Mộc", "nature": "Cát tinh", "desc": "Xông pha hành động, giải cứu, quyết đoán thần tốc"},
    "Thiên Phụ": {"element": "Mộc", "nature": "Đại Cát", "desc": "Văn xương học vấn, thi cử, quý nhân trợ lực"},
    "Thiên Cầm": {"element": "Thổ", "nature": "Đại Cát", "desc": "Tọa trấn trung cung, quân vương chính đạo, bao dung vạn vật"},
    "Thiên Tâm": {"element": "Kim", "nature": "Đại Cát", "desc": "Y đạo trị bệnh, mưu lược lãnh đạo, quân sư chiến lược"},
    "Thiên Trụ": {"element": "Kim", "nature": "Hung tinh", "desc": "Hùng biện thuyết phục, phòng thủ kiên cố, chỉnh đốn kỷ cương"},
    "Thiên Nhậm": {"element": "Thổ", "nature": "Đại Cát", "desc": "Làm ăn chân chính, tích lũy điền sản, trung hậu thành tín"},
    "Thiên Anh": {"element": "Hỏa", "nature": "Bình tinh", "desc": "Hào quang danh tiếng, thanh thế lẫy lừng, lễ nghi tiệc tùng"}
}

EIGHT_DEITIES = {
    "Trực Phù": {"nature": "Đại Cát", "desc": "Bách thần chi thủ, vạn ác tiêu tan, quý nhân tối cao phò trợ"},
    "Đằng Xà": {"nature": "Hung thần", "desc": "Biến hóa khôn lường, hư kinh quái dị, mộng mị lo âu"},
    "Thái Âm": {"nature": "Cát thần", "desc": "Âm đức che chở, mưu kín thành tựu, quý nhân ẩn tàng hỗ trợ"},
    "Lục Hợp": {"nature": "Cát thần", "desc": "Hòa hợp giao dịch, hôn nhân mai mối, đàm phán ký kết thắng lợi"},
    "Bạch Hổ": {"nature": "Hung thần", "desc": "Sát phạt quyền uy, tai nạn thương tích, quyết đoán quân sự"},
    "Huyền Vũ": {"nature": "Hung thần", "desc": "Trộm cắp mất mát, tiểu nhân lừa dối, phòng ngừa khẩu thiệt"},
    "Cửu Địa": {"nature": "Cát thần", "desc": "Kiên cố vững vàng, ẩn nhẫn tích lũy, phòng thủ bảo toàn nguyên khí"},
    "Cửu Thiên": {"nature": "Đại Cát", "desc": "Chủ động xuất kích, thanh danh vang dội, thăng tiến vượt bậc"}
}

def calculate_strategic_qimen(dt: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Tính toán Bàn Kỳ Môn Độn Giáp Chiến Lược dựa trên Bàn Kỳ Môn Canonical 4 Lớp.
    """
    if dt is None:
        dt = datetime.now()
        
    chart = calculate_ky_mon_chart(dt)
    
    palace_matrix = []
    palace_indices = [1, 8, 3, 4, 9, 2, 7, 6]  # Khảm, Cấn, Chấn, Tốn, Ly, Khôn, Đoài, Càn
    
    for p_idx in palace_indices:
        p_raw = chart["palaces"].get(p_idx, {})
        p_info = PALACE_DIRECTIONS[p_idx]
        door_name = p_raw.get("gate", "Hưu Môn")
        star_name = p_raw.get("star", "Thiên Bồng")
        deity_name = p_raw.get("spirit", "Trực Phù")
        
        door_info = EIGHT_DOORS.get(door_name, {"type": "Bình", "meaning": "", "element": "Mộc"})
        star_info = NINE_STARS.get(star_name, {"element": "Thổ", "nature": "Cát tinh", "desc": ""})
        deity_info = EIGHT_DEITIES.get(deity_name, {"nature": "Cát thần", "desc": ""})
        
        # Đánh giá điểm chiến lược
        score = 0
        if door_info.get("type") in ["Đại Cát", "Cát"]: score += 2
        elif door_info.get("type") == "Thứ Cát": score += 1
        elif door_info.get("type") in ["Đại Hung", "Hung"]: score -= 2
        
        if star_info.get("nature") in ["Đại Cát", "Cát tinh"]: score += 2
        elif star_info.get("nature") == "Hung tinh": score -= 1
        
        if deity_info.get("nature") in ["Đại Cát", "Cát thần"]: score += 2
        elif deity_info.get("nature") == "Hung thần": score -= 1
        
        level = "ĐẠI CÁT" if score >= 4 else ("CÁT" if score >= 2 else ("BÌNH" if score >= 0 else "HUNG"))
        
        palace_matrix.append({
            "palace_idx": p_idx,
            "palace_name": p_info["name"],
            "direction": p_info["dir"],
            "element": p_info["element"],
            "thien_ban": p_raw.get("thien_ban", ""),
            "di_ban": p_raw.get("di_ban", ""),
            "door": {"name": door_name, **door_info},
            "star": {"name": star_name, **star_info},
            "deity": {"name": deity_name, **deity_info},
            "strategic_score": score,
            "overall_level": level
        })
        
    # Định vị các phương vị chiến lược quan trọng nhất
    best_wealth = next((p for p in palace_matrix if "Sinh Môn" in p["door"]["name"]), palace_matrix[0])
    best_career = next((p for p in palace_matrix if "Khai Môn" in p["door"]["name"]), palace_matrix[1])
    best_peace = next((p for p in palace_matrix if "Hưu Môn" in p["door"]["name"]), palace_matrix[2])
    best_fame = next((p for p in palace_matrix if "Cảnh Môn" in p["door"]["name"]), palace_matrix[3])
    
    # Giao thoa chiến lược hành động đa bộ môn
    cross_discipline_strategies = {
        "tu_vi_action": f"Khi cần kích hoạt cung Tài Bạch/Điền Trạch hoặc giải tỏa Kỵ tinh: Xuất hành/đàm phán hướng {best_wealth['direction']} ({best_wealth['door']['name']} + {best_wealth['deity']['name']}).",
        "bazi_action": f"Thời khắc đắc khí để hành sự theo Dụng Thần: Hướng {best_career['direction']} ({best_career['door']['name']} + {best_career['star']['name']}) mang lại uy quyền và hợp đồng quyết định.",
        "iching_remedy": f"Hóa giải quẻ hiểm (Kiển, Khảm, Truân): Lấy hướng {best_peace['direction']} ({best_peace['door']['name']} + {best_peace['deity']['name']}) làm phương vị thu liễm, hòa giải và tìm quý nhân.",
        "feng_shui_boost": f"Kích hoạt Cửu Tử Hỏa Tinh Vận 9: Đặt bàn làm việc hoặc vật phẩm phong thủy kích tài tại phương vị {best_wealth['direction']} ({best_wealth['door']['name']}).",
        "dan_dao_health": f"Thời điểm tĩnh tọa luyện khí dưỡng tạng phủ: Quay mặt về hướng {best_peace['direction']} ({best_peace['door']['name']} + {best_peace['deity']['name']}) để an định thần khí, nạp âm tinh."
    }
    
    return {
        "datetime": dt.strftime("%d/%m/%Y %H:%M"),
        "cycle_type": chart["dun_type_viet"],
        "tiet_khi": chart["tiet_khi"],
        "lead_star": chart["lead_star"],
        "lead_gate": chart["lead_gate"],
        "palaces": palace_matrix,
        "strategic_highlights": {
            "cầu_tài_đầu_tư": {"direction": best_wealth["direction"], "door": best_wealth["door"]["name"], "star": best_wealth["star"]["name"], "deity": best_wealth["deity"]["name"]},
            "công_danh_ký_kết": {"direction": best_career["direction"], "door": best_career["door"]["name"], "star": best_career["star"]["name"], "deity": best_career["deity"]["name"]},
            "quý_nhân_hòa_giải": {"direction": best_peace["direction"], "door": best_peace["door"]["name"], "star": best_peace["star"]["name"], "deity": best_peace["deity"]["name"]},
            "danh_tiếng_truyền_thông": {"direction": best_fame["direction"], "door": best_fame["door"]["name"], "star": best_fame["star"]["name"], "deity": best_fame["deity"]["name"]}
        },
        "cross_strategies": cross_discipline_strategies,
        "auspicious_patterns": chart["auspicious_patterns"],
        "inauspicious_patterns": chart["inauspicious_patterns"]
    }
