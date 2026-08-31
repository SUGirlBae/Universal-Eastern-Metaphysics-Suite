"""
Timing Almanac Module (Định Vị Ứng Kỳ & Trạch Cát Hoàng Đạo Tung Shing)
Canonical implementation based on Hiệp Kỷ Biện Phương Thư & Khổng Minh Lục Diệu:
1. 12 Trực (Thập Nhị Kiến Trừ)
2. 28 Tú (Nhị Thập Bát Tú)
3. 6 Diệu (Khổng Minh Lục Diệu: Đại An, Lưu Niên, Tốc Hỷ, Xích Khẩu, Tiểu Cát, Không Vong)
4. 12 Thần Nhật & Thời Hoàng Đạo / Hắc Đạo
5. Nghi & Kỵ (Auspicious & Taboo Activities)
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

try:
    from .lunar_solar import translate_han_viet, CAN, CHI, LOCAL_TZ
    from .luc_hao import BRANCH_ELEMENTS
except (ImportError, ValueError):
    from lunar_solar import translate_han_viet, CAN, CHI, LOCAL_TZ
    from luc_hao import BRANCH_ELEMENTS

# 12 Trực Translation & Cát Hung
TRUC_MAP = {
    "建": {"name": "Kiến", "nature": "Bình", "desc": "Khởi đầu, xuất hành, nhậm chức; kỵ động thổ lớn"},
    "除": {"name": "Trừ", "nature": "Cát", "desc": "Tẩy uế, trừ tà, khám chữa bệnh, tắm gội thảo dược"},
    "满": {"name": "Mãn", "nature": "Cát", "desc": "Khai trương, nhập trạch, cầu tài, tích lũy, mở kho"},
    "平": {"name": "Bình", "nature": "Bình", "desc": "Bình ổn, hòa giải, tu sửa nhỏ, san bằng"},
    "定": {"name": "Định", "nature": "Cát", "desc": "Ký kết, đính ước, nhập học, định kế hoạch lâu dài"},
    "执": {"name": "Chấp", "nature": "Cát", "desc": "Bắt đầu công việc, xây đắp, trồng trọt, thu giữ"},
    "破": {"name": "Phá", "nature": "Hung", "desc": "Phá dỡ, trừ bỏ đồ cũ, phẫu thuật; đại kỵ cưới hỏi, khai trương"},
    "危": {"name": "Nguy", "nature": "Hung", "desc": "Thận trọng cao độ, kỵ leo cao, xuất hành xa vượt biển"},
    "成": {"name": "Thành", "nature": "Đại Cát", "desc": "Vạn sự thành tựu, khai trương, cưới hỏi, nhập trạch, khai bút"},
    "收": {"name": "Thâu", "nature": "Cát", "desc": "Thu hoạch, thu tiền của, cất giữ bảo vật, thu nợ"},
    "开": {"name": "Khai", "nature": "Đại Cát", "desc": "Khai mở, khai quang pháp khí, khai trương, rước lộc"},
    "闭": {"name": "Bế", "nature": "Bình", "desc": "Đóng cửa tĩnh tu, đắp đê, ngăn ngừa trược khí; kỵ chữa mắt, xuất hành"}
}

# 28 Tú Translation
XIU_MAP = {
    "角": "Giác (Mộc - Cát)", "亢": "Cang (Kim - Hung)", "氐": "Đê (Thổ - Hung)", "房": "Phòng (Nhật - Đại Cát)",
    "心": "Tâm (Nguyệt - Hung)", "尾": "Vĩ (Hỏa - Cát)", "箕": "Cơ (Thủy - Cát)", "斗": "Đẩu (Mộc - Cát)",
    "牛": "Ngưu (Kim - Hung)", "女": "Nữ (Thổ - Hung)", "虚": "Hư (Nhật - Hung)", "危": "Nguy (Nguyệt - Hung)",
    "室": "Thất (Hỏa - Cát)", "壁": "Bích (Thủy - Đại Cát)", "奎": "Khuê (Mộc - Hung)", "娄": "Lâu (Kim - Cát)",
    "胃": "Vị (Thổ - Cát)", "昂": "Mão (Nhật - Hung)", "毕": "Tất (Nguyệt - Đại Cát)", "觜": "Chủy (Hỏa - Hung)",
    "参": "Sâm (Thủy - Cát)", "井": "Tỉnh (Mộc - Cát)", "鬼": "Quỷ (Kim - Hung)", "柳": "Liễu (Thổ - Hung)",
    "星": "Tinh (Nhật - Hung)", "张": "Trương (Nguyệt - Cát)", "翼": "Dực (Hỏa - Hung)", "轸": "Chẩn (Thủy - Cát)"
}

# Lục Diệu (Khổng Minh Lục Diệu)
LUC_DIEU_LIST = [
    "Đại An (Cát - Bình an, cầu tài hướng Tây Nam, gia đạo êm ấm)",
    "Lưu Niên (Hung - Trì trệ, việc khó thành ngay, cần nhẫn nại)",
    "Tốc Hỷ (Cát - Tin vui đến nhanh, cầu tài buổi sáng, hòa hợp)",
    "Xích Khẩu (Hung - Khẩu thiệt thị phi, tranh chấp, phòng cãi vã)",
    "Tiểu Cát (Cát - Quý nhân trợ lực, giao dịch thông thuận, bình an)",
    "Không Vong (Hung - Trống rỗng, tổn thất, kỵ mưu sự lớn)"
]

# 12 Thần Nhật Hoàng Đạo / Hắc Đạo
TIANSHEN_MAP = {
    "青龙": "Thanh Long (Hoàng Đạo - Đại Cát)",
    "明堂": "Minh Đường (Hoàng Đạo - Đại Cát)",
    "天刑": "Thiên Hình (Hắc Đạo - Kỵ kiện tụng/tranh chấp)",
    "朱雀": "Chu Tước (Hắc Đạo - Kỵ khẩu thiệt)",
    "金匮": "Kim Quỹ (Hoàng Đạo - Tài lộc/Phúc đức)",
    "天德": "Thiên Đức (Hoàng Đạo - Vạn sự thông)",
    "白虎": "Bạch Hổ (Hắc Đạo - Kỵ xuất hành xa)",
    "玉堂": "Ngọc Đường (Hoàng Đạo - Khai bút/Học hành)",
    "天牢": "Thiên Lao (Hắc Đạo - Trì trệ)",
    "玄武": "Huyền Vũ (Hắc Đạo - Kỵ thị phi)",
    "司命": "Tư Mệnh (Hoàng Đạo - An cư/Bảo hộ)",
    "勾陈": "Câu Trần (Hắc Đạo - Kỵ dời đổi)"
}

# Yi / Ji action translation mapping
YI_JI_MAP = {
    "嫁娶": "Cưới hỏi", "纳采": "Dạm ngõ", "订盟": "Đính ước", "祭祀": "Tế tự / Cúng bái",
    "祈福": "Cầu phúc", "斋醮": "Làm lễ / Trai đàn", "普渡": "Phổ độ / Cầu siêu", "移徙": "Chuyển nhà",
    "入宅": "Nhập trạch", "出行": "Xuất hành", "安机械": "Lắp máy móc", "开光": "Khai quang điểm nhãn",
    "修造": "Tu sửa", "动土": "Động thổ", "竖柱": "Dựng cột", "上梁": "Cất nóc", "盖屋": "Lợp nhà",
    "起基": "Lập nền", "安门": "Lắp cửa", "安葬": "An táng", "破土": "Phá thổ", "开市": "Khai trương",
    "立券": "Ký hợp đồng", "交易": "Giao dịch", "置产": "Mua tài sản", "求医": "Khám chữa bệnh / Tìm thầy thuốc",
    "治病": "Trị bệnh", "沐浴": "Tắm gội tẩy trược", "理发": "Cắt tóc", "扫舍": "Quét dọn nhà cửa",
    "作灶": "Đặt bếp", "造桥": "Làm cầu", "开仓": "Mở kho", "出货财": "Xuất hàng",
    "经络": "Khai thông kinh lạc", "行丧": "Hành tang", "馀事勿取": "Các việc khác không nên làm",
    "诸事不宜": "Trăm việc đều nên kiêng dè", "掘井": "Đào giếng", "开渠": "Đào mương",
    "安床": "Kê giường", "纳畜": "Nuôi gia súc", "伐木": "Đốn cây", "栽种": "Trồng trọt"
}

def translate_actions(action_list: List[str]) -> List[str]:
    return [YI_JI_MAP.get(a, a) for a in action_list]

def calculate_luc_dieu(lunar_month: int, lunar_day: int) -> str:
    """Tính Lục Diệu từ Tháng và Ngày Âm lịch."""
    month_start = (lunar_month - 1) % 6
    day_idx = (month_start + lunar_day - 1) % 6
    return LUC_DIEU_LIST[day_idx]

def calculate_timing_almanac(dt: datetime) -> Dict[str, Any]:
    """
    Tính toán Trạch Cát Hoàng Lịch Tung Shing cho một mốc thời gian cụ thể.
    """
    from lunar_python import Solar, Lunar
    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    lunar = solar.getLunar()
    
    day_can_chi = translate_han_viet(lunar.getDayInGanZhi())
    truc_raw = lunar.getZhiXing()
    truc_info = TRUC_MAP.get(truc_raw, {"name": truc_raw, "nature": "Bình", "desc": ""})
    
    xiu_raw = lunar.getXiu()
    xiu_name = XIU_MAP.get(xiu_raw, xiu_raw)
    
    luc_dieu_str = calculate_luc_dieu(abs(lunar.getMonth()), lunar.getDay())
    
    raw_shen = lunar.getDayTianShen()
    shen_type = lunar.getDayTianShenType()
    is_hoang_dao = "黄道" in shen_type or "Hoàng Đạo" in shen_type or raw_shen in ["青龙", "明堂", "金匮", "天德", "玉堂", "司命"]
    hoang_dao_str = TIANSHEN_MAP.get(raw_shen, f"{translate_han_viet(raw_shen)} ({'Hoàng Đạo' if is_hoang_dao else 'Hắc Đạo'})")
    
    yi_list = translate_actions(list(lunar.getDayYi())[:8])
    ji_list = translate_actions(list(lunar.getDayJi())[:6])
    
    return {
        "solar_datetime": dt.strftime("%d/%m/%Y %H:%M"),
        "lunar_date": f"{lunar.getDay():02d}/{abs(lunar.getMonth()):02d}/{lunar.getYear()}",
        "day_can_chi": day_can_chi,
        "truc_12": f"{truc_info['name']} [{truc_info['nature']}] - {truc_info['desc']}",
        "truc": truc_info,
        "tu_28": xiu_name,
        "sao_xiu": xiu_name,
        "luc_dieu": luc_dieu_str,
        "hoang_dao_than": hoang_dao_str,
        "is_hoang_dao": is_hoang_dao,
        "auspicious_activities": yi_list,
        "taboo_activities": ji_list,
        "yi": yi_list,
        "ji": ji_list
    }

def scan_target_timing_dates(start_dt: datetime, target_branches: List[str], days_limit: int = 45) -> List[Dict[str, Any]]:
    """Quét tìm các ngày ứng kỳ phù hợp với các Địa Chi mục tiêu."""
    from lunar_python import Solar, Lunar
    
    results = []
    current_dt = start_dt
    
    for i in range(1, days_limit + 1):
        test_dt = current_dt + timedelta(days=i)
        solar = Solar.fromYmdHms(test_dt.year, test_dt.month, test_dt.day, 12, 0, 0)
        lunar = solar.getLunar()
        
        day_can_chi = translate_han_viet(lunar.getDayInGanZhi())
        day_chi = day_can_chi.split()[1] if len(day_can_chi.split()) > 1 else ""
        
        if day_chi in target_branches:
            almanac = calculate_timing_almanac(test_dt)
            
            # Scan auspicious hours for this day
            good_hours = []
            for h in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]:
                h_solar = Solar.fromYmdHms(test_dt.year, test_dt.month, test_dt.day, h, 0, 0)
                h_lunar = h_solar.getLunar()
                h_canchi = translate_han_viet(h_lunar.getTimeInGanZhi())
                h_raw_shen = h_lunar.getTimeTianShen()
                h_shen = TIANSHEN_MAP.get(h_raw_shen, translate_han_viet(h_raw_shen))
                h_type = h_lunar.getTimeTianShenType()
                if "黄道" in h_type or "Hoàng Đạo" in h_type or h_raw_shen in ["青龙", "明堂", "金匮", "天德", "玉堂", "司命"]:
                    good_hours.append(f"{h_canchi} ({h:02d}:00-{(h+2)%24:02d}:00 - {h_shen})")
                    
            results.append({
                "solar_date": test_dt.strftime("%d/%m/%Y"),
                "lunar_date": almanac["lunar_date"],
                "day_can_chi": day_can_chi,
                "target_branch": day_chi,
                "truc": almanac["truc"],
                "truc_12": almanac["truc_12"],
                "sao_xiu": almanac["tu_28"],
                "tu_28": almanac["tu_28"],
                "luc_dieu": almanac["luc_dieu"],
                "hoang_dao": almanac["hoang_dao_than"],
                "hoang_dao_than": almanac["hoang_dao_than"],
                "is_hoang_dao": almanac["is_hoang_dao"],
                "yi": almanac["yi"],
                "ji": almanac["ji"],
                "auspicious_activities": almanac["yi"],
                "taboo_activities": almanac["ji"],
                "good_hours": good_hours[:4]
            })
            
            if len(results) >= 3:
                break
                
    return results

def format_timing_almanac_report(timing_dates: List[Dict[str, Any]], context_reason: str = "") -> str:
    if not timing_dates:
        return "Không tìm thấy mốc ngày phù hợp trong khoảng quét 45 ngày."
        
    out = []
    out.append("=== ĐỊNH VỊ ỨNG KỲ THỰC CHIẾN & TRẠCH CÁT HOÀNG ĐẠO (TUNG SHING) ===")
    if context_reason:
        out.append(f"• Cơ sở Dịch lý: {context_reason}")
    out.append("")
    
    for idx, d in enumerate(timing_dates, 1):
        nature_tag = f"[{d['truc']['nature'].upper()}]" if isinstance(d.get('truc'), dict) and d['truc'].get('nature') else ""
        out.append(f"【MỐC {idx}: NGÀY {d['day_can_chi'].upper()} — {nature_tag}】")
        out.append(f"  • Dương Lịch: {d['solar_date']} | Âm Lịch: {d['lunar_date']}")
        out.append(f"  • Trực: {d.get('truc_12', d.get('truc', {}).get('name', ''))} | Sao: {d.get('tu_28', d.get('sao_xiu', ''))}")
        out.append(f"  • Lục Diệu: {d.get('luc_dieu', '')}")
        out.append(f"  • Thần Nhật: {d.get('hoang_dao_than', d.get('hoang_dao', ''))}")
        if d.get('yi') or d.get('auspicious_activities'):
            out.append(f"  • Việc Nên Làm (Nghi): {', '.join(d.get('yi', d.get('auspicious_activities', [])))}")
        if d.get('ji') or d.get('taboo_activities'):
            out.append(f"  • Việc Kiêng Kỵ (Kỵ): {', '.join(d.get('ji', d.get('taboo_activities', [])))}")
        if d.get('good_hours'):
            out.append(f"  • Khung Giờ Hoàng Đạo Đại Cát: {'; '.join(d['good_hours'])}")
        out.append("")
        
    return "\n".join(out)
