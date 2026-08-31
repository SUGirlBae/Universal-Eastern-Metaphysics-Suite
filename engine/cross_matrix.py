"""
Cross-Disciplinary Metaphysics Synthesis Matrix (Động Cơ Giao Thoa Ma Trận Chéo)
Strict Architecture Invariant:
- I Ching (Mai Hoa, Lục Hào 3 Xu, Bát Quái) acts as the UNIDIRECTIONAL BACKBONE (Xương sống 1 chiều).
- I Ching is injected into other disciplines (Eastern Medicine, Feng Shui, Tu Vi, Bazi, Annual Forecast).
- No other disciplines are allowed to mutate or inject backwards into pure I Ching.
- Non-I Ching disciplines may cross-interact freely.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .mai_hoa import calculate_mai_hoa_from_time
    from .luc_hao import calculate_full_luc_hao, get_hex_classifications
    from .coin_toss import calculate_coin_luc_hao, roll_3_coins
    from .bazi_engine import calculate_bazi
    from .tu_vi_engine import calculate_tu_vi_chart
    from .dan_dao_health import diagnose_dan_dao_health
    from .feng_shui import calculate_feng_shui_period9, MOUNTAINS_24
    from .annual_forecast import calculate_annual_forecast
    from .timing_almanac import scan_target_timing_dates
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from mai_hoa import calculate_mai_hoa_from_time
    from luc_hao import calculate_full_luc_hao, get_hex_classifications
    from coin_toss import calculate_coin_luc_hao, roll_3_coins
    from bazi_engine import calculate_bazi
    from tu_vi_engine import calculate_tu_vi_chart
    from dan_dao_health import diagnose_dan_dao_health
    from feng_shui import calculate_feng_shui_period9, MOUNTAINS_24
    from annual_forecast import calculate_annual_forecast
    from timing_almanac import scan_target_timing_dates

HOUSE_LINE_MAP = {
    1: {"zone": "Nền móng, Giếng nước, Cống ngầm, Trẻ nhỏ", "item": "Móng nhà, nguồn nước, sàn đất"},
    2: {"zone": "Gian bếp, Bếp nấu, Giường ngủ, Nữ gia chủ", "item": "Bếp lò, giường ngủ, bàn ăn"},
    3: {"zone": "Cửa chính, Cổng ngõ, Bậc tam cấp", "item": "Cánh cửa, khung bao, lối vào"},
    4: {"zone": "Lối đi, Cửa sổ, Hành lang, Ban công", "item": "Cửa ngách, ban công, vách ngăn"},
    5: {"zone": "Phòng khách, Trụ cột chính, Nam gia chủ", "item": "Trụ nhà, gian tiếp khách, bàn thờ Thổ Địa"},
    6: {"zone": "Mái nhà, Tầng thượng, Bàn thờ Gia Tiên, Tường rào", "item": "Mái ngói, bàn thờ gia tiên, nóc nhà"}
}

BODY_LINE_MAP = {
    1: {"part": "Bàn chân, Ngón chân, Hạ tiêu", "organ": "Kinh lạc bàn chân, huyệt Dũng Tuyền"},
    2: {"part": "Cẳng chân, Đầu gối, Bàng quang, Tử cung", "organ": "Đầu gối, bắp chân, niệu đạo"},
    3: {"part": "Bụng dưới, Vùng rốn, Thận, Đại tràng", "organ": "Hạ đan điền, ruột già, thận"},
    4: {"part": "Ngực, Bụng trên, Tỳ vị, Gan mật", "organ": "Trung đan điền, dạ dày, lá lách, gan"},
    5: {"part": "Ngực trên, Cổ họng, Tim phổi, Khí quản", "organ": "Thượng đan điền, tim, phế quản, họng"},
    6: {"part": "Đầu, Não bộ, Mắt, Thần kinh trung ương", "organ": "Bách hội, thần trí, ngũ quan"}
}

def cross_health_iching_synthesis(
    birth_dt: datetime,
    eval_dt: Optional[datetime] = None,
    gender: int = 1,
    coin_values: Optional[List[int]] = None,
    question: str = ""
) -> Dict[str, Any]:
    if eval_dt is None:
        eval_dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        
    tc = calculate_time_coordinates(eval_dt)
    health_base = diagnose_dan_dao_health(birth_dt, gender=gender)
    
    if coin_values:
        iching_data = calculate_coin_luc_hao(coin_values, question=question or "Khí cơ tạng phủ")
        pri_hex_name = iching_data["primary_info"][1]
        trans_hex_name = iching_data["trans_info"][1] if iching_data["moving_lines"] else pri_hex_name
        lines = iching_data["lines"]
        moving_lines = iching_data["moving_lines"]
    else:
        mh = calculate_mai_hoa_from_time(tc)
        lh = calculate_full_luc_hao(mh, tc)
        pri_hex_name = lh["hex_name"]
        trans_hex_name = lh["t_hex_name"]
        lines = lh["lines"]
        moving_lines = [lh["moving_line"]] if lh.get("moving_line") else []

    afflicted_zones = []
    for l_num in moving_lines:
        line_info = next((l for l in lines if l.get("line_num") == l_num or l.get("pos") == l_num), None)
        body_info = BODY_LINE_MAP.get(l_num, {})
        afflicted_zones.append({
            "line_num": l_num,
            "body_part": body_info.get("part", ""),
            "organ_focus": body_info.get("organ", ""),
            "relation": (line_info.get("luc_than") or line_info.get("p_relation") or "") if line_info else "",
            "beast": (line_info.get("luc_thu") or line_info.get("p_beast") or "") if line_info else ""
        })

    return {
        "type": "Y_DICH_DONG_NGUYEN",
        "birth_time": birth_dt.strftime("%d/%m/%Y %H:%M"),
        "eval_time": eval_dt.strftime("%d/%m/%Y %H:%M"),
        "bazi_organs": health_base.get("organ_diagnosis", health_base.get("constitutional_zang_fu", {})),
        "constitutional_zang_fu": {
            "excess": health_base["excess_organ"],
            "deficient": health_base["deficient_organ"],
            "elements": health_base["element_balance"]
        },
        "iching_dynamic_scan": {
            "primary_hex": pri_hex_name,
            "transformed_hex": trans_hex_name,
            "moving_lines": moving_lines,
            "afflicted_zones": afflicted_zones
        },
        "alchemy_prescription": health_base["alchemy_guidance"]
    }

def cross_feng_shui_iching_synthesis(
    facing_mountain: str = "Tý",
    birth_year: Optional[int] = None,
    eval_dt: Optional[datetime] = None,
    coin_values: Optional[List[int]] = None,
    question: str = ""
) -> Dict[str, Any]:
    if eval_dt is None:
        eval_dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        
    tc = calculate_time_coordinates(eval_dt)
    fs_base = calculate_feng_shui_period9(facing_mountain=facing_mountain, birth_year=birth_year)
    
    if coin_values:
        iching_data = calculate_coin_luc_hao(coin_values, question=question or "Dương trạch phong thủy")
        pri_hex_name = iching_data["primary_info"][1]
        trans_hex_name = iching_data["trans_info"][1] if iching_data["moving_lines"] else pri_hex_name
        lines = iching_data["lines"]
        moving_lines = iching_data["moving_lines"]
    else:
        mh = calculate_mai_hoa_from_time(tc)
        lh = calculate_full_luc_hao(mh, tc)
        pri_hex_name = lh["hex_name"]
        trans_hex_name = lh["t_hex_name"]
        lines = lh["lines"]
        moving_lines = [lh["moving_line"]] if lh.get("moving_line") else []

    house_zone_insights = []
    scan_lines = moving_lines if moving_lines else [2, 5]
    for l_num in scan_lines:
        line_info = next((l for l in lines if l.get("line_num") == l_num or l.get("pos") == l_num), None)
        z_info = HOUSE_LINE_MAP.get(l_num, {})
        house_zone_insights.append({
            "line_num": l_num,
            "house_zone": z_info.get("zone", ""),
            "affected_item": z_info.get("item", ""),
            "relation": (line_info.get("luc_than") or line_info.get("p_relation") or "") if line_info else "",
            "beast": (line_info.get("luc_thu") or line_info.get("p_beast") or "") if line_info else ""
        })

    return {
        "type": "DUONG_TRACH_DONG_THAI",
        "facing": facing_mountain,
        "sitting": fs_base["sitting"],
        "period9_flying_stars": fs_base,
        "spatial_period9_matrix": fs_base["key_sectors"],
        "personal_cung_phi": fs_base["cung_phi_personal"],
        "iching_spatial_scan": {
            "primary_hex": pri_hex_name,
            "transformed_hex": trans_hex_name,
            "moving_lines": moving_lines,
            "house_zones": house_zone_insights
        }
    }

def format_cross_health_report(res: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append("   ĐẠI BÁO CÁO GIAO THOA: Y DỊCH ĐỒNG NGUYÊN (ĐÔNG Y ✕ KINH DỊCH LỤC HÀO)")
    out.append("   [Nguyên lý: Kinh Dịch làm xương sống 1 chiều soi sáng khí cơ tạng phủ]")
    out.append("================================================================================")
    out.append(f"Hồ sơ bản mệnh: {res['birth_time']} | Thời điểm chẩn đoán: {res['eval_time']}")
    out.append("")
    
    out.append("【I. THỂ CHẤT GỐC TIÊN THIÊN (BÁT TỰ TỨ TRỤ)】")
    eb = res["constitutional_zang_fu"]["elements"]
    out.append(f"  • Ngũ Hành Bản Thể: Kim({eb['Kim']}) | Thủy({eb['Thủy']}) | Mộc({eb['Mộc']}) | Hỏa({eb['Hỏa']}) | Thổ({eb['Thổ']})")
    out.append(f"  • Tạng Phủ Thái Quá: {res['constitutional_zang_fu']['excess']['zang_fu']}")
    out.append(f"  • Tạng Phủ Bất Cập : {res['constitutional_zang_fu']['deficient']['zang_fu']}")
    out.append("")
    
    out.append("【II. KHÍ CƠ ĐỘNG THÁI HẬU THIÊN (KINH DỊCH LỤC HÀO CHIÊM BỆNH)】")
    ic = res["iching_dynamic_scan"]
    out.append(f"  • Quẻ Dịch Khí Cơ: {ic['primary_hex']} --> Biến Quẻ: {ic['transformed_hex']}")
    if ic["afflicted_zones"]:
        out.append("  • Vị Trí Kinh Lạc & Vùng Cơ Thể Đang Biến Động:")
        for z in ic["afflicted_zones"]:
            out.append(f"    - Hào {z['line_num']} [{z['relation']} - {z['beast']}]: Tác động vùng [{z['body_part']}]. Trọng tâm: {z['organ_focus']}.")
    else:
        out.append("  • Quẻ Tĩnh thuần hòa: Khí cơ toàn thân đang ở trạng thái ổn định, không có xung đột cấp tính.")
    out.append("")
    
    out.append("【III. PHƯƠNG ÁN ĐIỀU TỨC & DƯỠNG SINH ĐAN ĐẠO CHUYÊN BIỆT】")
    al = res["alchemy_prescription"]
    out.append(f"  • Phép Thở Lục Tự Quyết: {al['breathing_technique']}")
    out.append(f"  • Ý Thủ Đan Điền: {al['dan_dien_focus']}")
    out.append(f"  • Thảo Dược Hỗ Trợ: {al['herbal_nourishment']}")
    out.append("================================================================================")
    return "\n".join(out)

def format_cross_feng_shui_report(res: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append("   ĐẠI BÁO CÁO GIAO THOA: DƯƠNG TRẠCH ĐỘNG THÁI (HUYỀN KHÔNG VẬN 9 ✕ LỤC HÀO)")
    out.append("   [Nguyên lý: Kinh Dịch làm xương sống 1 chiều định vị đồ vật & góc nhà]")
    out.append("================================================================================")
    out.append(f"Tọa Sơn: {res['sitting']} | Hướng Nhà: {res['facing']}")
    out.append("")
    
    out.append("【I. TRẬN ĐỒ KHÔNG GIAN HUYỀN KHÔNG CỬU TINH VẬN 9】")
    for k, v in res["spatial_period9_matrix"].items():
        out.append(f"  • {k:<25}: {v}")
    out.append("")
    
    if res["personal_cung_phi"]:
        cp = res["personal_cung_phi"]
        out.append("【II. ĐỐI ỨNG BẢN MỆNH GIA CHỦ (BÁT TRẠCH CUNG PHI)】")
        out.append(f"  • Năm sinh: {cp['birth_year']} | Cung Phi: {cp['cung_phi']} ({cp['group']})")
        out.append("")
        
    out.append("【III. ĐỊNH VỊ KHÍ TRƯỜNG TỨC THỜI (LỤC HÀO CHIÊM TRẠCH)】")
    ic = res["iching_spatial_scan"]
    out.append(f"  • Quẻ Trạch Khí: {ic['primary_hex']} --> Biến Quẻ: {ic['transformed_hex']}")
    out.append("  • Chi Tiết Khảo Sát 6 Cung Vị Trong Nhà:")
    for z in ic["house_zones"]:
        out.append(f"    - Hào {z['line_num']} [{z['relation']} - {z['beast']}]: Quản vùng [{z['house_zone']}].")
        out.append(f"      --> Cảnh báo đồ vật/khu vực: {z['affected_item']}.")
    out.append("================================================================================")
    return "\n".join(out)
