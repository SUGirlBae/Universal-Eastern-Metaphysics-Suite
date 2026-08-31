"""
Master Metaphysics Synthesis Engine
Integrates I Ching, Bazi, Tu Vi, Ha Lac, Ky Mon, and Tung Shing into a single coherent assessment.
"""
from datetime import datetime
from typing import Dict, Any, List

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .mai_hoa import calculate_mai_hoa_from_time
    from .luc_hao import calculate_full_luc_hao
    from .bazi_engine import calculate_bazi
    from .tu_vi_engine import calculate_tu_vi_chart
    from .ha_lac_engine import calculate_ha_lac
    from .ky_mon_engine import calculate_ky_mon
    from .timing_almanac import scan_target_timing_dates
    from .knowledge_graph import analyze_wuxing_interaction, analyze_branch_pair
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from mai_hoa import calculate_mai_hoa_from_time
    from luc_hao import calculate_full_luc_hao
    from bazi_engine import calculate_bazi
    from tu_vi_engine import calculate_tu_vi_chart
    from ha_lac_engine import calculate_ha_lac
    from ky_mon_engine import calculate_ky_mon
    from timing_almanac import scan_target_timing_dates
    from knowledge_graph import analyze_wuxing_interaction, analyze_branch_pair

def run_master_synthesis(dt: datetime, question: str = "", gender: int = 1) -> Dict[str, Any]:
    # 1. Coordinate & I Ching
    time_coords = calculate_time_coordinates(dt)
    mai_hoa = calculate_mai_hoa_from_time(time_coords)
    luc_hao = calculate_full_luc_hao(mai_hoa, time_coords)
    
    # 2. Bazi
    bazi = calculate_bazi(dt, gender=gender)
    
    # 3. Tu Vi
    tu_vi = calculate_tu_vi_chart(dt, gender=gender)
    
    # 4. Ha Lac
    ha_lac = calculate_ha_lac(dt, gender=gender)
    
    # 5. Ky Mon
    ky_mon = calculate_ky_mon(dt)
    
    # 6. Cross-System Synthesis Insights
    CAN_WUXING = {"Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa", "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim", "Nhâm": "Thủy", "Quý": "Thủy"}
    the_elem = luc_hao["palace_elem"]
    day_master_elem = CAN_WUXING.get(bazi["day_master"]["can"], "Thủy")
    
    cross_wuxing = analyze_wuxing_interaction(day_master_elem, the_elem)
    
    insights = []
    insights.append(f"• Tương tác Bản Mệnh (Bát Tự) & Thế Quái (Lục Hào): Nhật Chủ [{day_master_elem}] gặp Thế Cung [{the_elem}] -> {cross_wuxing}")
    insights.append(f"• Tử Vi Cục Số [{tu_vi['cuc_name']}] tương hòa với Kỳ Môn Cục [{ky_mon['dun_type']}]")
    insights.append(f"• Trực Phù [{ky_mon['lead_star']}] - Trực Sử [{ky_mon['lead_gate']}] chỉ hướng khai mở thời vận.")
    insights.append(f"• Hà Lạc Tiên Thiên [{ha_lac['tien_thien']['hex_name']}] chuyển dịch sang Hậu Thiên [{ha_lac['hau_thien']['hex_name']}].")
    
    return {
        "timestamp": dt.strftime("%d/%m/%Y %H:%M"),
        "meta": {
            "query_time": dt.strftime("%d/%m/%Y %H:%M"),
            "question": question or "Tổng quan thời vận & mưu sự",
            "gender": "Nam" if gender == 1 else "Nữ"
        },
        "time_coordinates": time_coords,
        "i_ching": {
            "main_hex": luc_hao["hex_name"],
            "palace": luc_hao["palace_name"],
            "element": luc_hao["palace_elem"],
            "moving_line": luc_hao["moving_line"],
            "transformed_hex": luc_hao["t_hex_name"]
        },
        "bazi": {
            "pillars": bazi["pillars"],
            "day_master": bazi["day_master"]
        },
        "tu_vi": {
            "cuc_name": tu_vi["cuc_name"],
            "menh_branch": tu_vi["menh_branch"],
            "than_branch": tu_vi["than_branch"],
            "four_transformations": tu_vi["four_transformations"]
        },
        "ha_lac": {
            "tien_thien": ha_lac["tien_thien"]["hex_name"],
            "hau_thien": ha_lac["hau_thien"]["hex_name"],
            "nguyen_khi": ha_lac["nguyen_khi"],
            "hoa_cong": ha_lac["hoa_cong"]
        },
        "ky_mon": {
            "dun_type": ky_mon["dun_type"],
            "lead_star": ky_mon["lead_star"],
            "lead_gate": ky_mon["lead_gate"]
        },
        "synthesis_insights": insights,
        "cross_synthesis_insights": insights,
        "cross_discipline_insights": insights
    }

def format_master_synthesis_report(syn: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append("    BÁO CÁO ĐẠI TỔNG HỢP THUẬT SỐ Á ĐÔNG TOÀN DIỆN (MASTER SYNTHESIS REPORT)")
    out.append("================================================================================")
    m = syn["meta"]
    out.append(f"Mục tiêu vấn sự: {m['question']}")
    out.append(f"Thời Không: {m['query_time']} (Múi giờ GMT+7) | Giới tính: {m['gender']}")
    tc = syn["time_coordinates"]
    out.append(f"Tứ Trụ Thời Gian: {tc['can_chi_year']} - {tc['can_chi_month']} - {tc['can_chi_day']} - {tc['can_chi_hour']} | Tiết Khí: {tc['tiet_khi']}")
    out.append("")
    
    out.append("【1. KINH DỊCH & LỤC HÀO】")
    ic = syn["i_ching"]
    out.append(f"  • Quẻ Chính: {ic['main_hex']} (Cung {ic['palace']} - Hành {ic['element']})")
    out.append(f"  • Hào Động: Hào {ic['moving_line']} --> Biến Quẻ: {ic['transformed_hex']}")
    out.append("")
    
    out.append("【2. TỬ BÌNH BÁT TỰ & NHẬT CHỦ】")
    bz = syn["bazi"]
    out.append(f"  • Nhật Chủ: {bz['day_master']['can']} ({bz['day_master'].get('wuxing', '')}) - Nạp Âm: {bz['day_master'].get('nayin', '')}")
    out.append("")
    
    out.append("【3. TỬ VI ĐẨU SỐ】")
    tv = syn["tu_vi"]
    out.append(f"  • Cục Số: {tv['cuc_name']} | Cung Mệnh tại [{tv['menh_branch']}] - Cung Thân tại [{tv['than_branch']}]")
    out.append("")
    
    out.append("【4. BÁT TỰ HÀ LẠC】")
    hl = syn["ha_lac"]
    out.append(f"  • Tiên Thiên: {hl['tien_thien']} | Hậu Thiên: {hl['hau_thien']}")
    out.append(f"  • Hào Nguyên Khí: {hl['nguyen_khi']} | Hào Hóa Công: {hl['hoa_cong']}")
    out.append("")
    
    out.append("【5. KỲ MÔN ĐỘN GIÁP THỜI GIA】")
    km = syn["ky_mon"]
    out.append(f"  • Cục Số: {km['dun_type']}")
    out.append(f"  • Trực Phù: {km['lead_star']} | Trực Sử: {km['lead_gate']}")
    out.append("")
    
    out.append("================================================================================")
    out.append("【ĐẠI ĐỐI ỨNG & KẾT LUẬN CHIẾN LƯỢC TOÀN DIỆN】")
    for ins in syn["synthesis_insights"]:
        out.append(f"  {ins}")
    out.append("================================================================================")
    return "\n".join(out)
