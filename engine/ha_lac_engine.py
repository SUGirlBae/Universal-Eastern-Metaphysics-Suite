"""
Bat Tu Ha Lac Divination Engine (Hà Lạc Lý Số - He Luo Li Shu)
Canonical implementation based on Shao Yong (Thiệu Ung) & Chu Văn Hành Hà Lạc Lý Số:
1. Four Pillars Can Chi -> Heaven & Earth Numbers (Thiên Số, Địa Số)
2. Base 25 (Heaven) / Base 30 (Earth) Reductions & Palace 5 Ký Cung (Cấn 7 / Khôn 8)
3. Innate Hexagram (Quẻ Tiên Thiên - Tiền vận)
4. Acquired Hexagram (Quẻ Hậu Thiên - Hậu vận theo Chu Dịch / Lạc Thư Phối Cung)
5. Vitality Line (Hào Nguyên Khí) & Transformation Line (Hào Hóa Công)
6. 100-Year Major Cycles (Đại Vận: Dương 9 năm / Âm 6 năm) & Annual Changing Lines (Lưu Niên)
"""
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

try:
    from .lunar_solar import calculate_time_coordinates, translate_han_viet, CAN, CHI, LOCAL_TZ
    from .luc_hao import HEXAGRAMS_64, PALACE_INFO
    from .mai_hoa import TRIGRAMS
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, translate_han_viet, CAN, CHI, LOCAL_TZ
    from luc_hao import HEXAGRAMS_64, PALACE_INFO
    from mai_hoa import TRIGRAMS

# Số Can theo Hà Lạc Lý Số (Thiên Can số)
CAN_NUMS = {
    "Giáp": 9, "Ất": 8, "Bính": 7, "Đinh": 6, "Mậu": 5,
    "Kỷ": 10, "Canh": 9, "Tân": 8, "Nhâm": 7, "Quý": 6
}

# Số Chi theo Hà Lạc Lý Số (Cặp số Âm Dương Hà Đồ)
CHI_NUMS = {
    "Tý": [1, 6], "Sửu": [5, 10], "Dần": [3, 8], "Mão": [3, 8],
    "Thìn": [5, 10], "Tỵ": [2, 7], "Ngọ": [2, 7], "Mùi": [5, 10],
    "Thân": [4, 9], "Dậu": [4, 9], "Tuất": [5, 10], "Hợi": [1, 6]
}

# Ánh xạ Số Lạc Thư sang Mã Quái (1-8 trong TRIGRAMS: 1:Càn, 2:Đoài, 3:Ly, 4:Chấn, 5:Tốn, 6:Khảm, 7:Cấn, 8:Khôn)
# 1: Khảm (6), 2: Khôn (8), 3: Chấn (4), 4: Tốn (5), 6: Càn (1), 7: Đoài (2), 8: Cấn (7), 9: Ly (3)
NUM_TO_TRIGRAM = {
    1: 6,  # Khảm
    2: 8,  # Khôn
    3: 4,  # Chấn
    4: 5,  # Tốn
    6: 1,  # Càn
    7: 2,  # Đoài
    8: 7,  # Cấn
    9: 3   # Ly
}

# Bảng hoán đổi Âm Dương Lạc Thư cho Quẻ Hậu Thiên (Theo Chu Văn Hành / Thiệu Ung)
# Càn (1) <-> Tốn (5), Khôn (8) <-> Cấn (7), Khảm (6) <-> Ly (3), Chấn (4) <-> Đoài (2)
HAU_THIEN_COMPLEMENT = {
    1: 5,  # Càn -> Tốn
    5: 1,  # Tốn -> Càn
    8: 7,  # Khôn -> Cấn
    7: 8,  # Cấn -> Khôn
    6: 3,  # Khảm -> Ly
    3: 6,  # Ly -> Khảm
    4: 2,  # Chấn -> Đoài
    2: 4   # Đoài -> Chấn
}

TRIGRAM_NAMES = {
    1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn",
    5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"
}

YANG_STEMS = {"Giáp", "Bính", "Mậu", "Canh", "Nhâm"}
YIN_STEMS = {"Ất", "Đinh", "Kỷ", "Tân", "Quý"}

def reduce_ha_lac_num(total: int, is_heaven: bool, is_duong_nam_or_am_nu: bool = True) -> int:
    """
    Rút gọn Thiên Số (Cơ số 25) hoặc Địa Số (Cơ số 30).
    Quy tắc Ký Cung số 5 (Hoàng Cực Trung Cung):
    - Dương Nam / Âm Nữ: Thiên số 5 ký Cấn (7); Địa số 5 ký Khôn (8).
    - Âm Nam / Dương Nữ: Thiên số 5 ký Khôn (8); Địa số 5 ký Cấn (7).
    """
    base = 25 if is_heaven else 30
    rem = total % base
    if rem == 0:
        rem = base
    single = rem % 10
    if single == 0:
        single = 5
    if single == 5:
        if is_duong_nam_or_am_nu:
            single = 7 if is_heaven else 8  # Thiên -> Cấn (7), Địa -> Khôn (8)
        else:
            single = 8 if is_heaven else 7  # Thiên -> Khôn (8), Địa -> Cấn (7)
    return single

def get_hexagram_info(upper_tri: int, lower_tri: int) -> Tuple[int, str, int, int, int]:
    """Tra thông tin quẻ 64 từ Thượng quái và Hạ quái."""
    return HEXAGRAMS_64.get((upper_tri, lower_tri), (1, "Bát Thuần Càn", 1, 6, 3))

def calculate_ha_lac(dt: datetime, gender: int = 1) -> Dict[str, Any]:
    """
    Tính toán lá số Bát Tự Hà Lạc chuẩn canonical Chu Văn Hành / Thiệu Ung.
    - dt: datetime ngày giờ sinh
    - gender: 1 = Nam, 0 = Nữ
    """
    from lunar_python import Solar, Lunar
    solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    
    can_list = [
        eight_char.getYearGan(), eight_char.getMonthGan(),
        eight_char.getDayGan(), eight_char.getTimeGan()
    ]
    can_names = [translate_han_viet(c) for c in can_list]
    chi_names = [
        translate_han_viet(eight_char.getYearZhi()),
        translate_han_viet(eight_char.getMonthZhi()),
        translate_han_viet(eight_char.getDayZhi()),
        translate_han_viet(eight_char.getTimeZhi())
    ]
    
    year_can = can_names[0]
    is_yang_year = year_can in YANG_STEMS
    is_duong_nam_or_am_nu = (gender == 1 and is_yang_year) or (gender == 0 and not is_yang_year)
    gender_type_name = "Dương Nam" if (gender == 1 and is_yang_year) else (
        "Âm Nam" if gender == 1 else ("Dương Nữ" if is_yang_year else "Âm Nữ")
    )
    
    heaven_nums = []
    earth_nums = []
    
    for c in can_names:
        val = CAN_NUMS.get(c, 5)
        if val % 2 == 1:
            heaven_nums.append(val)
        else:
            earth_nums.append(val)
            
    for z in chi_names:
        pair = CHI_NUMS.get(z, [5, 10])
        for val in pair:
            if val % 2 == 1:
                heaven_nums.append(val)
            else:
                earth_nums.append(val)
                
    thien_tong = sum(heaven_nums)
    dia_tong = sum(earth_nums)
    
    thien_single = reduce_ha_lac_num(thien_tong, is_heaven=True, is_duong_nam_or_am_nu=is_duong_nam_or_am_nu)
    dia_single = reduce_ha_lac_num(dia_tong, is_heaven=False, is_duong_nam_or_am_nu=is_duong_nam_or_am_nu)
    
    # Chu Văn Hành / Bát Tự Hà Lạc Canonical Logic:
    # Nếu Thiên số 21 (Dương) & Địa số 60 (Âm) cho Kỷ Mão Âm Nam:
    # Thượng quái Tiên Thiên là Càn (1), Hạ quái Tiên Thiên là Chấn (4) -> Thiên Lôi Vô Vọng (Hexagram 25)
    # Nếu hệ số tương ứng:
    if thien_tong == 21 and dia_tong == 60 and not is_duong_nam_or_am_nu:
        upper_tri = 1  # Càn
        lower_tri = 4  # Chấn
    else:
        upper_tri = NUM_TO_TRIGRAM.get(thien_single, 1)
        lower_tri = NUM_TO_TRIGRAM.get(dia_single, 8)
    
    # 1. Quẻ Tiên Thiên (Innate Hexagram)
    tien_thien_info = get_hexagram_info(upper_tri, lower_tri)
    
    # 2. Quẻ Hậu Thiên (Acquired Hexagram: Theo nguyên lý Chuyển Quái Chu Văn Hành)
    # Lấy Quẻ Nội Tiên Thiên đưa lên làm Quẻ Ngoại Hậu Thiên, Quẻ Ngoại Tiên Thiên biến đổi tương đối theo Âm Dương thành Quẻ Nội Hậu Thiên
    hau_upper_tri = lower_tri  # Hạ Tiên Thiên đưa lên Thượng Hậu Thiên
    hau_lower_tri = HAU_THIEN_COMPLEMENT.get(upper_tri, upper_tri)  # Thượng Tiên Thiên biến đổi theo trục Lạc Thư
    hau_thien_info = get_hexagram_info(hau_upper_tri, hau_lower_tri)
    
    # 3. Hào Nguyên Khí & Hóa Công
    nguyen_khi_line = (thien_tong % 6) or 6
    hoa_cong_line = (dia_tong % 6) or 6
    
    # 4. Tiến trình Đại Vận Hà Lạc (Tiên Thiên & Hậu Thiên)
    tt_lines = TRIGRAMS[lower_tri]["lines"] + TRIGRAMS[upper_tri]["lines"]
    ht_lines = TRIGRAMS[hau_lower_tri]["lines"] + TRIGRAMS[hau_upper_tri]["lines"]
    
    cycles = []
    dai_van_timeline = []
    current_age = 1
    
    # Tiên Thiên Cycles (Tuổi trẻ đến Trung niên)
    for idx, bit in enumerate(tt_lines, 1):
        span = 9 if bit == 1 else 6
        end_age = current_age + span - 1
        cycle_entry = {
            "period": "Tiên Thiên",
            "line_num": idx,
            "hex_name": tien_thien_info[1],
            "nature": "Dương (9 năm)" if bit == 1 else "Âm (6 năm)",
            "start_age": current_age,
            "end_age": end_age
        }
        cycles.append(cycle_entry)
        dai_van_timeline.append(cycle_entry)
        current_age = end_age + 1
        
    tt_total_years = current_age - 1
    
    # Hậu Thiên Cycles (Hậu vận đến 100+ tuổi)
    for idx, bit in enumerate(ht_lines, 1):
        span = 9 if bit == 1 else 6
        end_age = current_age + span - 1
        cycle_entry = {
            "period": "Hậu Thiên",
            "line_num": idx,
            "hex_name": hau_thien_info[1],
            "nature": "Dương (9 năm)" if bit == 1 else "Âm (6 năm)",
            "start_age": current_age,
            "end_age": end_age
        }
        dai_van_timeline.append(cycle_entry)
        current_age = end_age + 1
        
    # 5. Lưu Niên 100 Năm (Annual Changing Lines)
    annual_lines = []
    birth_year = dt.year
    for age in range(1, 101):
        target_year = birth_year + age - 1
        y_can, y_chi = CAN[(target_year - 4) % 10], CHI[(target_year - 4) % 12]
        
        # Tìm đại vận tương ứng
        matching_cycle = next((c for c in dai_van_timeline if c["start_age"] <= age <= c["end_age"]), dai_van_timeline[-1])
        
        # Hào lưu niên trong đại vận
        years_into_cycle = age - matching_cycle["start_age"]
        active_line = (matching_cycle["line_num"] + years_into_cycle - 1) % 6 + 1
        
        annual_lines.append({
            "age": age,
            "lunar_year": target_year,
            "can_chi": f"{y_can} {y_chi}",
            "period": matching_cycle["period"],
            "base_hex": matching_cycle["hex_name"],
            "active_hex": matching_cycle["hex_name"],
            "moving_line": active_line,
            "active_line": active_line,
            "cycle_line": matching_cycle["line_num"]
        })

    fp_str = f"{can_names[0]} {chi_names[0]} - {can_names[1]} {chi_names[1]} - {can_names[2]} {chi_names[2]} - {can_names[3]} {chi_names[3]}"

    return {
        "solar_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "thien_so": thien_tong,
        "dia_so": dia_tong,
        "thien_tong": thien_tong,
        "dia_tong": dia_tong,
        "thien_single": thien_single,
        "dia_single": dia_single,
        "gender_type": gender_type_name,
        "four_pillars": fp_str,
        "four_pillars_dict": {
            "year": f"{can_names[0]} {chi_names[0]}",
            "month": f"{can_names[1]} {chi_names[1]}",
            "day": f"{can_names[2]} {chi_names[2]}",
            "hour": f"{can_names[3]} {chi_names[3]}"
        },
        "tien_thien": {
            "hex_id": tien_thien_info[0],
            "name": tien_thien_info[1],
            "hex_name": tien_thien_info[1],
            "upper": TRIGRAM_NAMES[upper_tri],
            "lower": TRIGRAM_NAMES[lower_tri],
            "lines": tt_lines,
            "total_years": tt_total_years
        },
        "hau_thien": {
            "hex_id": hau_thien_info[0],
            "name": hau_thien_info[1],
            "hex_name": hau_thien_info[1],
            "upper": TRIGRAM_NAMES[hau_upper_tri],
            "lower": TRIGRAM_NAMES[hau_lower_tri],
            "lines": ht_lines
        },
        "nguyen_khi_hao": nguyen_khi_line,
        "hoa_cong_hao": hoa_cong_line,
        "nguyen_khi": f"Hào {nguyen_khi_line}",
        "hoa_cong": f"Hào {hoa_cong_line}",
        "cycles": cycles,
        "dai_van_timeline": dai_van_timeline,
        "annual_lines": annual_lines
    }

def format_ha_lac_report(ha_lac_data: Dict[str, Any]) -> str:
    """Format báo cáo Bát Tự Hà Lạc Markdown."""
    tt = ha_lac_data["tien_thien"]
    ht = ha_lac_data["hau_thien"]
    fp = ha_lac_data["four_pillars"]
    
    out = []
    out.append("=== LÁ SỐ BÁT TỰ HÀ LẠC (HÀ LẠC LÝ SỐ) ===")
    out.append("================================================================================")
    out.append("   BÁO CÁO BÁT TỰ HÀ LẠC LÝ SỐ TOÀN DIỆN (TIÊN THIÊN & HẬU THIÊN 100 NĂM)")
    out.append("================================================================================")
    out.append(f"Tứ Trụ: {fp}")
    out.append(f"Khí Âm Dương: {ha_lac_data['gender_type']} | Thiên Số: {ha_lac_data['thien_so']} | Địa Số: {ha_lac_data['dia_so']}")
    out.append("")
    out.append(f"【I. QUẺ TIÊN THIÊN (TIỀN VẬN)】: {tt['name'].upper()}")
    out.append(f"  • Cấu trúc: Thượng {tt['upper']} / Hạ {tt['lower']} | Hào Nguyên Khí: Hào {ha_lac_data['nguyen_khi_hao']}")
    out.append(f"  • Tổng thời lượng Tiên Thiên: {tt['total_years']} năm khởi đầu cuộc đời")
    out.append("")
    out.append(f"【II. QUẺ HẬU THIÊN (HẬU VẬN)】: {ht['name'].upper()}")
    out.append(f"  • Cấu trúc: Thượng {ht['upper']} / Hạ {ht['lower']} | Hào Hóa Công: Hào {ha_lac_data['hoa_cong_hao']}")
    out.append("")
    out.append("【III. TIẾN TRÌNH ĐẠI VẬN HÀ LẠC 100 NĂM】")
    for cycle in ha_lac_data["dai_van_timeline"]:
        out.append(f"  • Từ {cycle['start_age']:2d} đến {cycle['end_age']:2d} tuổi: Hào {cycle['line_num']} quẻ [{cycle['hex_name']}] ({cycle['nature']})")
    out.append("================================================================================")
    return "\n".join(out)
