"""
Daoist Inner Alchemy (Đan Đạo Dưỡng Sinh) & Five Zang-Fu Organs Diagnosis Engine
Canonical implementation based on Chu Dịch Tham Đồng Khế (Ngụy Bá Dương), Hoàng Đế Nội Kinh,
Tính Mệnh Khuê Chỉ, Biển Thước Nạn Kinh, and Dược Tính Chỉ Nam:
1. 12 Tịch Quái (Sự Tiêu Trưởng Khí Cơ Âm Dương)
2. Tý Ngọ Lưu Chú & Vận Hành Kinh Lạc 12 Canh Giờ
3. Lục Tự Quyết (Hư, Ha, Hô, Si, Xuy, Hí)
4. Dẫn Hỏa Quy Nguyên (Khai Uất - Tả Nhiệt - Hạ Hành)
5. Chẩn Đoán Ngũ Hành Tạng Phủ từ Tứ Trụ Bát Tự
"""
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import json

try:
    from .bazi_engine import calculate_bazi
    from .luc_hao import calculate_full_luc_hao
    from .mai_hoa import calculate_mai_hoa_from_time
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
except (ImportError, ValueError):
    from bazi_engine import calculate_bazi
    from luc_hao import calculate_full_luc_hao
    from mai_hoa import calculate_mai_hoa_from_time
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ

# 12 Tịch Quái Tham Đồng Khế (Âm Dương Tiêu Trưởng)
TICH_QUAI_12 = {
    11: {"branch": "Tý", "tiet_khi": "Đông Chí", "hex_name": "Địa Lôi Phục", "state": "Nhất Dương Sơ Động (1 Dương sơ sinh)", "advice": "Tĩnh tọa hồi quang, giữ ấm Đan Điền, tích tụ dương khí sơ khởi."},
    12: {"branch": "Sửu", "tiet_khi": "Đại Hàn", "hex_name": "Địa Trạch Lâm", "state": "Nhị Dương Tăng Trưởng (2 Dương)", "advice": "Bồi hoàn nguyên tinh, tích lũy chân khí, tránh hao tổn."},
    1:  {"branch": "Dần", "tiet_khi": "Lập Xuân", "hex_name": "Địa Thiên Thái", "state": "Tam Dương Khai Thái (3 Dương)", "advice": "Khí cơ thư thái, sơ can lý khí, vận động nhẹ nhàng đón xuân."},
    2:  {"branch": "Mão", "tiet_khi": "Xuân Phân", "hex_name": "Lôi Thiên Đại Tráng", "state": "Tứ Dương Thịnh Vượng (4 Dương)", "advice": "Quân bình âm dương, dưỡng can mộc, thanh lọc cơ thể."},
    3:  {"branch": "Thìn", "tiet_khi": "Thanh Minh", "hex_name": "Trạch Thiên Quải", "state": "Ngũ Dương Cực Thịnh (5 Dương)", "advice": "Tẩy trược trừ độc, thanh lọc thân tâm, mở rộng kinh mạch."},
    4:  {"branch": "Tỵ", "tiet_khi": "Lập Hạ", "hex_name": "Bát Thuần Càn", "state": "Lục Dương Thuần Dương (6 Dương)", "advice": "Dương khí cực thịnh, đề phòng nhiệt thịnh hao tâm dịch, bổ âm giữ hỏa."},
    5:  {"branch": "Ngọ", "tiet_khi": "Hạ Chí", "hex_name": "Thiên Phong Cấu", "state": "Nhất Âm Sơ Động (1 Âm sơ sinh)", "advice": "Tránh tham đồ mát lạnh, dưỡng tâm an thần, nghỉ trưa điều tức."},
    6:  {"branch": "Mùi", "tiet_khi": "Đại Thử", "hex_name": "Thiên Sơn Độn", "state": "Nhị Âm Tăng Trưởng (2 Âm)", "advice": "Kiện tỳ dưỡng vị, trừ thấp nhiệt mùa hạ, thu liễm tâm thần."},
    7:  {"branch": "Thân", "tiet_khi": "Lập Thu", "hex_name": "Thiên Địa Bĩ", "state": "Tam Âm (Âm Dương Giao Biên, 3 Âm)", "advice": "Thu liễm phế khí, dưỡng phế âm, an định tinh thần."},
    8:  {"branch": "Dậu", "tiet_khi": "Thu Phân", "hex_name": "Phong Địa Quán", "state": "Tứ Âm Vượng (4 Âm)", "advice": "Dưỡng phế kim, phòng ngừa táo tà khí, uống nước thảo dược."},
    9:  {"branch": "Tuất", "tiet_khi": "Sương Giáng", "hex_name": "Sơn Địa Bác", "state": "Ngũ Âm Thịnh (5 Âm)", "advice": "Bổ thận nạp khí, giữ ấm tạng phủ, phòng phong hàn."},
    10: {"branch": "Hợi", "tiet_khi": "Lập Đông", "hex_name": "Bát Thuần Khôn", "state": "Lục Âm Thuần Âm (6 Âm)", "advice": "Bế tàng nguyên khí, dưỡng tinh tích lực, ngủ sớm dậy muộn."}
}

# Tý Ngọ Lưu Chú (12 Canh Giờ và 12 Kinh Lạc)
TY_NGO_LUU_CHU = {
    "Tý (23h00 - 01h00)": {"meridian": "Đởm Kinh (Túi Mật)", "action": "Phải ngủ say để túi mật thanh lọc dịch mật, tái tạo tủy."},
    "Sửu (01h00 - 03h00)": {"meridian": "Can Kinh (Gan)", "action": "Gan tàng huyết và thải độc tối đa; cần giấc ngủ sâu tuyệt đối."},
    "Dần (03h00 - 05h00)": {"meridian": "Phế Kinh (Phổi)", "action": "Phổi phân phối khí huyết toàn thân; thức dậy tập thở sâu, điều tức."},
    "Mão (05h00 - 07h00)": {"meridian": "Đại Trường (Ruột Già)", "action": "Uống nước ấm, bài tiết độc tố đường tiêu hóa."},
    "Thìn (07h00 - 09h00)": {"meridian": "Vị Kinh (Dạ Dày)", "action": "Thời điểm tiêu hóa tốt nhất; ăn sáng ấm nóng đầy đủ dinh dưỡng."},
    "Tỵ (09h00 - 11h00)": {"meridian": "Tỳ Kinh (Lá Lách)", "action": "Tỳ vận hóa dưỡng chất; não bộ tập trung làm việc hiệu quả nhất."},
    "Ngọ (11h00 - 13h00)": {"meridian": "Tâm Kinh (Tim)", "action": "Nghỉ trưa ngắn (15-30 phút) để dưỡng tâm khí, bình ổn huyết áp."},
    "Mùi (13h00 - 15h00)": {"meridian": "Tiểu Trường (Ruột Non)", "action": "Phân thanh giáng trược, hấp thu dưỡng chất, uống nước thanh nhiệt."},
    "Thân (15h00 - 17h00)": {"meridian": "Bàng Quang Kinh", "action": "Thải độc niệu quản; vận động nhẹ nhàng, uống nước bổ sung."},
    "Dậu (17h00 - 19h00)": {"meridian": "Thận Kinh (Thận/Tủy)", "action": "Thận tàng tinh sinh tủy; ăn tối thanh đạm, tránh làm việc quá sức."},
    "Tuất (19h00 - 21h00)": {"meridian": "Tâm Bào Kinh (Màng Tim)", "action": "Bảo vệ tâm hỏa; thư giãn tinh thần, nghe nhạc nhẹ, trò chuyện."},
    "Hợi (21h00 - 23h00)": {"meridian": "Tam Tiêu Kinh", "action": "Thông suốt thượng - trung - hạ tiêu; chuẩn bị nhập giấc ngủ an lành."}
}

# Ngũ Tạng Bản Thể & Lục Tự Quyết
ZANG_FU_MAP = {
    "Mộc": {
        "zang": "Can (Gan)", "fu": "Đởm (Mật)", "tissue": "Gân cốt, Móng", "sense": "Mắt",
        "emotion": "Giận dữ (Nộ)", "flavour": "Chua", "season": "Mùa Xuân",
        "breathing": "Hư tự quyết (Xuy/Hư khí trừ can hỏa uất)", "herb_guide": "Sài Hồ, Bạch Thược, Câu Kỷ Tử"
    },
    "Hỏa": {
        "zang": "Tâm (Tim)", "fu": "Tiểu Trường (Ruột non)", "tissue": "Huyết mạch, Sắc mặt", "sense": "Lưỡi",
        "emotion": "Mừng quá hóa loạn (Hỷ)", "flavour": "Đắng", "season": "Mùa Hạ",
        "breathing": "Ha tự quyết (Thổi tâm hỏa, trừ nhiệt phiền)", "herb_guide": "Đan Sâm, Toan Táo Nhân, Viễn Chí"
    },
    "Thổ": {
        "zang": "Tỳ (Lá lách)", "fu": "Vị (Dạ dày)", "tissue": "Cơ nhục, Môi miệng", "sense": "Miệng",
        "emotion": "Lo nghĩ suy tư (Ưu/Tư)", "flavour": "Ngọt", "season": "Trưởng Hạ (Giao mùa)",
        "breathing": "Hô tự quyết (Kiện tỳ hóa thấp, ấm bụng)", "herb_guide": "Bạch Truật, Phục Linh, Hoài Sơn"
    },
    "Kim": {
        "zang": "Phế (Phổi)", "fu": "Đại Trường (Ruột già)", "tissue": "Bì mao (Da lông)", "sense": "Mũi",
        "emotion": "Bi thương, Sầu muộn (Bi/Ưu)", "flavour": "Cay", "season": "Mùa Thu",
        "breathing": "Si tự quyết (Nhuận phế chỉ khái, ích khí)", "herb_guide": "Hoàng Kỳ, Sa Sâm, Mạch Môn"
    },
    "Thủy": {
        "zang": "Thận (Thận/Tủy)", "fu": "Bàng Quang", "tissue": "Xương tủy, Răng, Tóc", "sense": "Tai",
        "emotion": "Kinh hãi, Sợ hãi (Khủng/Kinh)", "flavour": "Mặn", "season": "Mùa Đông",
        "breathing": "Xuy tự quyết (Ích thận thủy, ấm lưng gối)", "herb_guide": "Thục Địa, Đỗ Trọng, Ba Kích"
    }
}

CAN_ELEMENT = {"Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa", "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim", "Nhâm": "Thủy", "Quý": "Thủy"}
CHI_ELEMENT = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}

def get_current_meridian_hour(hour: int) -> Tuple[str, Dict[str, str]]:
    """Xác định kinh lạc đương lệnh theo giờ hiện tại."""
    if hour == 23 or hour == 0: key = "Tý (23h00 - 01h00)"
    elif hour in [1, 2]: key = "Sửu (01h00 - 03h00)"
    elif hour in [3, 4]: key = "Dần (03h00 - 05h00)"
    elif hour in [5, 6]: key = "Mão (05h00 - 07h00)"
    elif hour in [7, 8]: key = "Thìn (07h00 - 09h00)"
    elif hour in [9, 10]: key = "Tỵ (09h00 - 11h00)"
    elif hour in [11, 12]: key = "Ngọ (11h00 - 13h00)"
    elif hour in [13, 14]: key = "Mùi (13h00 - 15h00)"
    elif hour in [15, 16]: key = "Thân (15h00 - 17h00)"
    elif hour in [17, 18]: key = "Dậu (17h00 - 19h00)"
    elif hour in [19, 20]: key = "Tuất (19h00 - 21h00)"
    else: key = "Hợi (21h00 - 23h00)"
    return key, TY_NGO_LUU_CHU[key]

def calculate_dan_dao_health(dt: datetime, gender: int = 1) -> Dict[str, Any]:
    """
    Tính toán chẩn đoán Đan Đạo Dưỡng Sinh & Ngũ Tạng Tạng Phủ theo chuẩn canonical.
    """
    from lunar_python import Solar, Lunar
    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    lunar = solar.getLunar()
    
    lunar_month = abs(lunar.getMonth())
    tich_quai_data = TICH_QUAI_12.get(lunar_month, TICH_QUAI_12[1])
    
    hour_key, cur_meridian = get_current_meridian_hour(dt.hour)
    
    # Tính Bát Tự để chẩn đoán Ngũ Hành Tạng Phủ
    bazi = calculate_bazi(dt, gender=gender)
    elem_counts = {"Kim": 0, "Thủy": 0, "Mộc": 0, "Hỏa": 0, "Thổ": 0}
    for p_key, p_data in bazi["pillars"].items():
        cc = p_data.get("can_chi", "").split()
        if len(cc) == 2:
            can, chi = cc[0], cc[1]
            if can in CAN_ELEMENT: elem_counts[CAN_ELEMENT[can]] += 1
            if chi in CHI_ELEMENT: elem_counts[CHI_ELEMENT[chi]] += 1
            
    sorted_elems = sorted(elem_counts.items(), key=lambda x: x[1], reverse=True)
    strongest_elem = sorted_elems[0][0]
    weakest_elem = sorted_elems[-1][0]
    
    zang_strong = ZANG_FU_MAP[strongest_elem]
    zang_weak = ZANG_FU_MAP[weakest_elem]
    
    # Phác đồ Dẫn Hỏa Quy Nguyên
    dan_hoa_quy_nguyen = {
        "phap_do": "Khai Uất - Tả Nhiệt - Hạ Hành Quy Thận Thủy",
        "huyet_dao": "Day bấm Đản Trung/Nội Quan (3 phút) -> Tả nhiệt Hợp Cốc -> Ý thủ Dũng Tuyền/Khí Hải",
        "khi_quyet": "Thở Xuy tự quyết chậm sâu (36 lần) để dẫn hỏa quy về thận thủy, hạ nhiệt bốc đầu."
    }
    
    luc_tu_quyet_prescription = f"Tập trung âm '{zang_weak['breathing']}' để bồi bổ tạng {zang_weak['zang']}; phối hợp 'Hí' tự quyết thông suốt Tam Tiêu."
    
    return {
        "datetime": dt.strftime("%d/%m/%Y %H:%M"),
        "tich_quai": f"{tich_quai_data['hex_name']} ({tich_quai_data['state']})",
        "tiet_khi": tich_quai_data["tiet_khi"],
        "tich_quai_advice": tich_quai_data["advice"],
        "ty_ngo_luu_chu": {
            "current_hour": hour_key,
            "active_meridian": cur_meridian["meridian"],
            "guidance": cur_meridian["action"],
            "all_schedule": TY_NGO_LUU_CHU
        },
        "luc_tu_quyet": luc_tu_quyet_prescription,
        "dan_hoa_quy_nguyen": dan_hoa_quy_nguyen,
        "organ_diagnosis": {
            "element_balance": elem_counts,
            "excess_organ": f"{zang_strong['zang']} ({strongest_elem})",
            "deficient_organ": f"{zang_weak['zang']} ({weakest_elem})",
            "weak_manifestation": f"Cần chú ý vùng {zang_weak['tissue']}, vùng cảm giác ({zang_weak['sense']}).",
            "herb_support": zang_weak["herb_guide"]
        },
        "bazi_profile": bazi.get("condensed_profile", ""),
        "element_balance": elem_counts,
        "excess_organ": {
            "element": strongest_elem,
            "zang_fu": f"{zang_strong['zang']} / {zang_strong['fu']}",
            "manifestation": f"Dễ căng thẳng vùng {zang_strong['tissue']}, cảm xúc {zang_strong['emotion']} vượng."
        },
        "deficient_organ": {
            "element": weakest_elem,
            "zang_fu": f"{zang_weak['zang']} / {zang_weak['fu']}",
            "manifestation": f"Cần lưu ý bồi bổ {zang_weak['tissue']}, vùng cảm giác ({zang_weak['sense']})."
        },
        "alchemy_guidance": {
            "truc_co_stage": "Bách Nhật Trúc Cơ: Bồi hoàn nguyên tinh, điều tức an thần.",
            "breathing_technique": f"Lục Tự Khí Quyết: {luc_tu_quyet_prescription}",
            "dan_dien_focus": "Hạ Đan Điền (Khí Hải) - Ngưng Thần Nhập Khí Huyệt.",
            "auspicious_hours": [
                "Giờ Tý (23h00 - 01h00): Nhất Dương Sơ Sinh, Đan Điền phát hỏa.",
                "Giờ Ngọ (11h00 - 13h00): Nhất Âm Sơ Sinh, Thủy Hỏa Ký Tế."
            ],
            "herbal_nourishment": f"Bổ trợ: {zang_weak['herb_guide']}."
        }
    }

def diagnose_dan_dao_health(dt: datetime, gender: int = 1) -> Dict[str, Any]:
    """Hàm tương thích giao diện cũ."""
    return calculate_dan_dao_health(dt, gender)

def format_dan_dao_health_report(res: Dict[str, Any]) -> str:
    out = []
    out.append("================================================================================")
    out.append("   CHẨN ĐOÁN KHÍ CƠ TẠNG PHỦ & HƯỚNG DẪN DƯỠNG SINH ĐAN ĐẠO (DAOIST ALCHEMY)")
    out.append("================================================================================")
    out.append(f"Thời gian chẩn đoán: {res['datetime']}")
    out.append(f"Khí Cơ Vũ Trụ (Tham Đồng Khế 12 Tịch Quái): 【{res.get('tich_quai', '')}】 - Tiết {res.get('tiet_khi', '')}")
    out.append(f"• Chỉ dẫn: {res.get('tich_quai_advice', '')}")
    out.append("")
    
    tng = res.get("ty_ngo_luu_chu", {})
    out.append(f"【I. TÝ NGỌ LƯU CHÚ HIỆN TẠI — {tng.get('current_hour', '')}】")
    out.append(f"  • Kinh Lạc Đương Lệnh: {tng.get('active_meridian', '')}")
    out.append(f"  • Chỉ Dẫn Dưỡng Sinh : {tng.get('guidance', '')}")
    out.append("")
    
    out.append("【II. TƯƠNG QUAN NGŨ HÀNH TẠNG PHỦ】")
    eb = res.get("element_balance", {})
    out.append(f"  • Phân bổ Ngũ Hành: Kim({eb.get('Kim', 0)}) | Thủy({eb.get('Thủy', 0)}) | Mộc({eb.get('Mộc', 0)}) | Hỏa({eb.get('Hỏa', 0)}) | Thổ({eb.get('Thổ', 0)})")
    out.append(f"  • Tạng Phủ Thái Quá (Vượng): Hành {res['excess_organ']['element']} -> {res['excess_organ']['zang_fu']}")
    out.append(f"    --> Biểu hiện: {res['excess_organ']['manifestation']}")
    out.append(f"  • Tạng Phủ Bất Cập (Suy/Thiếu): Hành {res['deficient_organ']['element']} -> {res['deficient_organ']['zang_fu']}")
    out.append(f"    --> Cảnh báo: {res['deficient_organ']['manifestation']}")
    out.append("")
    
    out.append("【III. PHƯƠNG PHÁP ĐIỀU TỨC & DƯỠNG SINH ĐAN ĐẠO (TÍNH MỆNH KHUÊ CHỈ)】")
    ag = res.get("alchemy_guidance", {})
    out.append(f"  • Giai Đoạn Công Phu: {ag.get('truc_co_stage', '')}")
    out.append(f"  • Phép Thở Lục Tự Quyết: {res.get('luc_tu_quyet', ag.get('breathing_technique', ''))}")
    out.append(f"  • Ý Thủ Đan Điền: {ag.get('dan_dien_focus', '')}")
    out.append(f"  • Dẫn Hỏa Quy Nguyên: {res.get('dan_hoa_quy_nguyen', {}).get('huyet_dao', '')}")
    out.append(f"  • Dược Thảo Dưỡng Sinh Đông Y: {ag.get('herbal_nourishment', '')}")
    out.append("================================================================================")
    return "\n".join(out)
