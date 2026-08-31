"""
CanonicalAstrolabe Ground-Truth Parser Module
Parses the complete 3-table "Dùng cho AI - Nhấn sao chép" export from Canonical-Astrolabe-Engine
into a standardized structured Python dictionary / JSON representation.

Covers 100% of fields:
1. Profile & Spatio-Temporal Metadata (Name, Gender, Civil & Solar Times, Coordinates, Lunar/Solar Can Chi)
2. Khối I: Bát Tự Tứ Trụ (Solar term, Direction, 4 Pillars Detail Table, 10 Bazi Da Yun steps)
3. Khối II: Tử Vi Chi Tiết 12 Cung Vị & Phi Hóa (Cục số, Mệnh/Thân, Niên Hóa A-B-C-D, 12 Cung Matrix,
   14 Main Stars with Dac/Ham/VCD xung, 110+ Minor Stars, 4 Flying destinations, Tu Hoa / Huong Tam,
   Kham Thien Routes, Phuong Vien Loc Ky Toan Do).
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple


PALACE_CODE_MAP = {
    "MỆNH": "MỆNH",
    "MỆNH CUNG": "MỆNH",
    "MỆNH BÀN": "MỆNH",
    "PHỤ": "PHỤ",
    "PHỤ MẪU": "PHỤ",
    "PHÚC": "PHÚC",
    "PHÚC ĐỨC": "PHÚC",
    "ĐIỀN": "ĐIỀN",
    "ĐIỀN TRẠCH": "ĐIỀN",
    "QUAN": "QUAN",
    "QUAN LỘC": "QUAN",
    "NÔ": "NÔ",
    "NÔ BỘC": "NÔ",
    "DI": "DI",
    "THIÊN DI": "DI",
    "TẬT": "TẬT",
    "TẬT ÁCH": "TẬT",
    "TÀI": "TÀI",
    "TÀI BẠCH": "TÀI",
    "TỬ": "TỬ",
    "TỬ TỨC": "TỬ",
    "PHỐI": "PHỐI",
    "PHU THÊ": "PHỐI",
    "PHU": "PHỐI",
    "THÊ": "PHỐI",
    "BÀO": "BÀO",
    "HUYNH ĐỆ": "BÀO",
    "HUYNH": "BÀO"
}

BRANCH_NORMALIZATION = {
    "Tị": "Tỵ",
    "tị": "tỵ",
    "TỊ": "TỴ"
}


def normalize_branch(text: str) -> str:
    """Normalize branch spelling (e.g. Tị -> Tỵ)."""
    if not text:
        return ""
    res = text
    for k, v in BRANCH_NORMALIZATION.items():
        res = res.replace(k, v)
    return res


def normalize_palace_code(text: str) -> str:
    """Normalize any palace name variation to standardized uppercase short code."""
    if not text:
        return ""
    cleaned = text.replace("**", "").replace("*", "").replace("Thân cư", "").replace("Cung", "").strip().upper()
    return PALACE_CODE_MAP.get(cleaned, cleaned)


def clean_markdown_text(text: str) -> str:
    """Strip markdown formatting characters."""
    if not text:
        return ""
    return text.replace("**", "").replace("*", "").replace("_", "").strip()


def parse_tang_can(raw_str: str) -> List[Dict[str, str]]:
    """
    Parse hidden stems string like 'Giáp (Quan), Bính (Ấn), Mậu (Kiếp)'
    into [{'can': 'Giáp', 'thap_than': 'Quan'}, ...].
    """
    items = []
    if not raw_str:
        return items
    parts = [p.strip() for p in raw_str.split(",") if p.strip()]
    for p in parts:
        m = re.match(r"([^\(]+)\s*\(([^\)]+)\)", p)
        if m:
            can_name = m.group(1).strip()
            thap_than = m.group(2).strip()
            items.append({"can": can_name, "thap_than": thap_than})
        else:
            items.append({"can": p.strip(), "thap_than": ""})
    return items


def split_markdown_tables(text: str) -> Dict[str, List[List[str]]]:
    """
    Split markdown text into structured table rows based on table signature headers:
    - bazi_pillars: contains 'Thành phần' and 'Trụ Năm'
    - bazi_dayun: contains 'Vận' and 'DV-TT' or '1 ('
    - ziwei_palaces: contains 'Tên Cung' and 'Phi Lộc' or 'Đại Vận Tử Vi'
    """
    lines = [l.strip() for l in text.splitlines()]
    raw_tables: List[List[str]] = []
    curr: List[str] = []
    
    for l in lines:
        if l.startswith("|"):
            curr.append(l)
        elif curr:
            raw_tables.append(curr)
            curr = []
    if curr:
        raw_tables.append(curr)

    parsed_tables: Dict[str, List[List[str]]] = {}
    for table_lines in raw_tables:
        if not table_lines:
            continue
        # Filter out separator row (| --- | --- |)
        clean_rows = []
        for r in table_lines:
            if re.match(r"^\|\s*[-:\s|]+\s*\|?$", r):
                continue
            cells = [c.strip() for c in r.split("|")[1:-1]]
            if cells:
                clean_rows.append(cells)

        if not clean_rows:
            continue

        header_str = " ".join(clean_rows[0])
        # Priority check: Tên Cung first for ziwei_palaces to avoid collision with 'Vận' in 'Đại Vận'
        if "Tên Cung" in header_str:
            parsed_tables["ziwei_palaces"] = clean_rows
        elif "Thành phần" in header_str and "Trụ Năm" in header_str:
            parsed_tables["bazi_pillars"] = clean_rows
        elif "Vận" in header_str:
            parsed_tables["bazi_dayun"] = clean_rows

    return parsed_tables


def parse_canonical_astrolabe_ai_copy(text: str) -> Dict[str, Any]:
    """
    Comprehensive parser for Canonical-Astrolabe-Engine 'Dùng cho AI - Nhấn sao chép' format.
    Extracts 100% of fields into a clean, typed hierarchical structure.
    """
    data: Dict[str, Any] = {
        "profile": {
            "name": None,
            "gender": "Nam",
            "birth_date_raw": "",
            "birth_date_str": "",
            "civil_time": "",
            "solar_time": "",
            "birth_datetime_raw": "",
            "lunar_date_raw": "",
            "lunar_date_str": "",
            "lunar_year_can_chi": "",
            "lunar_day": 0,
            "lunar_month": 0,
            "lunar_hour_branch": "",
            "birth_place": "",
            "coordinates": {"latitude": 0.0, "longitude": 0.0},
            "basic_four_pillars_raw": "",
            "basic_tu_vi_raw": ""
        },
        "bazi": {
            "solar_term": "",
            "direction": "Thuận",
            "pillars": {},
            "da_yun_steps": []
        },
        "four_pillars": {},
        "da_yun_bazi": [],
        "tu_vi_meta": {
            "cuc": "",
            "cuc_name": "",
            "cuc_start_age": 0,
            "cuc_num": 0,
            "menh_nayin": "",
            "than_palace": "",
            "yin_yang_gender": "",
            "parity": "",
            "birth_season": "",
            "season_status": "",
            "cuc_menh_relation": ""
        },
        "nien_hoa": {
            "year_can": "",
            "A": {},
            "B": {},
            "C": {},
            "D": {}
        },
        "si_hua_routes": {
            "ky_chuyen_loc": [],
            "chuyen_ky": []
        },
        "palaces": []
    }

    lines = [l.strip() for l in text.splitlines()]

    # --------------------------------------------------------------------------
    # 1. Parse Profile & Metadata Lines
    # --------------------------------------------------------------------------
    for line in lines:
        raw_line = line.strip()
        if not raw_line:
            continue
        cl = clean_markdown_text(raw_line)

        # Name: * **Tên:** ...
        if "Tên:" in cl:
            val = cl.split("Tên:")[-1].strip()
            if val:
                data["profile"]["name"] = val

        # Gender: * **Giới tính:** Nam / Nữ
        if "Giới tính:" in cl:
            val = cl.split("Giới tính:")[-1].strip()
            data["profile"]["gender"] = val

        # Birth date & times: * **Ngày sinh:** 26/3/2005 4h30 (Hành chính), 4h29 (Giờ Mặt Trời)
        if "Ngày sinh:" in cl:
            val = cl.split("Ngày sinh:")[-1].strip()
            data["profile"]["birth_datetime_raw"] = val
            data["profile"]["birth_date_raw"] = val
            # Extract date
            m_date = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", val)
            if m_date:
                data["profile"]["birth_date_str"] = m_date.group(1)
            # Extract civil time (allow whitespace/tabs in format like 17h\t00 or 17h00)
            m_civil = re.search(r"(\d{1,2}h[\s\t]*\d{1,2})\s*\(Hành chính\)", val)
            if m_civil:
                data["profile"]["civil_time"] = re.sub(r"\s+", "", m_civil.group(1))
            # Extract solar time
            m_solar = re.search(r"(\d{1,2}h[\s\t]*\d{1,2})\s*\(Giờ Mặt Trời\)", val)
            if m_solar:
                data["profile"]["solar_time"] = re.sub(r"\s+", "", m_solar.group(1))

        # Lunar datetime: * **Âm lịch:** Năm Ất Dậu, ngày 17 tháng 02, giờ Dần
        if "Âm lịch:" in cl:
            val = cl.split("Âm lịch:")[-1].strip()
            data["profile"]["lunar_date_str"] = val
            data["profile"]["lunar_date_raw"] = val
            m_lunar = re.search(r"Năm\s*([^,]+),\s*ngày\s*(\d+)\s*tháng\s*(\d+),\s*giờ\s*(\w+)", val)
            if m_lunar:
                data["profile"]["lunar_year_can_chi"] = normalize_branch(m_lunar.group(1).strip())
                data["profile"]["lunar_day"] = int(m_lunar.group(2))
                data["profile"]["lunar_month"] = int(m_lunar.group(3))
                data["profile"]["lunar_hour_branch"] = normalize_branch(m_lunar.group(4).strip())

        # Birth place & coordinates: * **Nơi sinh:** Mỹ Tho, Vietnam (10.353°, 106.375°)
        if "Nơi sinh:" in cl:
            val = cl.split("Nơi sinh:")[-1].strip()
            m_place = re.search(r"([^(]+)\s*\(([\d.]+)[°,\s]+([\d.]+)[°\)]", val)
            if m_place:
                data["profile"]["birth_place"] = m_place.group(1).strip()
                try:
                    data["profile"]["coordinates"]["latitude"] = float(m_place.group(2))
                    data["profile"]["coordinates"]["longitude"] = float(m_place.group(3))
                except ValueError:
                    pass
            else:
                data["profile"]["birth_place"] = val

        # Basic Four Pillars: * **Tứ trụ cơ bản (theo tiết khí):** ...
        if "Tứ trụ cơ bản (theo tiết khí):" in cl:
            data["profile"]["basic_four_pillars_raw"] = cl.split("Tứ trụ cơ bản (theo tiết khí):")[-1].strip()

        # Basic Tu Vi: * **Tử vi cơ bản (theo âm lịch):** ...
        if "Tử vi cơ bản (theo âm lịch):" in cl:
            data["profile"]["basic_tu_vi_raw"] = cl.split("Tử vi cơ bản (theo âm lịch):")[-1].strip()

        # Solar Term & Direction: * **Tiết khí:** Xuân Phân. **Vận:** Nghịch.
        if "Tiết khí:" in cl and "Vận:" in cl:
            m_term = re.search(r"Tiết khí:\s*([^.]+)\.\s*Vận:\s*([^.]+)", cl)
            if m_term:
                data["bazi"]["solar_term"] = m_term.group(1).strip()
                data["bazi"]["direction"] = m_term.group(2).strip()
            else:
                if "Tiết khí:" in cl:
                    data["bazi"]["solar_term"] = cl.split("Tiết khí:")[-1].split(".")[0].strip()
                if "Vận:" in cl:
                    data["bazi"]["direction"] = cl.split("Vận:")[-1].split(".")[0].strip()

        # Tu Vi Basic & Nayin: * **Cơ bản:** Âm Nam, Âm dương thuận lý. **Mệnh:** Tuyền Trung Thủy.
        if "Cơ bản:" in cl and "Mệnh:" in cl:
            m_cb = re.search(r"Cơ bản:\s*([^,]+),\s*([^.]+)\.\s*Mệnh:\s*([^.]+)", cl)
            if m_cb:
                data["tu_vi_meta"]["yin_yang_gender"] = m_cb.group(1).strip()
                data["tu_vi_meta"]["parity"] = m_cb.group(2).strip()
                data["tu_vi_meta"]["menh_nayin"] = m_cb.group(3).strip()

        # Cuc & Than: * **Cục:** Hỏa Lục Cục (Khởi vận 6 tuổi). **Thân:** Thân cư QUAN.
        if "Cục:" in cl and "Thân:" in cl:
            m_cuc = re.search(r"Cục:\s*([^(]+)\s*\(Khởi vận\s*(\d+)\s*tuổi\)\.?\s*Thân:\s*(?:Thân cư\s*)?([^.]+)", cl)
            if m_cuc:
                cuc_name = m_cuc.group(1).strip()
                cuc_age = int(m_cuc.group(2))
                than_p = m_cuc.group(3).strip()
                data["tu_vi_meta"]["cuc"] = cuc_name
                data["tu_vi_meta"]["cuc_name"] = cuc_name
                data["tu_vi_meta"]["cuc_start_age"] = cuc_age
                data["tu_vi_meta"]["cuc_num"] = cuc_age
                data["tu_vi_meta"]["than_palace"] = normalize_palace_code(than_p)
            else:
                if "Cục:" in cl:
                    cuc_str = cl.split("Cục:")[-1].split(".")[0].strip()
                    data["tu_vi_meta"]["cuc"] = cuc_str
                    data["tu_vi_meta"]["cuc_name"] = cuc_str
                if "Thân:" in cl:
                    than_str = cl.split("Thân:")[-1].split(".")[0].strip()
                    data["tu_vi_meta"]["than_palace"] = normalize_palace_code(than_str)

        # Season characteristics: * **Đặc điểm:** Sinh mùa Xuân (Không được mùa sinh), Mệnh khắc cục.
        if "Đặc điểm:" in cl:
            m_season = re.search(r"Đặc điểm:\s*Sinh mùa\s*([^(]+)\s*\(([^)]+)\),\s*([^.]+)", cl)
            if m_season:
                data["tu_vi_meta"]["birth_season"] = m_season.group(1).strip()
                data["tu_vi_meta"]["season_status"] = m_season.group(2).strip()
                data["tu_vi_meta"]["cuc_menh_relation"] = m_season.group(3).strip()

        # Niên Hóa: * **Niên Hóa (Can Ất):** Lộc (A) -> Thiên Cơ (PHỤ) | Quyền (B) -> Thiên Lương (NÔ) | Khoa (C) -> Tử Vi (PHÚC) | Kỵ (D) -> Thái Âm (PHỤ).
        if "Niên Hóa" in cl:
            m_nh = re.search(r"Niên Hóa\s*\(Can\s*(\w+)\):\s*(.+)", cl)
            if m_nh:
                year_can = m_nh.group(1).strip()
                data["nien_hoa"]["year_can"] = year_can
                items_str = m_nh.group(2)
                pipe_parts = [p.strip() for p in items_str.split("|")]
                for part in pipe_parts:
                    m_item = re.search(r"(Lộc\s*\(A\)|Quyền\s*\(B\)|Khoa\s*\(C\)|Kỵ\s*\(D\)|Kị\s*\(D\))\s*->\s*([^(]+)\(([^)]+)\)", part)
                    if m_item:
                        hoa_type = m_item.group(1).strip()
                        star = m_item.group(2).strip()
                        p_code = normalize_palace_code(m_item.group(3).strip())
                        key = "A" if "Lộc" in hoa_type else ("B" if "Quyền" in hoa_type else ("C" if "Khoa" in hoa_type else "D"))
                        data["nien_hoa"][key] = {
                            "star": star,
                            "palace_code": p_code,
                            "display": f"{hoa_type} -> {star} ({p_code})"
                        }

        # Kham Thien Routes:
        # * **Đường Kị chuyển Lộc:** PHỐI -> ĐIỀN, TỬ -> DI...
        if "Đường Kị chuyển Lộc:" in cl or "Đường Kỵ chuyển Lộc:" in cl:
            val = cl.split(":")[-1]
            raw_paths = [x.strip() for x in val.split(",") if x.strip()]
            data["si_hua_routes"]["ky_chuyen_loc"] = raw_paths

        # * **Đường chuyển Kị:** NÔ -> PHỐI (Vũ Khúc)...
        if "Đường chuyển Kị:" in cl or "Đường chuyển Kỵ:" in cl:
            val = cl.split(":")[-1]
            raw_paths = [x.strip() for x in val.split(",") if x.strip()]
            data["si_hua_routes"]["chuyen_ky"] = raw_paths

    # --------------------------------------------------------------------------
    # 2. Parse Markdown Tables
    # --------------------------------------------------------------------------
    tables = split_markdown_tables(text)

    # Table 1: Bazi Four Pillars Detail
    if "bazi_pillars" in tables:
        rows = tables["bazi_pillars"]
        pillars_dict = {"year": {}, "month": {}, "day": {}, "hour": {}}
        keys = ["year", "month", "day", "hour"]
        row_map = {}
        for r in rows[1:]:
            if not r:
                continue
            label = clean_markdown_text(r[0])
            row_map[label] = [clean_markdown_text(c) for c in r[1:]]

        for i, k in enumerate(keys):
            tt = row_map.get("Thập Thần", ["", "", "", ""])[i] if i < len(row_map.get("Thập Thần", [])) else ""
            can = row_map.get("Thiên Can", ["", "", "", ""])[i] if i < len(row_map.get("Thiên Can", [])) else ""
            chi = normalize_branch(row_map.get("Địa Chi", ["", "", "", ""])[i] if i < len(row_map.get("Địa Chi", [])) else "")
            tc_raw = row_map.get("Tàng Can", ["", "", "", ""])[i] if i < len(row_map.get("Tàng Can", [])) else ""
            ts = row_map.get("Trường Sinh", ["", "", "", ""])[i] if i < len(row_map.get("Trường Sinh", [])) else ""
            na = row_map.get("Nạp Âm", ["", "", "", ""])[i] if i < len(row_map.get("Nạp Âm", [])) else ""
            
            can_chi_str = f"{can.title()} {chi.title()}".strip()

            pillars_dict[k] = {
                "thap_than": tt,
                "can": can,
                "chi": chi,
                "can_chi": can_chi_str,
                "tang_can_raw": tc_raw,
                "tang_can": parse_tang_can(tc_raw),
                "truong_sinh": ts,
                "nayin": na
            }

        data["bazi"]["pillars"] = pillars_dict
        data["four_pillars"] = pillars_dict

    # Table 2: Bazi Da Yun Steps
    if "bazi_dayun" in tables:
        rows = tables["bazi_dayun"]
        if len(rows) >= 4:
            headers = rows[0][1:]
            years_row = rows[1][1:]
            can_chi_row = rows[2][1:]
            than_row = rows[3][1:]
            
            da_yun_steps = []
            for idx, h in enumerate(headers):
                h_clean = clean_markdown_text(h)
                m_step = re.match(r"(\d+)\s*\(([^-]+)-([^t\)]+)t?\)", h_clean)
                step_idx = idx + 1
                age_range = h_clean
                age_start = 0
                age_end = 0
                if m_step:
                    step_idx = int(m_step.group(1))
                    age_start = int(m_step.group(2).strip())
                    age_end = int(m_step.group(3).strip())
                    age_range = f"{age_start}-{age_end}t"

                start_yr = int(clean_markdown_text(years_row[idx])) if idx < len(years_row) and clean_markdown_text(years_row[idx]).isdigit() else 0
                cc_val = normalize_branch(clean_markdown_text(can_chi_row[idx])) if idx < len(can_chi_row) else ""
                cc_parts = cc_val.split()
                c_val = cc_parts[0] if cc_parts else ""
                ch_val = cc_parts[1] if len(cc_parts) > 1 else ""
                th_val = clean_markdown_text(than_row[idx]) if idx < len(than_row) else ""

                da_yun_steps.append({
                    "step_index": step_idx,
                    "age_range": age_range,
                    "age_start": age_start,
                    "age_end": age_end,
                    "start_year": start_yr,
                    "can_chi": cc_val,
                    "can": c_val,
                    "chi": ch_val,
                    "thap_than": th_val
                })

            data["bazi"]["da_yun_steps"] = da_yun_steps
            data["da_yun_bazi"] = da_yun_steps

    # Table 3: Ziwei 12 Palaces Matrix
    if "ziwei_palaces" in tables:
        rows = tables["ziwei_palaces"]
        palaces_list = []
        for r in rows[1:]:
            if len(r) < 10:
                continue
            raw_p_name = clean_markdown_text(r[0])
            p_code = normalize_palace_code(raw_p_name)
            branch = normalize_branch(clean_markdown_text(r[1]))
            can_chi = normalize_branch(clean_markdown_text(r[2]))
            can_parts = can_chi.split()
            can_name = can_parts[0] if can_parts else ""
            
            da_yun_raw = clean_markdown_text(r[3])
            dy_start, dy_end = 0, 0
            m_dy = re.search(r"(\d+)\s*-\s*(\d+)", da_yun_raw)
            if m_dy:
                dy_start = int(m_dy.group(1))
                dy_end = int(m_dy.group(2))

            # Main Stars & VCD
            main_stars_raw = clean_markdown_text(r[4])
            is_vcd = False
            vcd_xung = ""
            main_stars = []
            
            if "VCD" in main_stars_raw:
                is_vcd = True
                m_vcd = re.search(r"VCD\s*xung\s*\(([^)]+)\)", main_stars_raw)
                if m_vcd:
                    vcd_xung = m_vcd.group(1).strip()
            else:
                main_stars = [s.strip() for s in main_stars_raw.split(",") if s.strip()]

            # Minor Stars
            minor_stars_raw = clean_markdown_text(r[5])
            minor_stars = [s.strip() for s in minor_stars_raw.split(",") if s.strip()]

            # Flying Stars Destinations
            phi_loc = normalize_palace_code(clean_markdown_text(r[6]).replace("->", ""))
            phi_quyen = normalize_palace_code(clean_markdown_text(r[7]).replace("->", ""))
            phi_khoa = normalize_palace_code(clean_markdown_text(r[8]).replace("->", ""))
            phi_ky = normalize_palace_code(clean_markdown_text(r[9]).replace("->", ""))

            # Tu Hoa / Huong Tam
            tu_hoa_huong_tam_raw = r[10].strip() if len(r) > 10 else ""
            tu_hoa_clean = clean_markdown_text(tu_hoa_huong_tam_raw)
            self_trans = []
            inward_trans = []
            if tu_hoa_clean:
                items = [clean_markdown_text(it) for it in tu_hoa_clean.split(",") if it.strip()]
                for it in items:
                    if "Tự hóa" in it or "Tự hoá" in it:
                        self_trans.append(it)
                    elif "Hướng tâm" in it:
                        inward_trans.append(it)

            # Phuong Vien Loc Ky Toan Do
            phuong_vien_raw = clean_markdown_text(r[11]) if len(r) > 11 else ""
            loc_cnt, quyen_cnt, khoa_cnt, ky_cnt = 0, 0, 0, 0
            if phuong_vien_raw:
                m_l = re.search(r"(\d+)\s*L[^\s,]*", phuong_vien_raw)
                if m_l:
                    loc_cnt = int(m_l.group(1))
                m_q = re.search(r"(\d+)\s*Q[^\s,]*", phuong_vien_raw)
                if m_q:
                    quyen_cnt = int(m_q.group(1))
                m_k = re.search(r"(\d+)\s*Khoa", phuong_vien_raw)
                if m_k:
                    khoa_cnt = int(m_k.group(1))
                m_ky = re.search(r"(\d+)\s*K[ịỵyIíìYýỵ]|\b(\d+)\s*K[^\s,]*\(D\)", phuong_vien_raw)
                if m_ky:
                    ky_cnt = int(m_ky.group(1) or m_ky.group(2))

            palaces_list.append({
                "name": raw_p_name,
                "palace_code": p_code,
                "branch": branch,
                "can_chi": can_chi,
                "can": can_name,
                "da_yun": da_yun_raw,
                "da_yun_range": da_yun_raw,
                "da_yun_start": dy_start,
                "da_yun_end": dy_end,
                "is_vcd": is_vcd,
                "vcd_xung": vcd_xung,
                "main_stars": main_stars,
                "main_stars_with_brightness": main_stars,
                "minor_stars": minor_stars,
                "phi_loc": phi_loc,
                "phi_quyen": phi_quyen,
                "phi_khoa": phi_khoa,
                "phi_ky": phi_ky,
                "self_transformations": self_trans,
                "inward_transformations": inward_trans,
                "tu_hoa_huong_tam": tu_hoa_clean,
                "tu_hoa_huong_tam_raw": tu_hoa_clean,
                "phuong_vien": phuong_vien_raw,
                "phuong_vien_loc_ky": phuong_vien_raw,
                "phuong_vien_loc_count": loc_cnt,
                "phuong_vien_quyen_count": quyen_cnt,
                "phuong_vien_khoa_count": khoa_cnt,
                "phuong_vien_ky_count": ky_cnt
            })

        data["palaces"] = palaces_list

    return data


def parse_canonical_astrolabe_file(file_path: str) -> Dict[str, Any]:
    """Parse a CanonicalAstrolabe markdown file directly from its filesystem path."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return parse_canonical_astrolabe_ai_copy(content)
