"""
I Ching Cards & Oracle Tile Spreads Engine (Bốc Bài / Thẻ Gỗ Kinh Dịch — Đạo Quân Tử)
Supports 1, 2, 3, 5, Relationship (7 cards), and Dynamic Storytelling modes.
"""
import random
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Local imports
try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .luc_hao import HEXAGRAMS_64, PALACE_INFO
    from .atomic_clock import get_precise_atomic_now
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from luc_hao import HEXAGRAMS_64, PALACE_INFO
    from atomic_clock import get_precise_atomic_now

HEX_LIST = sorted(list(HEXAGRAMS_64.keys()))

TRIGRAM_SYMBOLS = {
    1: "☰", 2: "☱", 3: "☲", 4: "☳",
    5: "☴", 6: "☵", 7: "☶", 8: "☷"
}

def draw_random_card() -> Tuple[int, int]:
    return random.choice(HEX_LIST)

def draw_cards_without_replacement(n: int) -> List[Tuple[int, int]]:
    return random.sample(HEX_LIST, n)

def draw_cards_with_replacement(n: int) -> List[Tuple[int, int]]:
    return [random.choice(HEX_LIST) for _ in range(n)]

def get_hex_card_info(hex_pair):
    info = HEXAGRAMS_64[hex_pair]
    upper_id, lower_id = hex_pair
    palace_name = PALACE_INFO[info[2]]["name"]
    return {
        "pair": hex_pair,
        "name": info[0],
        "full_name": info[1],
        "palace": palace_name,
        "symbol": f"{TRIGRAM_SYMBOLS[upper_id]}/{TRIGRAM_SYMBOLS[lower_id]}",
        "the_line": info[3],
        "ung_line": info[4]
    }

def format_card_spread(spread_type: str, cards: List, question: str = "", context_meta: Dict = None) -> str:
    atomic_info = get_precise_atomic_now()
    dt = atomic_info["datetime"]
    time_coords = calculate_time_coordinates(dt)
    
    out = []
    if atomic_info.get("source") == "ATOMIC_QUANTUM_CLOCK":
        out.append(f"[Chuẩn Thời Gian: Đồng Hồ Nguyên Tử/Lượng Tử ({atomic_info.get('server')}) | RTT: {atomic_info.get('latency_ms')} ms]")
    out.append("=== PHƯƠNG PHÁP: BỐC BÀI / THẺ GỖ KINH DỊCH — ĐẠO QUÂN TỬ ===")
    out.append(f"Kiểu trải bài: {spread_type.upper()}")
    if question:
        out.append(f"Việc cần xem: {question}")
    out.append(f"Thời gian: {time_coords['solar']} ({time_coords['can_chi_hour']}, {time_coords['can_chi_day']}, {time_coords['can_chi_month']}, {time_coords['can_chi_year']})")
    out.append("")
    
    card_infos = [get_hex_card_info(c) for c in cards]
    
    if spread_type == "single" or len(cards) == 1:
        c = card_infos[0]
        out.append("=== TRẢI 1 QUẺ (ĐƠN QUẺ — THÔNG ĐIỆP CỐT LÕI) ===")
        out.append(f"Quẻ: {c['full_name'].upper()} (Họ {c['palace']}) [{c['symbol']}]")
        out.append(f"Ý nghĩa: Phản ánh trực tiếp bản chất năng lượng và lời chỉ dẫn trọng tâm.")
        
    elif spread_type == "two" or len(cards) == 2:
        out.append("=== TRẢI 2 QUẺ (HIỆN TRẠNG & XU HƯỚNG) ===")
        out.append(f"1. QUẺ HIỆN TRẠNG: {card_infos[0]['full_name'].upper()} (Họ {card_infos[0]['palace']}) [{card_infos[0]['symbol']}]")
        out.append(f"2. QUẺ XU HƯỚNG / LỜI KHUYÊN: {card_infos[1]['full_name'].upper()} (Họ {card_infos[1]['palace']}) [{card_infos[1]['symbol']}]")
        
    elif spread_type == "three" or len(cards) == 3:
        out.append("=== TRẢI 3 QUẺ (TAM TÀI: QUÁ KHỨ — HIỆN TẠI — TƯƠNG LAI) ===")
        out.append(f"1. QUẺ 1 (GỐC RỄ / NGUYÊN NHÂN): {card_infos[0]['full_name'].upper()} (Họ {card_infos[0]['palace']}) [{card_infos[0]['symbol']}]")
        out.append(f"2. QUẺ 2 (HIỆN TRẠNG / THỬ THÁCH): {card_infos[1]['full_name'].upper()} (Họ {card_infos[1]['palace']}) [{card_infos[1]['symbol']}]")
        out.append(f"3. QUẺ 3 (KẾT QUẢ / HƯỚNG PHÁT TRIỂN): {card_infos[2]['full_name'].upper()} (Họ {card_infos[2]['palace']}) [{card_infos[2]['symbol']}]")
        
    elif spread_type == "five" or len(cards) == 5:
        out.append("=== TRẢI 5 QUẺ (NGŨ HÀNH — TOÀN CẢNH ĐA DIỆN) ===")
        out.append(f"1. TRUNG CUNG (CỐT LÕI BẢN THỂ): {card_infos[0]['full_name'].upper()} (Họ {card_infos[0]['palace']}) [{card_infos[0]['symbol']}]")
        out.append(f"2. ĐÔNG PHƯƠNG (KHỞI ĐIỂM / ĐỘNG LỰC): {card_infos[1]['full_name'].upper()} (Họ {card_infos[1]['palace']}) [{card_infos[1]['symbol']}]")
        out.append(f"3. NAM PHƯƠNG (BIỂU HIỆN / KHÍ THẾ): {card_infos[2]['full_name'].upper()} (Họ {card_infos[2]['palace']}) [{card_infos[2]['symbol']}]")
        out.append(f"4. TÂY PHƯƠNG (HỆ QUẢ / THÀNH TỰU THỰC TẾ): {card_infos[3]['full_name'].upper()} (Họ {card_infos[3]['palace']}) [{card_infos[3]['symbol']}]")
        out.append(f"5. BẮC PHƯƠNG (MẠCH NGẦM / BÀI HỌC GIÁC NGỘ): {card_infos[4]['full_name'].upper()} (Họ {card_infos[4]['palace']}) [{card_infos[4]['symbol']}]")
        
    elif spread_type == "relationship" or len(cards) == 7:
        out.append("=== TRẢI MỐI QUAN HỆ (7 QUẺ — ĐỐI ỨNG TƯƠNG QUAN) ===")
        out.append("--- [BÊN TRÁI: NGƯỜI A / PHÍA BẢN THÂN] ---")
        out.append(f"  Quẻ 1 (Tâm thế / Cảm xúc): {card_infos[0]['full_name'].upper()} (Họ {card_infos[0]['palace']}) [{card_infos[0]['symbol']}]")
        out.append(f"  Quẻ 2 (Hành vi / Lối ứng xử): {card_infos[1]['full_name'].upper()} (Họ {card_infos[1]['palace']}) [{card_infos[1]['symbol']}]")
        out.append(f"  Quẻ 3 (Kỳ vọng / Nỗi niềm sâu kín): {card_infos[2]['full_name'].upper()} (Họ {card_infos[2]['palace']}) [{card_infos[2]['symbol']}]")
        out.append("")
        out.append("--- [BÊN PHẢI: NGƯỜI B / ĐỐI PHƯƠNG] ---")
        out.append(f"  Quẻ 4 (Tâm thế / Cảm xúc): {card_infos[3]['full_name'].upper()} (Họ {card_infos[3]['palace']}) [{card_infos[3]['symbol']}]")
        out.append(f"  Quẻ 5 (Hành vi / Lối ứng xử): {card_infos[4]['full_name'].upper()} (Họ {card_infos[4]['palace']}) [{card_infos[4]['symbol']}]")
        out.append(f"  Quẻ 6 (Kỳ vọng / Nỗi niềm sâu kín): {card_infos[5]['full_name'].upper()} (Họ {card_infos[5]['palace']}) [{card_infos[5]['symbol']}]")
        out.append("")
        out.append("--- [TRỌNG TÂM: MỐI QUAN HỆ CHUNG] ---")
        out.append(f"  Quẻ 7 (Bản chất liên kết & Dòng chảy chung): {card_infos[6]['full_name'].upper()} (Họ {card_infos[6]['palace']}) [{card_infos[6]['symbol']}]")
        
    elif spread_type == "story":
        out.append("=== TRẢI THEO MẠCH CÂU CHUYỆN (DYNAMIC STORYLINE SPREAD) ===")
        out.append("Quy tắc: Bốc 1 quẻ cho từng tình tiết -> Chiêm nghiệm -> Bỏ lại bộ bài & xào lại -> Bốc tình tiết tiếp theo.")
        out.append("")
        stages = (context_meta and context_meta.get("stages")) or [f"Tình tiết {i+1}" for i in range(len(card_infos))]
        for idx, (c, stage_name) in enumerate(zip(card_infos, stages), 1):
            out.append(f"• [Hồi {idx} - {stage_name}]: {c['full_name'].upper()} (Họ {c['palace']}) [{c['symbol']}]")
            
    return "\n".join(out)
