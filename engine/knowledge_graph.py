"""
Metaphysics Knowledge Graph & Ontology Engine
Models relations between Elements, Stems, Branches, Trigrams, Stars, Gates, and Spirits.
"""
from typing import Dict, Any, List, Set, Tuple

WUXING = ["Kim", "Thủy", "Mộc", "Hỏa", "Thổ"]

# Ngũ Hành Sinh Khắc
WUXING_RELATIONS = {
    "Kim": {"sinh": "Thủy", "sinh_boi": "Thổ", "khac": "Mộc", "bi_khac": "Hỏa", "color": "#E5E7EB"},
    "Thủy": {"sinh": "Mộc", "sinh_boi": "Kim", "khac": "Hỏa", "bi_khac": "Thổ", "color": "#3B82F6"},
    "Mộc": {"sinh": "Hỏa", "sinh_boi": "Thủy", "khac": "Thổ", "bi_khac": "Kim", "color": "#10B981"},
    "Hỏa": {"sinh": "Thổ", "sinh_boi": "Mộc", "khac": "Kim", "bi_khac": "Thủy", "color": "#EF4444"},
    "Thổ": {"sinh": "Kim", "sinh_boi": "Hỏa", "khac": "Thủy", "bi_khac": "Mộc", "color": "#F59E0B"}
}

# Chi Quan Hệ (Branches Interactions)
BRANCH_RELATIONS = {
    "tam_hop": {
        "Thân Tý Thìn": "Thủy", "Hợi Mão Mùi": "Mộc",
        "Dần Ngọ Tuất": "Hỏa", "Tỵ Dậu Sửu": "Kim"
    },
    "luc_hop": {
        "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần",
        "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn",
        "Tỵ": "Thân", "Thân": "Tỵ", "Ngọ": "Mùi", "Mùi": "Ngọ"
    },
    "luc_xung": {
        "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu",
        "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão",
        "Thìn": "Tuất", "Tuất": "Thìn", "Tỵ": "Hợi", "Hợi": "Tỵ"
    },
    "tuong_hai": {
        "Tý": "Mùi", "Mùi": "Tý", "Sửu": "Ngọ", "Ngọ": "Sửu",
        "Dần": "Tỵ", "Tỵ": "Dần", "Mão": "Thìn", "Thìn": "Mão",
        "Thân": "Hợi", "Hợi": "Thân", "Dậu": "Tuất", "Tuất": "Dậu"
    }
}

# Bát Quái Tương Quan
TRIGRAM_DATA = {
    "Càn": {"element": "Kim", "nature": "Trời", "family": "Cha", "number": 1, "color": "#E2E8F0"},
    "Đoài": {"element": "Kim", "nature": "Đầm/Hồ", "family": "Út Nữ", "number": 2, "color": "#CBD5E1"},
    "Ly": {"element": "Hỏa", "nature": "Lửa", "family": "Trung Nữ", "number": 3, "color": "#F87171"},
    "Chấn": {"element": "Mộc", "nature": "Sấm", "family": "Trưởng Nam", "number": 4, "color": "#34D399"},
    "Tốn": {"element": "Mộc", "nature": "Gió", "family": "Trưởng Nữ", "number": 5, "color": "#6EE7B7"},
    "Khảm": {"element": "Thủy", "nature": "Nước", "family": "Trung Nam", "number": 6, "color": "#60A5FA"},
    "Cấn": {"element": "Thổ", "nature": "Núi", "family": "Út Nam", "number": 7, "color": "#FBBF24"},
    "Khôn": {"element": "Thổ", "nature": "Đất", "family": "Mẹ", "number": 8, "color": "#FCD34D"}
}

class WuxingRelation(dict):
    """Lớp đối tượng quan hệ ngũ hành hỗ trợ cả dict access và string matching."""
    def __init__(self, desc: str, rel_type: str = "Tỷ Hòa"):
        super().__init__(relation=desc, type=rel_type, description=desc)
        self.desc = desc
        
    def __str__(self):
        return self.desc
        
    def __repr__(self):
        return f"'{self.desc}'"
        
    def __contains__(self, item):
        return item in self.desc or super().__contains__(item)

def analyze_wuxing_interaction(source_elem: str, target_elem: str) -> WuxingRelation:
    """Xác định quan hệ sinh khắc giữa 2 ngũ hành."""
    if source_elem == target_elem:
        return WuxingRelation("Tỷ Hòa (Đồng thanh tương ứng, hỗ trợ bền vững)", rel_type="Tỷ Hòa")
    rel = WUXING_RELATIONS.get(source_elem, {})
    if rel.get("sinh") == target_elem:
        return WuxingRelation("Sinh Xuất (Chủ thể tiết khí dưỡng ngoại cảnh, hao tâm tổn trí)", rel_type="Sinh Xuất")
    if rel.get("sinh_boi") == target_elem:
        return WuxingRelation("Sinh Nhập (Ngoại cảnh trợ sinh chủ thể, đắc lực hanh thông)", rel_type="Sinh Nhập")
    if rel.get("khac") == target_elem:
        return WuxingRelation("Khắc Xuất (Chủ thể chế ngự ngoại cảnh, vất vả nhưng đắc quyền)", rel_type="Khắc Xuất")
    if rel.get("bi_khac") == target_elem:
        return WuxingRelation("Khắc Nhập (Chủ thể bị ngoại cảnh áp chế, trở ngại nguy khốn)", rel_type="Khắc Nhập")
    return WuxingRelation("Bình Hòa", rel_type="Bình Hòa")

def analyze_branch_pair(b1: str, b2: str) -> List[str]:
    """Phân tích toàn diện quan hệ giữa 2 Địa Chi."""
    tags = []
    if BRANCH_RELATIONS["luc_hop"].get(b1) == b2:
        tags.append(f"Lục Hợp ({b1}-{b2}: Hòa hợp, gắn kết, tương trợ)")
    if BRANCH_RELATIONS["luc_xung"].get(b1) == b2:
        tags.append(f"Lục Xung ({b1}-{b2}: Xung đột, dịch chuyển, biến động lớn)")
    if BRANCH_RELATIONS["tuong_hai"].get(b1) == b2:
        tags.append(f"Tương Hại ({b1}-{b2}: Bất hòa ngầm, phản trắc, trắc trở)")
        
    for group, elem in BRANCH_RELATIONS["tam_hop"].items():
        if b1 in group and b2 in group:
            tags.append(f"Bán Tam Hợp {elem} Cục ({b1}-{b2})")
            
    return tags
