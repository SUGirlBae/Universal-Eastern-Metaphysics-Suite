"""
Liu Yao Coin Toss Divination Engine (Gieo Quẻ Bằng 3 Đồng Xu Dã Hạc)
Enhanced v4.0.0: Outputs 100% Comprehensive Technical Metadata:
  - Solar & Lunar Date/Time with Four Pillars & Nap Am
  - Accurate Solar Terms, Month/Day Branch Elements & Strengths
  - Day Void (Tuần Không Ngày) & Hour Void (Tuần Không Giờ)
  - Full Daily Shen Sha Table (Quý Nhân, Lộc, Mã, Đào, Hoa Cái, Tướng Tinh, Văn Xương, Thiên Y, Kiếp Sát, Tai Sát)
  - Quai Than (Quải Thần) & The Than
  - Full Phuc Than (Hidden Relatives with Branches, Elements and Host Line)
  - 6-Line Technical Markdown Table with exact metadata for independent user verification.
"""
import random
from typing import List, Tuple, Dict, Any
from datetime import datetime

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .luc_hao import (
        HEXAGRAMS_64, PALACE_INFO, PALACE_QUAI_THAN, TRIGRAM_NA_GIAP,
        BRANCH_ELEMENTS, ELEMENT_RELATIONS, SIX_BEASTS_BY_DAY_CAN,
        get_empty_branches, get_vuong_suy, get_hex_classifications,
        get_full_daily_than_sat, get_line_than_sat_list
    )
    from .atomic_clock import get_precise_atomic_now
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from luc_hao import (
        HEXAGRAMS_64, PALACE_INFO, PALACE_QUAI_THAN, TRIGRAM_NA_GIAP,
        BRANCH_ELEMENTS, ELEMENT_RELATIONS, SIX_BEASTS_BY_DAY_CAN,
        get_empty_branches, get_vuong_suy, get_hex_classifications,
        get_full_daily_than_sat, get_line_than_sat_list
    )
    from atomic_clock import get_precise_atomic_now

TRIGRAM_BITS = {
    1: (1, 1, 1), 2: (1, 1, 0), 3: (1, 0, 1), 4: (1, 0, 0),
    5: (0, 1, 1), 6: (0, 1, 0), 7: (0, 0, 1), 8: (0, 0, 0)
}
BITS_TO_TRIGRAM = {v: k for k, v in TRIGRAM_BITS.items()}

COIN_MAP = {
    6: {"name": "Lão Âm", "is_yang": False, "is_dong": True, "trans_yang": True, "symbol": "━ ━ X"},
    7: {"name": "Thiếu Dương", "is_yang": True, "is_dong": False, "trans_yang": True, "symbol": "━━━"},
    8: {"name": "Thiếu Âm", "is_yang": False, "is_dong": False, "trans_yang": False, "symbol": "━ ━"},
    9: {"name": "Lão Dương", "is_yang": True, "is_dong": True, "trans_yang": False, "symbol": "━━━ O"},
}

def roll_3_coins() -> int:
    c1 = 2 if random.random() < 0.5 else 3
    c2 = 2 if random.random() < 0.5 else 3
    c3 = 2 if random.random() < 0.5 else 3
    return c1 + c2 + c3

def parse_coin_values(coin_values: List[int]) -> Tuple[Tuple[int, int], Tuple[int, int], List[int]]:
    if len(coin_values) != 6:
        raise ValueError(f"Expected 6 coin toss values, got {len(coin_values)}")
        
    primary_bits = []
    trans_bits = []
    moving_lines = []
    
    for idx, val in enumerate(coin_values, 1):
        if val not in COIN_MAP:
            raise ValueError(f"Invalid coin value {val} at line {idx}. Must be 6, 7, 8, or 9.")
        info = COIN_MAP[val]
        primary_bits.append(1 if info["is_yang"] else 0)
        trans_bits.append(1 if info["trans_yang"] else 0)
        if info["is_dong"]:
            moving_lines.append(idx)
            
    pri_lower = BITS_TO_TRIGRAM[tuple(primary_bits[0:3])]
    pri_upper = BITS_TO_TRIGRAM[tuple(primary_bits[3:6])]
    
    trans_lower = BITS_TO_TRIGRAM[tuple(trans_bits[0:3])]
    trans_upper = BITS_TO_TRIGRAM[tuple(trans_bits[3:6])]
    
    return (pri_upper, pri_lower), (trans_upper, trans_lower), moving_lines

def calculate_coin_luc_hao(coin_values: List[int], dt: datetime = None, question: str = "") -> Dict[str, Any]:
    if dt is None:
        atomic_info = get_precise_atomic_now()
        dt = atomic_info["datetime"]
        time_meta = atomic_info
    else:
        time_meta = {"source": "USER_SPECIFIED", "datetime": dt}
        
    time_coords = calculate_time_coordinates(dt)
    (pri_upper, pri_lower), (trans_upper, trans_lower), moving_lines = parse_coin_values(coin_values)
    
    primary_info = HEXAGRAMS_64[(pri_upper, pri_lower)]
    trans_info = HEXAGRAMS_64[(trans_upper, trans_lower)]
    
    lines = []
    palace_id = primary_info[2]
    palace_elem = PALACE_INFO[palace_id]["element"]
    day_can = time_coords["day_can"]
    day_chi = time_coords["day_chi"]
    hour_can = time_coords["can_chi_hour"].split()[0]
    hour_chi = time_coords["can_chi_hour"].split()[1] if len(time_coords["can_chi_hour"].split()) > 1 else "Tý"
    month_chi = time_coords["month_chi"]
    month_elem = BRANCH_ELEMENTS[month_chi]
    beasts = SIX_BEASTS_BY_DAY_CAN.get(day_can, SIX_BEASTS_BY_DAY_CAN["Giáp"])
    quai_than_chi = PALACE_QUAI_THAN.get(palace_id)
    
    # Base pure hexagram Na Giap for Phuc Than
    base_tri = palace_id
    base_inner_can, base_inner_branches, base_outer_can, base_outer_branches = (
        TRIGRAM_NA_GIAP[base_tri][0], TRIGRAM_NA_GIAP[base_tri][1],
        TRIGRAM_NA_GIAP[base_tri][2], TRIGRAM_NA_GIAP[base_tri][3]
    )
    base_cans = [base_inner_can]*3 + [base_outer_can]*3
    base_chis = base_inner_branches + base_outer_branches
    
    # Primary & Trans Na Giap
    pri_inner_can, pri_inner_branches, pri_outer_can, pri_outer_branches = (
        TRIGRAM_NA_GIAP[pri_lower][0], TRIGRAM_NA_GIAP[pri_lower][1],
        TRIGRAM_NA_GIAP[pri_upper][2], TRIGRAM_NA_GIAP[pri_upper][3]
    )
    trans_inner_can, trans_inner_branches, trans_outer_can, trans_outer_branches = (
        TRIGRAM_NA_GIAP[trans_lower][0], TRIGRAM_NA_GIAP[trans_lower][1],
        TRIGRAM_NA_GIAP[trans_upper][2], TRIGRAM_NA_GIAP[trans_upper][3]
    )
    
    pri_cans = [pri_inner_can]*3 + [pri_outer_can]*3
    pri_chis = pri_inner_branches + pri_outer_branches
    trans_cans = [trans_inner_can]*3 + [trans_outer_can]*3
    trans_chis = trans_inner_branches + trans_outer_branches
    
    # Check existing relatives in Primary
    pri_relations = [ELEMENT_RELATIONS[palace_elem][BRANCH_ELEMENTS[c]] for c in pri_chis]
    all_relatives = ["Phụ Mẫu", "Tử Tôn", "Quan Quỷ", "Thê Tài", "Huynh Đệ"]
    missing_relatives = [r for r in all_relatives if r not in pri_relations]
    
    day_kv_list = get_empty_branches(day_can, day_chi)
    hour_kv_list = get_empty_branches(hour_can, hour_chi)
    daily_than_sat = get_full_daily_than_sat(day_can, day_chi, month_chi)
    
    for pos in range(1, 7):
        p_can = pri_cans[pos - 1]
        p_chi = pri_chis[pos - 1]
        p_elem = BRANCH_ELEMENTS[p_chi]
        p_relation = ELEMENT_RELATIONS[palace_elem][p_elem]
        p_beast = beasts[pos - 1]
        p_is_dong = pos in moving_lines
        p_vuong = get_vuong_suy(p_elem, month_elem)
        p_stars = get_line_than_sat_list(day_can, day_chi, p_chi, month_chi)
        is_quai_than = (p_chi == quai_than_chi)
        
        # Phục Thần
        b_can = base_cans[pos - 1]
        b_chi = base_chis[pos - 1]
        b_elem = BRANCH_ELEMENTS[b_chi]
        b_rel = ELEMENT_RELATIONS[palace_elem][b_elem]
        if b_rel in missing_relatives:
            phuc_than_str = f"{b_rel} {b_can} {b_chi} ({b_elem})"
        else:
            phuc_than_str = "—"
            
        # Transformed Line Calculations
        t_can = trans_cans[pos - 1]
        t_chi = trans_chis[pos - 1]
        t_elem = BRANCH_ELEMENTS[t_chi]
        t_relation = ELEMENT_RELATIONS[palace_elem][t_elem]
        t_vuong = get_vuong_suy(t_elem, month_elem)
        t_stars = get_line_than_sat_list(day_can, day_chi, t_chi, month_chi)
        t_is_kv = t_chi in day_kv_list
        t_is_quai_than = (t_chi == quai_than_chi)
        
        is_kv = p_chi in day_kv_list
        
        lines.append({
            "pos": pos,
            "is_dong": p_is_dong,
            "is_the": (pos == primary_info[3]),
            "is_ung": (pos == primary_info[4]),
            "p_can_chi": f"{p_can} {p_chi} ({p_elem})",
            "p_relation": p_relation,
            "p_vuong": p_vuong,
            "p_beast": p_beast,
            "p_stars": p_stars,
            "is_kv": is_kv,
            "is_quai_than": is_quai_than,
            "phuc_than": phuc_than_str,
            "t_can_chi": f"{t_can} {t_chi} ({t_elem})",
            "t_relation": t_relation,
            "t_vuong": t_vuong,
            "t_stars": t_stars,
            "t_is_kv": t_is_kv,
            "t_is_quai_than": t_is_quai_than
        })
        
    report = format_coin_report(
        time_coords, primary_info, trans_info, lines, moving_lines,
        question, time_meta, pri_upper, pri_lower, trans_upper, trans_lower,
        day_kv_list, hour_kv_list, daily_than_sat, quai_than_chi
    )
    
    return {
        "report": report,
        "time_coords": time_coords,
        "daily_than_sat": daily_than_sat,
        "day_kv": day_kv_list,
        "hour_kv": hour_kv_list,
        "quai_than": quai_than_chi,
        "primary_info": primary_info,
        "trans_info": trans_info,
        "moving_lines": moving_lines,
        "lines": lines
    }

def format_coin_report(
    time_coords, primary_info, trans_info, lines, moving_lines,
    question, time_meta, pri_upper=1, pri_lower=1, trans_upper=1, trans_lower=1,
    day_kv_list=None, hour_kv_list=None, daily_than_sat=None, quai_than_chi=None
):
    out = []
    if time_meta and time_meta.get("source") == "ATOMIC_QUANTUM_CLOCK":
        out.append(f"[Chuẩn Thời Gian: Đồng Hồ Nguyên Tử/Lượng Tử ({time_meta.get('server')}) | RTT: {time_meta.get('latency_ms')} ms]")
    out.append("==========================================================================================")
    out.append("       BẢNG METADATA KỸ THUẬT LỤC HÀO TOÀN DIỆN 100% (DÃ HẠC & BỐC PHỆ CHÍNH TÔNG)")
    out.append("==========================================================================================")
    if question:
        out.append(f"• Việc cần xem  : {question}")
    out.append(f"• Dương Lịch    : {time_coords['solar']}")
    out.append(f"• Âm Lịch       : Ngày {time_coords['lunar_day']:02d} Tháng {time_coords['lunar_month']:02d} Năm {time_coords['can_chi_year']} ({time_coords['nap_am_year']})")
    out.append(f"• Tứ Trụ Can Chi: Năm {time_coords['can_chi_year']} | Tháng {time_coords['can_chi_month']} | Ngày {time_coords['can_chi_day']} | Giờ {time_coords['can_chi_hour']}")
    out.append(f"• Tiết Khí      : {time_coords['tiet_khi']} (Nguyệt Kiến: {time_coords['month_chi']} | Nhật Kiến: {time_coords['day_chi']})")
    
    day_kv_str = " - ".join(day_kv_list) if day_kv_list else "Không"
    hour_kv_str = " - ".join(hour_kv_list) if hour_kv_list else "Không"
    out.append(f"• Tuần Không    : Tuần Không Ngày: 【{day_kv_str}】 | Tuần Không Giờ: 【{hour_kv_str}】")
    
    if daily_than_sat:
        qn_str = ", ".join(daily_than_sat.get("quy_nhan", []))
        out.append(f"• Bảng Thần Sát : Quý Nhân: {qn_str} | Lộc Thần: {daily_than_sat.get('loc_than')} | Dịch Mã: {daily_than_sat.get('dich_ma')} | Đào Hoa: {daily_than_sat.get('dao_hoa')}")
        out.append(f"                 Hoa Cái: {daily_than_sat.get('hoa_cai')} | Tướng Tinh: {daily_than_sat.get('tuong_tinh')} | Văn Xương: {daily_than_sat.get('van_xuong')} | Thiên Y: {daily_than_sat.get('thien_y')}")
        out.append(f"                 Kiếp Sát: {daily_than_sat.get('kiep_sat')} | Tai Sát: {daily_than_sat.get('tai_sat')} | Quải Thần: {quai_than_chi or '—'}")
    
    out.append("------------------------------------------------------------------------------------------")
    
    palace_name = PALACE_INFO[primary_info[2]]["name"]
    pri_tags = " - ".join(get_hex_classifications(pri_upper, pri_lower, primary_info[5]))
    out.append(f"=== QUẺ CHÍNH: {primary_info[1].upper()} (Cung {palace_name}) [{pri_tags}] ===")
    out.append("| Hào | Thế/Ứng | Lục Thân | Can Chi (Hành) | Phục Thần | Vượng/Suy | Không Vong | Thần Sát Lâm Hào | Lục Thú | Trạng Thái |")
    out.append("|:---:|:-------:|:--------:|:--------------:|:---------:|:---------:|:----------:|:-----------------|:-------:|:----------:|")
    
    for l in reversed(lines):
        pos_label = f"Hào {l['pos']}"
        the_ung = "Thế" if l['is_the'] else ("Ứng" if l['is_ung'] else "—")
        kv_str = "Tuần Không" if l['is_kv'] else "—"
        star_str = ", ".join(l['p_stars']) if l['p_stars'] else "—"
        dong_str = "ĐỘNG [O]" if l['is_dong'] else "Tĩnh"
        out.append(f"| {pos_label} | {the_ung} | {l['p_relation']} | {l['p_can_chi']} | {l['phuc_than']} | {l['p_vuong']} | {kv_str} | {star_str} | {l['p_beast']} | {dong_str} |")
        
    out.append("------------------------------------------------------------------------------------------")
    
    if moving_lines:
        trans_palace_name = PALACE_INFO[trans_info[2]]["name"]
        trans_tags = " - ".join(get_hex_classifications(trans_upper, trans_lower, trans_info[5]))
        out.append(f"=== QUẺ BIẾN: {trans_info[1].upper()} (Cung {trans_palace_name}) [{trans_tags}] ===")
        out.append("| Hào | Lục Thân Biến | Can Chi Biến | Vượng/Suy | Không Vong | Thần Sát Lâm Hào | Lục Thú | Hào Động Sang |")
        out.append("|:---:|:-------------:|:------------:|:---------:|:----------:|:-----------------|:-------:|:-------------:|")
        for l in reversed(lines):
            pos_label = f"Hào {l['pos']}"
            t_kv_str = "Tuần Không" if l['t_is_kv'] else "—"
            t_star_str = ", ".join(l['t_stars']) if l['t_stars'] else "—"
            dong_label = "Biến từ Hào Động" if l['is_dong'] else "Tĩnh Đồng Hào"
            out.append(f"| {pos_label} | {l['t_relation']} | {l['t_can_chi']} | {l['t_vuong']} | {t_kv_str} | {t_star_str} | {l['p_beast']} | {dong_label} |")
        out.append("------------------------------------------------------------------------------------------")
        out.append(f"• Các Hào Động  : {', '.join(f'Hào {m}' for m in moving_lines)}")
    else:
        out.append("=== QUẺ BIẾN: (Quẻ Tĩnh — Không có hào động) ===")
        
    out.append("==========================================================================================")
    return "\n".join(out)
