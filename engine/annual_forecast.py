"""
Multi-School Annual Destiny & Fortune Forecasting Engine (Dự Báo Lưu Niên 12 Tháng)
Canonical multi-disciplinary synthesis combining:
1. I Ching 6-Line Bimonthly Scan (6 Hào quản 12 Tháng Âm Lịch)
2. Tu Vi Year Transits (Lưu Thái Tuế & Lưu Tứ Hóa: Lộc, Quyền, Khoa, Kỵ)
3. Bát Tự Hà Lạc (Lưu Niên Biến Hào & Hào Đương Vận)
4. Qi Men Dun Jia Year Auspicious Guidance (Kỳ Môn Độn Giáp Niên Bàn)
"""
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
import json

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ, CAN, CHI
    from .mai_hoa import calculate_mai_hoa_from_time
    from .luc_hao import calculate_full_luc_hao, get_hex_classifications
    from .bazi_engine import calculate_bazi
    from .ha_lac_engine import calculate_ha_lac
    from .ky_mon_engine import calculate_ky_mon_chart
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ, CAN, CHI
    from mai_hoa import calculate_mai_hoa_from_time
    from luc_hao import calculate_full_luc_hao, get_hex_classifications
    from bazi_engine import calculate_bazi
    from ha_lac_engine import calculate_ha_lac
    from ky_mon_engine import calculate_ky_mon_chart

# Lưu Tứ Hóa theo Thiên Can Năm (Chuẩn Thập Can Tứ Hóa Toàn Thư)
YEAR_CAN_TU_HOA = {
    "Giáp": {"loc": "Liêm Trinh", "quyen": "Phá Quân", "khoa": "Vũ Khúc", "ky": "Thái Dương"},
    "Ất":   {"loc": "Thiên Cơ", "quyen": "Thiên Lương", "khoa": "Tử Vi", "ky": "Thái Âm"},
    "Bính": {"loc": "Thiên Đồng", "quyen": "Thiên Cơ", "khoa": "Văn Xương", "ky": "Liêm Trinh"},
    "Đinh": {"loc": "Thái Âm", "quyen": "Thiên Đồng", "khoa": "Thiên Cơ", "ky": "Cự Môn"},
    "Mậu":  {"loc": "Tham Lang", "quyen": "Thái Âm", "khoa": "Hữu Bật", "ky": "Thiên Cơ"},
    "Kỷ":   {"loc": "Vũ Khúc", "quyen": "Tham Lang", "khoa": "Thiên Lương", "ky": "Văn Khúc"},
    "Canh": {"loc": "Thái Dương", "quyen": "Vũ Khúc", "khoa": "Thái Âm", "ky": "Thiên Đồng"},
    "Tân":  {"loc": "Cự Môn", "quyen": "Thái Dương", "khoa": "Văn Khúc", "ky": "Văn Xương"},
    "Nhâm": {"loc": "Thiên Lương", "quyen": "Tử Vi", "khoa": "Tả Phụ", "ky": "Vũ Khúc"},
    "Quý":  {"loc": "Phá Quân", "quyen": "Cự Môn", "khoa": "Thái Âm", "ky": "Tham Lang"}
}

def get_year_canchi(year: int) -> Tuple[str, str]:
    can_idx = (year - 4) % 10
    chi_idx = (year - 4) % 12
    return CAN[can_idx], CHI[chi_idx]

def calculate_annual_forecast(*args, **kwargs) -> Dict[str, Any]:
    """
    Tính toán Dự Báo Lưu Niên 12 Tháng.
    Hỗ trợ linh hoạt mọi kiểu tham số (target_year trước hoặc birth_dt trước, positional hay keyword).
    """
    actual_year = 2026
    actual_birth = None
    gender = kwargs.get("gender", 1)
    question = kwargs.get("question", "")
    
    # 1. Parse positional arguments
    for arg in args:
        if isinstance(arg, datetime):
            actual_birth = arg
        elif isinstance(arg, (int, float)):
            actual_year = int(arg)
        elif isinstance(arg, str) and not question:
            question = arg
            
    # 2. Parse keyword arguments
    if "target_year" in kwargs:
        t = kwargs["target_year"]
        if isinstance(t, (int, float)):
            actual_year = int(t)
        elif isinstance(t, datetime):
            actual_birth = t
    if "birth_dt" in kwargs:
        b = kwargs["birth_dt"]
        if isinstance(b, datetime):
            actual_birth = b
        elif isinstance(b, (int, float)):
            actual_year = int(b)

    target_year = actual_year
    birth_dt = actual_birth
        
    year_can, year_chi = get_year_canchi(target_year)
    year_canchi_str = f"{year_can} {year_chi}"
    
    # 1. Thời điểm khởi tiết Lập Xuân năm mục tiêu
    eval_dt = datetime(target_year, 2, 4, 12, 0, tzinfo=LOCAL_TZ)
    tc = calculate_time_coordinates(eval_dt)
    
    # 2. Kinh Dịch Lục Hào: Quẻ Chiêm Niên Vận 6 Hào quản 12 Tháng
    mh = calculate_mai_hoa_from_time(tc)
    lh = calculate_full_luc_hao(mh, tc)
    
    month_periods = [
        {"period": "Tháng 1 & 2 (Dần, Mão)", "line_pos": 1, "theme": "Khởi đầu mùa xuân, tạo dựng nền tảng, mầm mống công việc"},
        {"period": "Tháng 3 & 4 (Thìn, Tỵ)", "line_pos": 2, "theme": "Gia trạch, công việc sơ khởi, sức khỏe cơ bản"},
        {"period": "Tháng 5 & 6 (Ngọ, Mùi)", "line_pos": 3, "theme": "Mở rộng quy mô, ngưỡng cửa biến động giữa năm"},
        {"period": "Tháng 7 & 8 (Thân, Dậu)", "line_pos": 4, "theme": "Chức vụ, quan hệ đối tác, hợp đồng bên ngoài"},
        {"period": "Tháng 9 & 10 (Tuất, Hợi)", "line_pos": 5, "theme": "Đỉnh cao tài lộc, quyết định chiến lược then chốt"},
        {"period": "Tháng 11 & 12 (Tý, Sửu)", "line_pos": 6, "theme": "Tổng kết cuối năm, thu hoạch tài chính và chuẩn bị chuyển giao"}
    ]
    
    six_lines_forecast = []
    for p in month_periods:
        line_data = next((l for l in lh["lines"] if l["line_num"] == p["line_pos"]), None)
        six_lines_forecast.append({
            "period": p["period"],
            "line_pos": p["line_pos"],
            "theme": p["theme"],
            "line_canchi": line_data["can_chi"] if line_data else "",
            "relation": line_data["luc_than"] if line_data else "",
            "vuong_suy": line_data["vuong_suy"] if line_data else "",
            "is_moving": line_data["is_dong"] if line_data else False,
            "is_kong": line_data["is_khong"] if line_data else False
        })
        
    # 3. Tử Vi Đẩu Số: Lưu Thái Tuế & Lưu Tứ Hóa
    tu_hoa = YEAR_CAN_TU_HOA.get(year_can, {})
    thai_tue_palace = f"Cung {year_chi}"
    
    # 4. Kỳ Môn Độn Giáp Niên Bàn
    km = calculate_ky_mon_chart(eval_dt)
    qimen_guidance = {
        "dun_type": km["dun_type_viet"],
        "lead_star": km["lead_star"]["name"],
        "lead_gate": km["lead_gate"]["name"],
        "best_direction": km["lead_gate"]["direction"],
        "auspicious_advice": km["auspicious_patterns"][:3]
    }
    
    # 5. Bát Tự Hà Lạc (nếu có birth_dt)
    halac_data = None
    if birth_dt:
        try:
            hl = calculate_ha_lac(birth_dt, gender=gender)
            age = target_year - birth_dt.year + 1
            matching_line = next((a for a in hl.get("annual_lines", []) if a["age"] == age), None)
            halac_data = {
                "age": age,
                "active_hex": matching_line["active_hex"] if matching_line else hl["tien_thien"]["hex_name"],
                "active_line": matching_line["active_line"] if matching_line else 1,
                "nguyen_khi": hl["nguyen_khi"],
                "hoa_cong": hl["hoa_cong"]
            }
        except Exception:
            halac_data = None
            
    return {
        "target_year": target_year,
        "lunar_year_can_chi": year_canchi_str,
        "year_canchi": year_canchi_str,
        "year_can": year_can,
        "year_chi": year_chi,
        "thai_tue_palace": thai_tue_palace,
        "luu_tu_hoa": tu_hoa,
        "query_topic": question or "Tổng quan vận trình 12 tháng",
        "iching_annual_hex": {
            "name": lh["hex_name"],
            "palace": lh["palace_name"],
            "tags": lh.get("hex_tags", []),
            "moving_line": lh["moving_line"],
            "transformed_hex": lh["t_hex_name"]
        },
        "six_lines_forecast": six_lines_forecast,
        "bimonthly_timeline": six_lines_forecast,
        "tu_vi_transits": {
            "luu_thai_tue_branch": year_chi,
            "year_transformations": tu_hoa
        },
        "qimen_annual_guidance": qimen_guidance,
        "ky_mon_directions": {
            "dun_type": km["dun_type_viet"],
            "lead_star": km["lead_star"]["name"],
            "lead_gate": km["lead_gate"]["name"]
        },
        "ha_lac_annual": halac_data
    }

def format_annual_forecast_report(res: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append(f"   BÁO CÁO DỰ BÁO THỜI VẬN 12 THÁNG NĂM {res['target_year']} ({res['year_canchi'].upper()})")
    out.append("================================================================================")
    out.append(f"Mục tiêu vấn sự: {res['query_topic']}")
    out.append(f"Lưu Niên: Năm {res['year_canchi']} | Lưu Thái Tuế: {res.get('thai_tue_palace', '')} | Tiết Khởi Vận: Lập Xuân")
    out.append("")
    
    out.append("【I. QUẺ CHIÊM NIÊN VẬN 12 THÁNG (KINH DỊCH LỤC HÀO)】")
    hx = res["iching_annual_hex"]
    tags_str = " - ".join(hx["tags"]) if hx["tags"] else ""
    out.append(f"  • Quẻ Chủ Năm: {hx['name']} (Họ {hx['palace']}) [{tags_str}]")
    out.append(f"  • Hào Động Biến Động: Hào {hx['moving_line']} --> Biến Quẻ: {hx['transformed_hex']}")
    out.append("")
    
    out.append("【II. TIẾN TRÌNH DIỄN BIẾN NĂNG LƯỢNG 6 GIAI ĐOẠN (12 THÁNG)】")
    for m in res["six_lines_forecast"]:
        dong_tag = " [⚡ BIẾN ĐỘNG TRỌNG TÂM]" if m["is_moving"] else ""
        kong_tag = " [⏳ TUẦN KHÔNG CHỜ THỜI]" if m["is_kong"] else ""
        out.append(f"  • {m['period']} (Hào {m['line_pos']}): {m['relation']} ({m['line_canchi']}) - {m['vuong_suy']}{dong_tag}{kong_tag}")
        out.append(f"    --> Chủ đề: {m['theme']}")
    out.append("")
    
    out.append(f"【III. LƯU TỨ HÓA NĂM {res['year_can'].upper()} (TỬ VI ĐẨU SỐ)】")
    th = res.get("luu_tu_hoa", res["tu_vi_transits"]["year_transformations"])
    out.append(f"  • Lưu Hóa Lộc  (Cơ Hội / Tài Khí)    : {th.get('loc')}")
    out.append(f"  • Lưu Hóa Quyền (Hành Động / Quyền Lực): {th.get('quyen')}")
    out.append(f"  • Lưu Hóa Khoa  (Danh Tiếng / Giải Ách): {th.get('khoa')}")
    out.append(f"  • Lưu Hóa Kỵ   (Trắc Trở / Thách Thức) : {th.get('ky')}")
    out.append(f"  • Lưu Thái Tuế tọa tại {res.get('thai_tue_palace', '')}")
    out.append("")
    
    out.append("【IV. KỲ MÔN ĐỘN GIÁP ĐỊNH HƯỚNG CHIẾN LƯỢC】")
    qm = res.get("qimen_annual_guidance", res.get("ky_mon_directions", {}))
    out.append(f"  • Cục Khí  : {qm.get('dun_type', '')}")
    out.append(f"  • Trực Phù : {qm.get('lead_star', '')} | Trực Sử: {qm.get('lead_gate', '')}")
    if qm.get("best_direction"):
        out.append(f"  • Phương Vị Khởi Sự Tối Ưu: {qm.get('best_direction')}")
    out.append("================================================================================")
    return "\n".join(out)
