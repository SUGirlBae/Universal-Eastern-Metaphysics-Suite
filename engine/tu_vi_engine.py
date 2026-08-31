"""
Tu Vi Occult Engine Facade
Provides unified access to Tu Vi Chart generation, 14 Main Stars, 12 Palaces, Four Transformations.
"""
from datetime import datetime
from typing import Dict, Any

try:
    from .tu_vi_astronomy import get_astronomical_profile
    from .tu_vi_cuc_so import build_12_palaces
    from .tu_vi_stars import place_14_main_stars, place_tu_vi
    from .tu_vi_four_transformations import TU_HOA_TABLES
except (ImportError, ValueError):
    from tu_vi_astronomy import get_astronomical_profile
    from tu_vi_cuc_so import build_12_palaces
    from tu_vi_stars import place_14_main_stars, place_tu_vi
    from tu_vi_four_transformations import TU_HOA_TABLES

def calculate_four_transformations(year_can: str, school: str = "kham_thien") -> Dict[str, Any]:
    table = TU_HOA_TABLES.get(school, TU_HOA_TABLES["kham_thien"])
    stars = table.get(year_can, table["Giáp"])
    return {
        "loc": stars[0],
        "quyen": stars[1],
        "khoa": stars[2],
        "ky": stars[3],
        "raw_assignments": {
            "Hóa Lộc": f"{stars[0]} (Lộc)",
            "Hóa Quyền": f"{stars[1]} (Quyền)",
            "Hóa Khoa": f"{stars[2]} (Khoa)",
            "Hóa Kỵ": f"{stars[3]} (Kỵ)"
        }
    }

def calculate_tu_vi_chart(dt: datetime, gender: int = 1, longitude: float = 105.720) -> Dict[str, Any]:
    astro = get_astronomical_profile(dt, longitude=longitude)
    
    palaces_data = build_12_palaces(astro["year_can_chi"], astro["lunar_month"], astro["hour_chi_idx"], gender=gender)
    tu_vi_pos = place_tu_vi(astro["lunar_day"], palaces_data["cuc_num"])
    main_stars = place_14_main_stars(tu_vi_pos)
    
    y_can = astro["year_can_chi"].split()[0]
    four_trans = calculate_four_transformations(y_can)
    
    palace_list = []
    for b_idx in range(12):
        p_info = palaces_data["palaces"].get(b_idx, {})
        stars_here = [s for s, pos in main_stars.items() if pos == b_idx]
        palace_list.append({
            "branch_idx": b_idx,
            "branch_name": p_info.get("branch_name", ""),
            "palace_name": p_info.get("palace_name", ""),
            "can_chi": p_info.get("can_chi", ""),
            "is_menh": p_info.get("is_menh", False),
            "is_than": p_info.get("is_than", False),
            "da_yun_range": p_info.get("da_yun_range", ""),
            "main_stars": stars_here
        })
        
    return {
        "solar_datetime": dt.strftime("%d/%m/%Y %H:%M"),
        "lunar_datetime": f"{astro['lunar_day']:02d}/{astro['lunar_month']:02d}/{astro['lunar_year']}",
        "can_chi": {
            "year": astro["year_can_chi"],
            "month": astro["month_can_chi"],
            "day": astro["day_can_chi"],
            "hour": astro["hour_can_chi"]
        },
        "cuc_name": palaces_data["cuc_name"],
        "direction_str": palaces_data["direction_str"],
        "menh_branch": palaces_data["menh_branch_name"],
        "than_branch": palaces_data["than_branch_name"],
        "palaces": palace_list,
        "four_transformations": four_trans
    }

def format_tu_vi_report(chart: Dict[str, Any]) -> str:
    out = []
    out.append("=== LÁ SỐ TỬ VI ĐẨU SỐ TOÀN DIỆN (PURPLE STAR ASTROLOGY) ===")
    out.append(f"Dương Lịch: {chart['solar_datetime']} | Âm Lịch: {chart['lunar_datetime']}")
    cc = chart['can_chi']
    out.append(f"Can Chi: {cc['year']} - {cc['month']} - {cc['day']} - {cc['hour']}")
    out.append(f"• Cục Số: {chart['cuc_name']} ({chart['direction_str']})")
    out.append(f"• Cung Mệnh tại: {chart['menh_branch']} | Cung Thân tại: {chart['than_branch']}")
    out.append("")
    out.append("=== BỐ TRÍ 12 CUNG & CHÍNH TINH ===")
    for p in chart["palaces"]:
        stars_str = ", ".join(p["main_stars"]) if p["main_stars"] else "Vô Chính Diệu"
        tags = []
        if p["is_menh"]: tags.append("[MỆNH]")
        if p["is_than"]: tags.append("[THÂN]")
        tag_str = " " + " ".join(tags) if tags else ""
        out.append(f"  • Cung {p['palace_name']:<12} ({p['branch_name']}) [{p['can_chi']}]{tag_str}: {stars_str} (Đại Vận: {p['da_yun_range']})")
    out.append("")
    out.append("=== TỨ HÓA NĂM SINH (LỘC QUYỀN KHOA KỴ) ===")
    ft = chart["four_transformations"]
    for k, v in ft.get("raw_assignments", {}).items():
        out.append(f"  • {k}: {v}")
    return "\n".join(out)
