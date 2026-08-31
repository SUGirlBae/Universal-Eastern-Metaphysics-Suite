"""
Four Transformations Module (Tứ Hóa Đa Tầng, Phi Tinh & Khâm Thiên Môn)
Calculates:
1. Niên Can Tứ Hóa (Hóa Lộc A, Hóa Quyền B, Hóa Khoa C, Hóa Kỵ D) across multiple schools.
2. Cung Can Tứ Hóa (Phi Hóa 12 Cung).
3. Tự Hóa (Li Tâm Tứ Hóa) & Hướng Tâm Tứ Hóa.
4. Lộ trình Chuyển Kỵ (Kỵ chuyển Lộc, Kỵ chuyển Kỵ) & Quy Tuyến Lộc Kỵ Toàn Đồ.
5. Tam Bàn: Thiên Bàn, Địa Bàn, Nhân Bàn.
"""
from typing import Dict, Any, List, Tuple
try:
    from .tu_vi_astronomy import CAN, CHI
    from .tu_vi_cuc_so import PALACE_NAMES
except (ImportError, ValueError):
    from tu_vi_astronomy import CAN, CHI
    from tu_vi_cuc_so import PALACE_NAMES

TU_HOA_TABLES = {
    "kham_thien": {
        "Giáp": ["Liêm Trinh", "Phá Quân", "Vũ Khúc", "Thái Dương"],
        "Ất": ["Thiên Cơ", "Thiên Lương", "Tử Vi", "Thái Âm"],
        "Bính": ["Thiên Đồng", "Thiên Cơ", "Văn Xương", "Liêm Trinh"],
        "Đinh": ["Thái Âm", "Thiên Đồng", "Thiên Cơ", "Cự Môn"],
        "Mậu": ["Tham Lang", "Thái Âm", "Hữu Bật", "Thiên Cơ"],
        "Kỷ": ["Vũ Khúc", "Tham Lang", "Thiên Lương", "Văn Khúc"],
        "Canh": ["Thái Dương", "Vũ Khúc", "Thái Âm", "Thiên Đồng"],
        "Tân": ["Cự Môn", "Thái Dương", "Văn Khúc", "Văn Xương"],
        "Nhâm": ["Thiên Lương", "Tử Vi", "Tả Phụ", "Vũ Khúc"],
        "Quý": ["Phá Quân", "Cự Môn", "Thái Âm", "Tham Lang"]
    },
    "trung_chau": {
        "Giáp": ["Liêm Trinh", "Phá Quân", "Vũ Khúc", "Thái Dương"],
        "Ất": ["Thiên Cơ", "Thiên Lương", "Tử Vi", "Thái Âm"],
        "Bính": ["Thiên Đồng", "Thiên Cơ", "Văn Xương", "Liêm Trinh"],
        "Đinh": ["Thái Âm", "Thiên Đồng", "Thiên Cơ", "Cự Môn"],
        "Mậu": ["Tham Lang", "Thái Âm", "Hữu Bật", "Thiên Cơ"],
        "Kỷ": ["Vũ Khúc", "Tham Lang", "Thiên Lương", "Văn Khúc"],
        "Canh": ["Thái Dương", "Vũ Khúc", "Thiên Phủ", "Thiên Đồng"],
        "Tân": ["Cự Môn", "Thái Dương", "Văn Khúc", "Văn Xương"],
        "Nhâm": ["Thiên Lương", "Tử Vi", "Thiên Phủ", "Vũ Khúc"],
        "Quý": ["Phá Quân", "Cự Môn", "Thái Âm", "Tham Lang"]
    },
    "nam_phai": {
        "Giáp": ["Liêm Trinh", "Phá Quân", "Vũ Khúc", "Thái Dương"],
        "Ất": ["Thiên Cơ", "Thiên Lương", "Tử Vi", "Thái Âm"],
        "Bính": ["Thiên Đồng", "Thiên Cơ", "Văn Xương", "Liêm Trinh"],
        "Đinh": ["Thái Âm", "Thiên Đồng", "Thiên Cơ", "Cự Môn"],
        "Mậu": ["Tham Lang", "Thái Âm", "Hữu Bật", "Thiên Cơ"],
        "Kỷ": ["Vũ Khúc", "Tham Lang", "Thiên Lương", "Văn Khúc"],
        "Canh": ["Thái Dương", "Vũ Khúc", "Thiên Đồng", "Thái Âm"],
        "Tân": ["Cự Môn", "Thái Dương", "Văn Khúc", "Văn Xương"],
        "Nhâm": ["Thiên Lương", "Tử Vi", "Thiên Phủ", "Vũ Khúc"],
        "Quý": ["Phá Quân", "Cự Môn", "Thái Âm", "Tham Lang"]
    }
}

def get_star_palace_map(palaces: Dict[int, Any]) -> Dict[str, int]:
    s_map = {}
    for b_idx, p in palaces.items():
        for s in p["main_stars"]:
            s_map[s["name"]] = b_idx
        for s in p["sub_stars"]:
            s_map[s] = b_idx
    return s_map

def calculate_nien_can_tu_hoa(year_can: str, palaces: Dict[int, Any], school: str = "kham_thien") -> Dict[str, Any]:
    table = TU_HOA_TABLES.get(school, TU_HOA_TABLES["kham_thien"])
    stars = table.get(year_can, table["Giáp"])
    s_map = get_star_palace_map(palaces)
    
    types = ["Hóa Lộc (A)", "Hóa Quyền (B)", "Hóa Khoa (C)", "Hóa Kỵ (D)"]
    res = {}
    for i, s_name in enumerate(stars):
        target_pos = s_map.get(s_name, -1)
        p_code = palaces[target_pos]["palace_code"] if target_pos != -1 else ""
        res[types[i]] = {
            "star": s_name,
            "palace_branch": target_pos,
            "palace_code": p_code,
            "display": f"{types[i]} -> {s_name} ({p_code})"
        }
    return res

def calculate_phi_hoa_12_palaces(palaces: Dict[int, Any], school: str = "kham_thien") -> Dict[int, Any]:
    table = TU_HOA_TABLES.get(school, TU_HOA_TABLES["kham_thien"])
    s_map = get_star_palace_map(palaces)
    
    phi_hoa_results = {}
    for b_idx, p in palaces.items():
        p_can = p["can_chi"].split()[0]
        stars = table.get(p_can, table["Giáp"])
        
        loc_star, q_star, k_star, ky_star = stars[0], stars[1], stars[2], stars[3]
        
        loc_palace = palaces[s_map[loc_star]]["palace_code"] if loc_star in s_map else ""
        q_palace = palaces[s_map[q_star]]["palace_code"] if q_star in s_map else ""
        k_palace = palaces[s_map[k_star]]["palace_code"] if k_star in s_map else ""
        ky_palace = palaces[s_map[ky_star]]["palace_code"] if ky_star in s_map else ""
        
        # Check Tự Hóa (Li Tâm Tứ Hóa)
        tu_hoa_list = []
        p_star_names = [s["name"] for s in p["main_stars"]] + p["sub_stars"]
        if loc_star in p_star_names:
            tu_hoa_list.append(f"Tự hóa Lộc ({loc_star})")
        if q_star in p_star_names:
            tu_hoa_list.append(f"Tự hóa Quyền ({q_star})")
        if k_star in p_star_names:
            tu_hoa_list.append(f"Tự hóa Khoa ({k_star})")
        if ky_star in p_star_names:
            tu_hoa_list.append(f"Tự hóa Kỵ ({ky_star})")
            
        phi_hoa_results[b_idx] = {
            "palace_code": p["palace_code"],
            "can_chi": p["can_chi"],
            "phi_loc": {"star": loc_star, "target": loc_palace},
            "phi_quyen": {"star": q_star, "target": q_palace},
            "phi_khoa": {"star": k_star, "target": k_palace},
            "phi_ky": {"star": ky_star, "target": ky_palace},
            "tu_hoa": tu_hoa_list,
            "huong_tam": []
        }
        
    # Check Hướng Tâm Tứ Hóa (Nhập Quái Chiếu Xung)
    # Hướng tâm phát sinh khi:
    # 1. Cung đối diện phi Tứ Hóa vào một sao nằm ở cung này.
    # 2. Cung đối diện Tự Hóa (Li tâm) chiếu thẳng sang cung này theo thế xung chiếu.
    for b_idx, p in palaces.items():
        opp_branch_idx = (b_idx + 6) % 12
        opp_phi = phi_hoa_results[opp_branch_idx]
        opp_p = palaces[opp_branch_idx]
        opp_stars = [s["name"] for s in opp_p["main_stars"]] + opp_p["sub_stars"]
        p_stars = [s["name"] for s in p["main_stars"]] + p["sub_stars"]
        
        huong_tam_list = []
        
        # 1. Direct Flying to this palace
        if opp_phi["phi_loc"]["target"] == p["palace_code"] and opp_phi["phi_loc"]["star"] in p_stars:
            huong_tam_list.append(f"Hướng tâm Lộc ({opp_phi['phi_loc']['star']})")
        if opp_phi["phi_quyen"]["target"] == p["palace_code"] and opp_phi["phi_quyen"]["star"] in p_stars:
            huong_tam_list.append(f"Hướng tâm Quyền ({opp_phi['phi_quyen']['star']})")
        if opp_phi["phi_khoa"]["target"] == p["palace_code"] and opp_phi["phi_khoa"]["star"] in p_stars:
            huong_tam_list.append(f"Hướng tâm Khoa ({opp_phi['phi_khoa']['star']})")
        if opp_phi["phi_ky"]["target"] == p["palace_code"] and opp_phi["phi_ky"]["star"] in p_stars:
            huong_tam_list.append(f"Hướng tâm Kỵ ({opp_phi['phi_ky']['star']})")
            
        # 2. Opposite self-transformation projecting to this palace
        for th in opp_phi["tu_hoa"]:
            if "Tự hóa Lộc" in th and "Hướng tâm Lộc" not in "".join(huong_tam_list):
                s_name = th.split("(")[1].split(")")[0]
                huong_tam_list.append(f"Hướng tâm Lộc ({s_name})")
            if "Tự hóa Quyền" in th and "Hướng tâm Quyền" not in "".join(huong_tam_list):
                s_name = th.split("(")[1].split(")")[0]
                huong_tam_list.append(f"Hướng tâm Quyền ({s_name})")
            if "Tự hóa Khoa" in th and "Hướng tâm Khoa" not in "".join(huong_tam_list):
                s_name = th.split("(")[1].split(")")[0]
                huong_tam_list.append(f"Hướng tâm Khoa ({s_name})")
            if "Tự hóa Kỵ" in th and "Hướng tâm Kỵ" not in "".join(huong_tam_list):
                s_name = th.split("(")[1].split(")")[0]
                huong_tam_list.append(f"Hướng tâm Kỵ ({s_name})")
                
        phi_hoa_results[b_idx]["huong_tam"] = list(set(huong_tam_list))
        
    return phi_hoa_results

def calculate_chuyen_ky_routes(phi_hoa_results: Dict[int, Any], palaces: Dict[int, Any]) -> List[str]:
    routes = []
    p_code_to_idx = {p["palace_code"]: b for b, p in palaces.items()}
    
    for start_code in ["MỆNH", "BÀO", "QUAN", "TÀI", "PHÚC", "ĐIỀN"]:
        b_idx = p_code_to_idx[start_code]
        phi = phi_hoa_results[b_idx]
        target_code = phi["phi_ky"]["target"]
        target_star = phi["phi_ky"]["star"]
        
        if target_code in p_code_to_idx:
            next_b_idx = p_code_to_idx[target_code]
            next_phi = phi_hoa_results[next_b_idx]
            next_loc = next_phi["phi_loc"]["target"]
            next_ky = next_phi["phi_ky"]["target"]
            
            routes.append(f"Tuyến Kỵ chuyển Lộc: {start_code} -> {target_code} ({target_star}) -> Phi Lộc sang {next_loc}")
            routes.append(f"Tuyến Chuyển Kỵ: {start_code} -> {target_code} ({target_star}) -> Phi Kỵ sang {next_ky}")
            
    return routes
