"""
Output Formatter matching standard Vietnamese divination format with 100% Technical Metadata.
"""
try:
    from .luc_hao import (
        BRANCH_ELEMENTS, get_empty_branches, get_full_daily_than_sat,
        get_line_than_sat_list, PALACE_QUAI_THAN
    )
except (ImportError, ValueError):
    from luc_hao import (
        BRANCH_ELEMENTS, get_empty_branches, get_full_daily_than_sat,
        get_line_than_sat_list, PALACE_QUAI_THAN
    )

def format_divination_report(time_coords, mai_hoa_res, luc_hao_res, question=""):
    out = []
    out.append("==========================================================================================")
    out.append("       BẢNG METADATA KỸ THUẬT DỊCH LÝ TOÀN DIỆN 100% (MAI HOA & LỤC HÀO)")
    out.append("==========================================================================================")
    if question:
        out.append(f"• Việc cần xem  : {question}")
    out.append(f"• Dương Lịch    : {time_coords['solar']}")
    out.append(f"• Âm Lịch       : Ngày {time_coords['lunar_day']:02d} Tháng {time_coords['lunar_month']:02d} Năm {time_coords['can_chi_year']} ({time_coords.get('nap_am_year', '')})")
    out.append(f"• Tứ Trụ Can Chi: Năm {time_coords['can_chi_year']} | Tháng {time_coords['can_chi_month']} | Ngày {time_coords['can_chi_day']} | Giờ {time_coords['can_chi_hour']}")
    out.append(f"• Tiết Khí      : {time_coords['tiet_khi']} (Nguyệt Kiến: {time_coords['month_chi']} | Nhật Kiến: {time_coords['day_chi']})")
    
    day_can = time_coords["day_can"]
    day_chi = time_coords["day_chi"]
    hour_can = time_coords["can_chi_hour"].split()[0]
    hour_chi = time_coords["can_chi_hour"].split()[1] if len(time_coords["can_chi_hour"].split()) > 1 else "Tý"
    month_chi = time_coords["month_chi"]
    
    day_kv = get_empty_branches(day_can, day_chi)
    hour_kv = get_empty_branches(hour_can, hour_chi)
    daily_than_sat = get_full_daily_than_sat(day_can, day_chi, month_chi)
    
    day_kv_str = " - ".join(day_kv)
    hour_kv_str = " - ".join(hour_kv)
    out.append(f"• Tuần Không    : Tuần Không Ngày: 【{day_kv_str}】 | Tuần Không Giờ: 【{hour_kv_str}】")
    
    qn_str = ", ".join(daily_than_sat.get("quy_nhan", []))
    out.append(f"• Bảng Thần Sát : Quý Nhân: {qn_str} | Lộc Thần: {daily_than_sat.get('loc_than')} | Dịch Mã: {daily_than_sat.get('dich_ma')} | Đào Hoa: {daily_than_sat.get('dao_hoa')}")
    out.append(f"                 Hoa Cái: {daily_than_sat.get('hoa_cai')} | Tướng Tinh: {daily_than_sat.get('tuong_tinh')} | Văn Xương: {daily_than_sat.get('van_xuong')} | Thiên Y: {daily_than_sat.get('thien_y')}")
    out.append(f"                 Kiếp Sát: {daily_than_sat.get('kiep_sat')} | Tai Sát: {daily_than_sat.get('tai_sat')}")
    
    out.append("------------------------------------------------------------------------------------------")
    
    # Primary Hexagram (Quẻ Chính)
    main_tags = " - ".join(luc_hao_res.get("hex_tags", []))
    out.append(f"=== QUẺ CHÍNH: {luc_hao_res['hex_symbol'].upper()} (Cung {luc_hao_res['palace_name']}) [{main_tags}] ===")
    out.append("| Hào | Thế/Ứng | Lục Thân | Can Chi (Hành) | Phục Thần | Vượng/Suy | Không Vong | Thần Sát Lâm Hào | Lục Thú | Trạng Thái |")
    out.append("|:---:|:-------:|:--------:|:--------------:|:---------:|:---------:|:----------:|:-----------------|:-------:|:----------:|")
    for line in reversed(luc_hao_res["lines"]):
        the_ung = line.get('pos_str', '') or "—"
        dong_str = "ĐỘNG [O]" if line['is_dong'] else "Tĩnh"
        stars_str = ", ".join(line['stars']) if line['stars'] else "—"
        kv_str = "Tuần Không" if line['is_khong'] else "—"
        out.append(
            f"| Hào {line['line_num']} | {the_ung} | {line['luc_than']} | {line['can_chi']} | "
            f"{line['phuc_than']} | {line['vuong_suy']} | {kv_str} | "
            f"{stars_str} | {line['luc_thu']} | {dong_str} |"
        )
    out.append("------------------------------------------------------------------------------------------")
    
    # Mutual Hexagram (Quẻ Hỗ)
    h_tags = " - ".join(luc_hao_res.get("h_hex_tags", []))
    out.append(f"=== QUẺ HỔ: {luc_hao_res['h_hex_symbol'].upper()} (Cung {luc_hao_res['h_palace_name']}) [{h_tags}] ===")
    out.append("------------------------------------------------------------------------------------------")
    
    # Transformed Hexagram (Quẻ Biến)
    t_tags = " - ".join(luc_hao_res.get("t_hex_tags", []))
    out.append(f"=== QUẺ BIẾN: {luc_hao_res['t_hex_symbol'].upper()} (Cung {luc_hao_res['t_palace_name']}) [{t_tags}] ===")
    out.append("| Hào | Lục Thân Biến | Can Chi Biến | Vượng/Suy | Không Vong | Thần Sát Lâm Hào | Lục Thú | Hào Động Sang |")
    out.append("|:---:|:-------------:|:------------:|:---------:|:----------:|:-----------------|:-------:|:-------------:|")
    for line in reversed(luc_hao_res["lines"]):
        t_stars_str = ", ".join(line['trans_stars']) if line['trans_stars'] else "—"
        t_kv_str = "Tuần Không" if line['trans_is_khong'] else "—"
        dong_label = "Biến từ Hào Động" if line['is_dong'] else "Tĩnh Đồng Hào"
        out.append(
            f"| Hào {line['line_num']} | {line['trans_luc_than']} | {line['trans_can_chi']} | "
            f"{line['trans_vuong_suy']} | {t_kv_str} | "
            f"{t_stars_str} | {line['luc_thu']} | {dong_label} |"
        )
    out.append("------------------------------------------------------------------------------------------")
    out.append(f"• Hào Động: Hào {mai_hoa_res['moving_line']}")
    out.append("==========================================================================================")
    
    return "\n".join(out)
