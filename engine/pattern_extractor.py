"""
Pattern Extractor Module (L4 Structural Fingerprinting)
Extracts abstract mathematical and metaphysical patterns from readings,
decoupling universal formulas from individual narrative outcomes.
"""

import re
import unicodedata
from typing import Dict, Any, List, Optional

def remove_accents(input_str: str) -> str:
    """Remove Vietnamese accents for robust ASCII pattern signatures."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D')

def normalize_pattern_signature(raw_pattern: str) -> str:
    """Convert raw descriptive string into standardized canonical signature."""
    clean = remove_accents(raw_pattern.strip())
    clean = re.sub(r'[^a-zA-Z0-9_]+', '_', clean)
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean

def extract_iching_patterns(luc_hao_result: dict) -> List[Dict[str, Any]]:
    """Extract structural patterns from I Ching / Luc Hao reading."""
    patterns = []
    
    main_hex = luc_hao_result.get("main_hexagram", {})
    changed_hex = luc_hao_result.get("changed_hexagram", {})
    moving_lines = luc_hao_result.get("moving_lines", [])
    
    # 1. Base hexagram pattern
    m_name = main_hex.get("name", "")
    if m_name:
        sig = normalize_pattern_signature(f"IChing_Que_{m_name}")
        patterns.append({
            "signature": sig,
            "discipline": "kinh_dich",
            "description": f"Quẻ chủ: {m_name}",
            "dao_root": "64 Quẻ Dịch Chu Dịch Khái Luận"
        })
        
    # 2. Moving lines patterns
    m_lines_detail = main_hex.get("lines", [])
    c_lines_detail = changed_hex.get("lines", []) if changed_hex else []
    
    for idx in moving_lines:
        if 1 <= idx <= len(m_lines_detail):
            m_line = m_lines_detail[idx - 1]
            m_than = m_line.get("luc_than", "")
            m_vuong = m_line.get("vuong_suy", "")
            m_khong = m_line.get("khong_vong", "")
            
            c_than = ""
            if c_lines_detail and idx <= len(c_lines_detail):
                c_than = c_lines_detail[idx - 1].get("luc_than", "")
                
            if m_than and c_than:
                sig = normalize_pattern_signature(f"IChing_Hao_{idx}_{m_than}_dong_hoa_{c_than}")
                patterns.append({
                    "signature": sig,
                    "discipline": "kinh_dich",
                    "description": f"Hào {idx} {m_than} động hóa {c_than} ({m_vuong})",
                    "dao_root": "Lục Hào Dã Hạc Bốc Phệ Biến Hóa"
                })
            elif m_than:
                sig = normalize_pattern_signature(f"IChing_Hao_{idx}_{m_than}_dong")
                patterns.append({
                    "signature": sig,
                    "discipline": "kinh_dich",
                    "description": f"Hào {idx} {m_than} phát động",
                    "dao_root": "Lục Hào Khẩu Quyết"
                })
                
    return patterns

def extract_bazi_patterns(bazi_result: dict) -> List[Dict[str, Any]]:
    """Extract structural patterns from Bazi reading."""
    patterns = []
    pillars = bazi_result.get("pillars", {})
    day_master = bazi_result.get("day_master", {})
    
    # 1. Day Master + Month Branch climate
    day_can = pillars.get("day", {}).get("can_chi", "").split()[0] if pillars.get("day", {}).get("can_chi") else ""
    month_chi = pillars.get("month", {}).get("can_chi", "").split()[1] if len(pillars.get("month", {}).get("can_chi", "").split()) > 1 else ""
    
    if day_can and month_chi:
        sig = normalize_pattern_signature(f"Bazi_Nhat_Chu_{day_can}_sinh_thang_{month_chi}")
        patterns.append({
            "signature": sig,
            "discipline": "bat_tu",
            "description": f"Nhật chủ {day_can} sinh tháng {month_chi}",
            "dao_root": "Cùng Thông Bảo Giám Điều Hầu Luận"
        })
        
    # 2. Branch interactions (Thìn-Sửu, Hợi-Mão, etc.)
    all_branches = []
    for p in ["year", "month", "day", "time"]:
        parts = pillars.get(p, {}).get("can_chi", "").split()
        if len(parts) > 1:
            all_branches.append(parts[1])
            
    b_set = set(all_branches)
    if "Thìn" in b_set and "Sửu" in b_set:
        patterns.append({
            "signature": "Bazi_Thin_Suu_tuong_pha",
            "discipline": "bat_tu",
            "description": "Địa chi có Thìn - Sửu tương phá",
            "dao_root": "Bát Tự Manh Phái Phá Luận"
        })
    if "Hợi" in b_set and "Mão" in b_set:
        patterns.append({
            "signature": "Bazi_Hoi_Mao_ban_hop_Moc",
            "discipline": "bat_tu",
            "description": "Địa chi có Hợi - Mão bán hợp Mộc cục",
            "dao_root": "Tam Hợp Cục Mộc Vượng"
        })
        
    return patterns

def extract_tuvi_patterns(tuvi_result: dict) -> List[Dict[str, Any]]:
    """Extract structural patterns from Ziwei reading."""
    patterns = []
    palaces = tuvi_result.get("palaces", [])
    
    for p in palaces:
        p_name = p.get("name", "")
        branch = p.get("branch_name", "")
        main_stars = [s.get("name", "") for s in p.get("main_stars", [])]
        minor_stars = [s.get("name", "") for s in p.get("minor_stars", [])]
        
        # Menh palace patterns
        if p.get("is_menh"):
            stars_str = "_".join(main_stars) if main_stars else "Vo_Chinh_Dieu"
            sig = normalize_pattern_signature(f"TuVi_Menh_{stars_str}_tai_{branch}")
            patterns.append({
                "signature": sig,
                "discipline": "tu_vi",
                "description": f"Mệnh cung {stars_str} tại {branch}",
                "dao_root": "Tử Vi Đẩu Số Toàn Thư Cung Mệnh"
            })
            
            # Sát tinh tại Mệnh
            sat_tinh = [s for s in minor_stars if s in ["Địa Không", "Địa Kiếp", "Hỏa Tinh", "Linh Tinh", "Kình Dương", "Đà La"]]
            if sat_tinh:
                sat_sig = normalize_pattern_signature(f"TuVi_Menh_lam_{'_'.join(sat_tinh)}")
                patterns.append({
                    "signature": sat_sig,
                    "discipline": "tu_vi",
                    "description": f"Mệnh cung hội sát tinh: {', '.join(sat_tinh)}",
                    "dao_root": "Lục Sát Tinh Tọa Mệnh"
                })
                
        # Tat Ach palace patterns
        if "Tật Ách" in p_name:
            sat_tat = [s for s in minor_stars if s in ["Đà La", "Hóa Kỵ", "Văn Khúc"]]
            if sat_tat:
                sig = normalize_pattern_signature(f"TuVi_Tat_Ach_{'_'.join(sat_tat)}")
                patterns.append({
                    "signature": sig,
                    "discipline": "tu_vi",
                    "description": f"Tật Ách cung hội {', '.join(sat_tat)}",
                    "dao_root": "Tật Ách Luận Ách Tắc Thần Kinh"
                })
                
    return patterns

def extract_cross_patterns(patterns_by_discipline: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Detect cross-discipline resonances across multiple readings."""
    cross_patterns = []
    
    # Collect all signatures
    all_sigs = []
    for d, pats in patterns_by_discipline.items():
        for p in pats:
            all_sigs.append(p.get("signature", "").lower())
            
    # Check for Water-Cold synergy (Nhâm Thủy + Thủy Thiên Nhu / Hóa Kỵ)
    has_cold_water_bazi = any("nham" in s and "hoi" in s for s in all_sigs)
    has_water_iching = any("nhu" in s or "kham" in s for s in all_sigs)
    
    if has_cold_water_bazi and has_water_iching:
        cross_patterns.append({
            "signature": "Cross_Thuy_khi_qua_thinh_can_Hoa_Dieu_Hau",
            "discipline": "cross_discipline",
            "description": "Bát Tự Thủy hàn ngộ Kinh Dịch Thủy vượng -> Khí số thuần Thủy, bức thiết cần Hỏa Điều Hầu",
            "dao_root": "Y Dịch Mệnh Quái Đồng Nguyên - Ngũ Hành Điều Hòa"
        })
        
    return cross_patterns
