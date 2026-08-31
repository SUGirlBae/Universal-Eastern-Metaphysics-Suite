"""
Cross-Discipline Memory Module (Dao Root & Yi-Yi Tong-Yuan Resonance)
Bridges I Ching, Bazi, Ziwei, Feng Shui, Internal Alchemy (Dan Dao), and TCM (Dong Y).
"""

import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .distilled_rules import add_or_update_pattern
except (ImportError, ValueError):
    from distilled_rules import add_or_update_pattern

WU_XING_ORGAN_MAP = {
    "Kim": {
        "organ_zang": "Phế (Phổi)",
        "organ_fu": "Đại Trường (Ruột già)",
        "sense_organ": "Mũi / Da lông / Khí quản",
        "emotion": "Bi (Ưu sầu, nén cảm xúc)",
        "nourishment": "Thực phẩm màu trắng, vị cay nhẹ, luyện thở quy tức"
    },
    "Mộc": {
        "organ_zang": "Can (Gan)",
        "organ_fu": "Đởm (Túi mật)",
        "sense_organ": "Mắt / Gân cốt",
        "emotion": "Nộ (Nóng giận, uất ức)",
        "nourishment": "Thực phẩm màu xanh, vị chua thanh, thư giãn điều tức"
    },
    "Thủy": {
        "organ_zang": "Thận",
        "organ_fu": "Bàng Quang",
        "sense_organ": "Tai / Xương tủy / Răng",
        "emotion": "Khủng (Kinh sợ, bất an)",
        "nourishment": "Thực phẩm màu đen/sẫm, vị mặn nhẹ, ôn bổ chân hỏa"
    },
    "Hỏa": {
        "organ_zang": "Tâm (Tim)",
        "organ_fu": "Tiểu Trường (Ruột non)",
        "sense_organ": "Lưỡi / Mạch máu / Thần trí",
        "emotion": "Hỷ (Kích động, quá vui hóa loạn)",
        "nourishment": "Thực phẩm màu đỏ, vị đắng dịu, tĩnh tâm an thần"
    },
    "Thổ": {
        "organ_zang": "Tỳ (Lách)",
        "organ_fu": "Vị (Dạ dày)",
        "sense_organ": "Miệng / Môi / Cơ bắp",
        "emotion": "Tư (Lo nghĩ quá độ, suy tư)",
        "nourishment": "Thực phẩm màu vàng, vị ngọt tự nhiên, kiện tỳ hóa thấp"
    }
}

def get_yi_yi_tong_yuan_mapping(element: str) -> Dict[str, Any]:
    """Retrieve TCM/Daoist resonance mapping for a given Wu Xing element."""
    elem_norm = element.strip().capitalize()
    return WU_XING_ORGAN_MAP.get(elem_norm, {
        "organ_zang": "Chưa rõ",
        "organ_fu": "Chưa rõ",
        "sense_organ": "Chưa rõ",
        "emotion": "Chưa rõ",
        "nourishment": "Cân bằng ngũ vị"
    })

def detect_cross_discipline_links(results_by_discipline: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Synthesize cross-discipline diagnostic links from multiple reading payloads."""
    insights = []
    
    # 1. Check Water dominance (Bazi + I Ching + Ziwei)
    has_water_bazi = False
    if "bazi" in results_by_discipline:
        b_res = results_by_discipline["bazi"]
        day_m = b_res.get("day_master", {}).get("element", "")
        if "Thủy" in day_m:
            has_water_bazi = True
            
    has_water_iching = False
    if "kinh_dich" in results_by_discipline:
        i_res = results_by_discipline["kinh_dich"]
        m_hex = i_res.get("main_hexagram", {}).get("name", "")
        if any(w in m_hex for w in ["Thủy", "Khảm", "Nhu", "Kiển", "Tiết", "Tỉnh"]):
            has_water_iching = True
            
    if has_water_bazi and has_water_iching:
        tcm_thuy = get_yi_yi_tong_yuan_mapping("Thủy")
        tcm_hoa = get_yi_yi_tong_yuan_mapping("Hỏa")
        insights.append({
            "signature": "Cross_Thuy_Vuong_Han_Thuy_Khuyet_Hoa",
            "disciplines": ["bat_tu", "kinh_dich", "dan_dao", "dong_y"],
            "description": "Bát Tự Thủy hàn ngộ Quẻ Dịch Khảm/Thủy vượng -> Khí cơ thiên về Âm Hàn, cần bổ Tâm Hỏa để Thủy Hỏa Ký Tế.",
            "dao_root": "Y Dịch Đồng Nguyên: Thủy Hỏa Ký Tế",
            "health_advice": f"Chú trọng dưỡng {tcm_thuy['organ_zang']} ({tcm_thuy['sense_organ']}), đồng thời kích hoạt {tcm_hoa['organ_zang']}."
        })
        
    return insights

def store_cross_pattern(pattern_data: Dict[str, Any], case_id: int, db_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Store a verified cross-discipline pattern into L4 memory."""
    sig = pattern_data.get("signature", "Cross_Generic_Pattern")
    return add_or_update_pattern(
        pattern_signature=sig,
        case_id=case_id,
        is_supporting=True,
        reason=pattern_data.get("description"),
        discipline_scope=pattern_data.get("disciplines", ["cross_discipline"]),
        description=pattern_data.get("description"),
        dao_root=pattern_data.get("dao_root"),
        db_path=db_path
    )
