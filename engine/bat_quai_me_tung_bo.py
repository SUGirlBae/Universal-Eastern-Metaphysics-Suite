"""
Bát Quái Mê Tung Bộ (八卦迷踪步 - Eight Trigrams Phantom Labyrinth Stepping Footwork Engine)
Comprehensive Daoist Metaphysics, Internal Martial Arts, Qi Cultivation & Strategic Spatial Locomotion System.

Core Pillars:
1. Nine-Palace Spatial Matrix (Lạc Thư Cửu Cung: Đới cửu lý nhất, tả tam hữu thất, nhị tứ vi kiên, lục bát vi túc, ngũ cư trung ương).
2. Trigram Attributes & 8 Directions (Càn, Khảm, Cấn, Chấn, Tốn, Ly, Khôn, Đoài + Trung Cung).
3. 3 Canonical Stepping Trajectories:
   - Dương Độn Thuận Hành (Tiến bộ Tương Sinh: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 1)
   - Âm Độn Nghịch Hành (Thoái bộ Tương Khắc / Triệt Phá: 9 -> 8 -> 7 -> 6 -> 5 -> 4 -> 3 -> 2 -> 1 -> 9)
   - Bát Quái Mê Tung Biến Hoán (Vũ Bộ Đạp Đẩu / Bắc Đẩu Thất Tinh Thân Pháp - The Phantom Labyrinth Route)
4. Yin-Yang Stepping Mechanics (Thực Bộ vs. Hư Bộ, Trọng tâm di chuyển, Khí cơ Đan Điền).
5. Hexagram Line Changing Dynamics (Mỗi bước biến hào, dịch chuyển tọa độ 64 quẻ).
6. Time & Qimen Strategic Synchronization (Phối hợp Tiết Khí, Bát Môn Sinh/Khai/Tử/Kinh).
7. Daoist Health & Internal Alchemy (Kỳ Kinh Bát Mạch, Thở Quy Tức, Đả thông Nhâm Đốc).
8. ASCII & Step-by-Step Visualization Matrix.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ, CAN, CHI
    from .ky_mon_engine import calculate_ky_mon
    from .luc_hao import HEXAGRAMS_64, PALACE_INFO
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ, CAN, CHI
    from ky_mon_engine import calculate_ky_mon
    from luc_hao import HEXAGRAMS_64, PALACE_INFO

# 9 Palaces Spatial Definition (Lạc Thư & Hậu Thiên Bát Quái)
NINE_PALACES: Dict[int, Dict[str, Any]] = {
    1: {
        "palace_num": 1,
        "trigram": "Khảm",
        "element": "Thủy",
        "direction": "Chính Bắc (0° / 360°)",
        "step_name": "Hư Thủy Bộ (Huyễn Ảnh Bộ)",
        "step_nature": "Hư bộ (Âm), thân pháp chìm xuống nương theo nước, ẩn tàng khí cơ, vô tung vô ảnh.",
        "breathing": "Thở ra từ từ, hạ khí xuống Đan Điền, thả lỏng toàn bộ khớp.",
        "martial_app": "Thoát hiểm khi bị vây hãm, hóa giải lực đánh trực diện, luồn ra sau lưng đối phương.",
        "health_benefit": "Dưỡng Thận Thủy, thanh lọc độc tố bàng quang, làm dịu tâm hỏa lo âu.",
        "meridian": "Kinh Thận & Bàng Quang (Nhâm Mạch)"
    },
    2: {
        "palace_num": 2,
        "trigram": "Khôn",
        "element": "Thổ",
        "direction": "Tây Nam (225°)",
        "step_name": "Nhu Thổ Bộ (Hậu Đức Bộ)",
        "step_nature": "Thực bộ (Âm), bước chân vững chãi đôn hậu như đất mẹ, bao dung thu nạp vạn vật.",
        "breathing": "Hít sâu bằng mũi, quán tưởng năng lượng đất mẹ nâng đỡ lòng bàn chân (Dũng Tuyền).",
        "martial_app": "Triệt hạ trọng tâm đối thủ, dùng nhu thắng cương, chuyển hướng lực quán tính.",
        "health_benefit": "Dưỡng Tỳ Vị, hỗ trợ hệ tiêu hóa, tiêu trừ ẩm thấp trong cơ thể.",
        "meridian": "Kinh Tỳ & Vị"
    },
    3: {
        "palace_num": 3,
        "trigram": "Chấn",
        "element": "Mộc",
        "direction": "Chính Đông (90°)",
        "step_name": "Lôi Đình Bộ (Kinh Lôi Bộ)",
        "step_nature": "Bộc phát (Dương), đạp gót phóng mũi, nhanh như sấm sét xé toạc không gian.",
        "breathing": "Ngưng khí 1 nhịp ngắn ở Đan Điền rồi phát lực nhanh qua hơi thở mạnh.",
        "martial_app": "Đột kích bất ngờ, chiếm thế thượng phong, áp sát thần tốc làm đối phương trở tay không kịp.",
        "health_benefit": "Sơ can lý khí, kích hoạt chức năng Gan và Mật, giải tỏa uất ức nội tâm.",
        "meridian": "Kinh Can & Đởm"
    },
    4: {
        "palace_num": 4,
        "trigram": "Tốn",
        "element": "Mộc",
        "direction": "Đông Nam (135°)",
        "step_name": "Phong Hành Bộ (Phiêu Diêu Bộ)",
        "step_nature": "Uyển chuyển (Âm), thân hình mềm mại như gió thổi qua rặng tre, luồn lách qua khe hẹp.",
        "breathing": "Hít thở đều đặn, nhịp nhàng theo chuyển động tròn của hông và vai.",
        "martial_app": "Vờn quanh góc chết của đối thủ, liên tục thay đổi cự ly, tránh đối đầu trực diện.",
        "health_benefit": "Lưu thông khí huyết toàn thân, giãn gân cốt vùng hông đùi và cột sống.",
        "meridian": "Đới Mạch & Kinh Đởm"
    },
    5: {
        "palace_num": 5,
        "trigram": "Trung Cung",
        "element": "Thổ (Hoàng Cực)",
        "direction": "Trung Ương (Tâm điểm chuyển trục)",
        "step_name": "Thái Cực Định Tâm Bộ (Hoàng Cực Bộ)",
        "step_nature": "Định vị (Trung Dung), đứng tại tâm xoay chuyển 8 hướng, điều phối toàn bộ khí trường.",
        "breathing": "Quy Tức Pháp (Thở bụng sâu và êm như rùa thở), tĩnh lặng tuyệt đối.",
        "martial_app": "Quan sát toàn cảnh, làm chủ không gian chiến lược, biến nguy thành an.",
        "health_benefit": "Cân bằng âm dương toàn cơ thể, hợp nhất Chân Khí về Đan Điền Trung Ương.",
        "meridian": "Đốc Mạch & Nhâm Mạch (Hợp nhất Chu Thiên)"
    },
    6: {
        "palace_num": 6,
        "trigram": "Càn",
        "element": "Kim",
        "direction": "Tây Bắc (315°)",
        "step_name": "Cương Kim Bộ (Kình Thiên Bộ)",
        "step_nature": "Cương kiện (Dương), bước chân dứt khoát uy lực, khí phách ngút trời của bậc đế vương.",
        "breathing": "Hít căng lồng ngực, mở rộng vai, giữ tâm thế uy nghiêm chính đại.",
        "martial_app": "Đánh thẳng vào trung lộ, áp đảo khí thế, phá tan thế trận phòng thủ.",
        "health_benefit": "Bổ Phế khí, tăng cường dung tích phổi và hệ miễn dịch toàn thân.",
        "meridian": "Kinh Phế & Đại Trường"
    },
    7: {
        "palace_num": 7,
        "trigram": "Đoài",
        "element": "Kim",
        "direction": "Chính Tây (270°)",
        "step_name": "Trạch Huyễn Bộ (Lạc Huyễn Bộ)",
        "step_nature": "Biến huyễn (Âm), lừa gạt thị giác, bước trái nhưng lách phải, làm đối phương mất phương hướng.",
        "breathing": "Thở nhẹ nhàng bằng miệng, thả lỏng quai hàm và cơ mặt.",
        "martial_app": "Phản đòn bất ngờ, đánh lừa phản xạ của đối thủ, chiếm lĩnh khoảng trống.",
        "health_benefit": "Thanh nhiệt nhuận phế, hỗ trợ thanh quản và điều hòa cảm xúc hoan hỷ.",
        "meridian": "Kinh Phế & Đại Trường"
    },
    8: {
        "palace_num": 8,
        "trigram": "Cấn",
        "element": "Thổ",
        "direction": "Đông Bắc (45°)",
        "step_name": "Trầm Sơn Bộ (Chỉ Bộ)",
        "step_nature": "Trầm ổn (Dương), đứng vững như núi Thái Sơn, khóa chặt không gian, bất khả xâm phạm.",
        "breathing": "Nén khí xuống hạ bàn, bám chặt 10 đầu ngón chân xuống mặt đất.",
        "martial_app": "Chặn đứng đà tấn công dữ dội của địch, làm tường chắn bảo vệ yếu nhân/vị trí hiểm yếu.",
        "health_benefit": "Củng cố khớp xương, cột sống thắt lưng và dây chằng chi dưới.",
        "meridian": "Kinh Vị & Đốc Mạch"
    },
    9: {
        "palace_num": 9,
        "trigram": "Ly",
        "element": "Hỏa",
        "direction": "Chính Nam (180°)",
        "step_name": "Liệt Hỏa Bộ (Quang Minh Bộ)",
        "step_nature": "Thần tốc (Dương), bừng sáng chói lòa như ngọn lửa bùng cháy, di chuyển nhanh hơn tốc độ mắt nhìn.",
        "breathing": "Thở gấp ngắn kết hợp xuất lực nhanh, kích thích tuần hoàn máu tối đa.",
        "martial_app": "Truy kích mục tiêu, kết liễu nhanh chóng, tỏa sáng tạo đột biến trận địa.",
        "health_benefit": "Trợ Tâm Hỏa, kích hoạt tuần hoàn máu não, tăng cường sự minh mẫn sắc bén.",
        "meridian": "Kinh Tâm & Tiểu Trường"
    }
}

# 3 Canonical Trajectories
TRAJECTORIES = {
    "duong_don_thuan": {
        "name": "Dương Độn Thuận Cửu Cung (Tiến Bộ Tương Sinh)",
        "type": "YANG_FORWARD",
        "path": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1],
        "description": "Quỹ đạo sinh trưởng của Khí Dương: Khởi Khảm Thủy -> Khôn Thổ -> Chấn Mộc -> Tốn Mộc -> Trung Thổ -> Càn Kim -> Đoài Kim -> Cấn Thổ -> Ly Hỏa -> Hồi quy Khảm. Dùng khi cầu tài lộc, dưỡng sinh, khai mở cơ hội mới và hòa giải phong thủy.",
        "strategic_intent": "Tăng cường sinh khí, nạp năng lượng đất trời, mở rộng không gian hành động."
    },
    "am_don_nghich": {
        "name": "Âm Độn Nghịch Cửu Cung (Thoái Bộ Tương Khắc / Triệt Phá)",
        "type": "YIN_BACKWARD",
        "path": [9, 8, 7, 6, 5, 4, 3, 2, 1, 9],
        "description": "Quỹ đạo thâu liễm của Khí Âm: Khởi Ly Hỏa -> Cấn Thổ -> Đoài Kim -> Càn Kim -> Trung Thổ -> Tốn Mộc -> Chấn Mộc -> Khôn Thổ -> Khảm Thủy -> Hồi quy Ly. Dùng khi phòng thủ, hóa giải sát khí, hóa giải vòng vây và ẩn nặc thân hình.",
        "strategic_intent": "Triệt tiêu áp lực ngoại cảnh, lui bước an toàn, bảo toàn chân khí."
    },
    "bat_quai_me_tung": {
        "name": "Bát Quái Mê Tung Biến Hoán (Vũ Bộ Đạp Đẩu / Bắc Đẩu Thất Tinh Thân Pháp)",
        "type": "PHANTOM_LABYRINTH",
        "path": [1, 7, 3, 9, 5, 2, 6, 4, 8, 5, 1],
        "description": "Quỹ đạo mê cung huyền thoại kết hợp Vũ Bộ Đạp Đẩu và Bắc Đẩu Thất Tinh (Tham Lang -> Cự Môn -> Lộc Tồn -> Văn Khúc -> Liêm Trinh -> Vũ Khúc -> Phá Quân). Bước chân thoắt Bắc thoắt Tây, thoắt Đông thoắt Nam, làm cho ngoại giới không thể đoán định phương hướng.",
        "strategic_intent": "Gây nhiễu loạn toàn diện phán đoán của đối phương, tạo ảo ảnh thân pháp, chuyển bại thành thắng."
    }
}


def calculate_bat_quai_me_tung_bo(
    dt: Optional[datetime] = None,
    trajectory_type: str = "bat_quai_me_tung",
    start_palace: Optional[int] = None,
    target_intent: str = "Tự vệ chiến lược & Dưỡng sinh khí cơ",
    user_gender: int = 1
) -> Dict[str, Any]:
    """
    Tính toán chi tiết hệ thống Bát Quái Mê Tung Bộ theo thời gian thực hoặc cấu hình tùy chọn.
    - dt: Thời điểm kích hoạt thân pháp (tính giờ Kỳ Môn & Tiết Khí)
    - trajectory_type: 'duong_don_thuan' | 'am_don_nghich' | 'bat_quai_me_tung'
    - start_palace: 1 đến 9 (Cung khởi bước, mặc định lấy cung đầu tiên của quỹ đạo)
    - target_intent: Mục đích hành động
    """
    if dt is None:
        dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        
    tc = calculate_time_coordinates(dt)
    tiet_khi = tc.get("tiet_khi", "Tiểu Tuyết")
    
    if trajectory_type not in TRAJECTORIES:
        trajectory_type = "bat_quai_me_tung"
        
    traj_info = TRAJECTORIES[trajectory_type]
    raw_path = traj_info["path"]
    
    if start_palace is not None and start_palace in NINE_PALACES and start_palace != raw_path[0]:
        if start_palace in raw_path:
            idx = raw_path.index(start_palace)
            path = raw_path[idx:] + raw_path[1:idx+1]
        else:
            path = [start_palace] + raw_path
    else:
        path = raw_path
        
    steps: List[Dict[str, Any]] = []
    accumulated_element_flow: List[str] = []
    
    for step_num, p_num in enumerate(path, 1):
        p_data = NINE_PALACES[p_num]
        accumulated_element_flow.append(p_data["element"])
        
        step_entry = {
            "step_order": step_num,
            "palace_num": p_num,
            "trigram": p_data["trigram"],
            "element": p_data["element"],
            "direction": p_data["direction"],
            "step_name": p_data["step_name"],
            "action_guidance": p_data["step_nature"],
            "breathing_technique": p_data["breathing"],
            "tactical_application": p_data["martial_app"],
            "internal_health_benefit": p_data["health_benefit"],
            "active_meridian": p_data["meridian"]
        }
        steps.append(step_entry)
        
    ascii_grid = _generate_ascii_labyrinth_grid(path)
    
    tactical_summary = {
        "trajectory_name": traj_info["name"],
        "total_steps": len(steps),
        "start_direction": NINE_PALACES[path[0]]["direction"],
        "finish_direction": NINE_PALACES[path[-1]]["direction"],
        "element_chain": " -> ".join(accumulated_element_flow),
        "strategic_intent": traj_info["strategic_intent"],
        "detailed_guidance": traj_info["description"]
    }
    
    formatted_report = format_bat_quai_me_tung_report(
        dt=dt,
        tc=tc,
        tactical_summary=tactical_summary,
        steps=steps,
        ascii_grid=ascii_grid,
        target_intent=target_intent
    )
    
    return {
        "timestamp_iso": dt.isoformat(),
        "time_coordinates": {
            "solar_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_datetime": f"{tc['lunar_day']:02d}/{tc['lunar_month']:02d}/{tc['lunar_year']}",
            "pillars": f"{tc['can_chi_year']} - {tc['can_chi_month']} - {tc['can_chi_day']} - {tc['can_chi_hour']}",
            "solar_term": tiet_khi
        },
        "target_intent": target_intent,
        "trajectory": tactical_summary,
        "stepping_sequence": steps,
        "ascii_matrix_grid": ascii_grid,
        "formatted_report": formatted_report
    }


def _generate_ascii_labyrinth_grid(path: List[int]) -> str:
    """Tạo biểu đồ trực quan ASCII ma trận 9 cung Lạc Thư với đường đi bước chân."""
    step_indices: Dict[int, List[int]] = {i: [] for i in range(1, 10)}
    for s_idx, p in enumerate(path, 1):
        step_indices[p].append(s_idx)
        
    def fmt_cell(p_num: int, name: str, elem: str) -> str:
        s_list = step_indices.get(p_num, [])
        s_str = ",".join(str(x) for x in s_list) if s_list else "—"
        return f"[{p_num}:{name} ({elem}) | Bước: {s_str}]"
        
    c4 = fmt_cell(4, "TỐN", "Mộc")
    c9 = fmt_cell(9, "LY", "Hỏa")
    c2 = fmt_cell(2, "KHÔN", "Thổ")
    
    c3 = fmt_cell(3, "CHẤN", "Mộc")
    c5 = fmt_cell(5, "TRUNG", "Thổ")
    c7 = fmt_cell(7, "ĐOÀI", "Kim")
    
    c8 = fmt_cell(8, "CẤN", "Thổ")
    c1 = fmt_cell(1, "KHẢM", "Thủy")
    c6 = fmt_cell(6, "CÀN", "Kim")
    
    grid = [
        "┌───────────────────────────┬───────────────────────────┬───────────────────────────┐",
        f"│ {c4:<25} │ {c9:<25} │ {c2:<25} │",
        "├───────────────────────────┼───────────────────────────┼───────────────────────────┤",
        f"│ {c3:<25} │ {c5:<25} │ {c7:<25} │",
        "├───────────────────────────┼───────────────────────────┼───────────────────────────┤",
        f"│ {c8:<25} │ {c1:<25} │ {c6:<25} │",
        "└───────────────────────────┴───────────────────────────┴───────────────────────────┘"
    ]
    return "\n".join(grid)


def format_bat_quai_me_tung_report(
    dt: datetime,
    tc: Dict[str, Any],
    tactical_summary: Dict[str, Any],
    steps: List[Dict[str, Any]],
    ascii_grid: str,
    target_intent: str
) -> str:
    """Định dạng báo cáo Bát Quái Mê Tung Bộ chuẩn mực cao cấp."""
    out = []
    out.append("================================================================================")
    out.append("   ĐẠI BẢN ĐỒ THÂN PHÁP: BÁT QUÁI MÊ TUNG BỘ (EIGHT TRIGRAMS PHANTOM FOOTWORK)")
    out.append("   Hệ Thống Thân Pháp Cửu Cung Lạc Thư - Vũ Bộ Đạp Đẩu - Khí Cơ Đan Đạo")
    out.append("================================================================================")
    out.append(f"Thời Điểm Khởi Bộ: {dt.strftime('%d/%m/%Y %H:%M:%S')} | Tiết Khí: {tc.get('tiet_khi', '')}")
    out.append(f"Tứ Trụ Khí Cơ     : {tc['can_chi_year']} - {tc['can_chi_month']} - {tc['can_chi_day']} - {tc['can_chi_hour']}")
    out.append(f"Dụng Ý Chiến Lược : {target_intent}")
    out.append(f"Quỹ Đạo Thân Pháp : {tactical_summary['trajectory_name']} ({tactical_summary['total_steps']} bước)")
    out.append(f"Dòng Chảy Ngũ Hành: {tactical_summary['element_chain']}")
    out.append("")
    out.append("【I. MA TRẬN ĐỒ HÌNH CỬU CUNG BƯỚC CHÂN (LẠC THƯ PHANTOM MATRIX)】")
    out.append(ascii_grid)
    out.append("")
    out.append("【II. HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC CHÂN & KHÍ CƠ (STEP-BY-STEP PROTOCOL)】")
    for s in steps:
        out.append(f"  👣 BƯỚC {s['step_order']:02d}: Cung {s['palace_num']} [{s['trigram']} - {s['element']}] ({s['direction']})")
        out.append(f"     • Thân Pháp   : {s['step_name']} - {s['action_guidance']}")
        out.append(f"     • Thở Khí Công: {s['breathing_technique']}")
        out.append(f"     • Ứng Dụng    : {s['tactical_application']}")
        out.append(f"     • Dưỡng Sinh  : {s['internal_health_benefit']} [{s['active_meridian']}]")
        out.append("")
    out.append("【III. ĐẠI KẾT LUẬN CHIẾN LƯỢC & TÂM PHÁP THÂN PHÁP】")
    out.append(f"  💡 {tactical_summary['strategic_intent']}")
    out.append(f"  📜 {tactical_summary['detailed_guidance']}")
    out.append("================================================================================")
    return "\n".join(out)
