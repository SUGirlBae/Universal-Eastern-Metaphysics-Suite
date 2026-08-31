"""
Standard JSON-RPC Stdio Model Context Protocol (MCP) Server
Allows Antigravity, Claude Code, Cursor, Windsurf to directly call Metaphysics tools.
Features:
- Universal Tu Vi (110+ stars, 12 Cung Phi Tinh, Tự Hóa/Hướng Tâm, Phương Viên Toàn Đồ, Khâm Thiên routes)
- Zero-Diff Ground-Truth Verification (Canonical-Astrolabe-Engine 3-Table parser & 7-step comparator)
- Multi-Century High-Throughput Stress Testing Pipeline
- Deterministic Random & Edge-Case Vector Generator
- Full Master Synthesis & Cross-Matrix Systems
"""
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "engine"))

try:
    from engine.agent_facade import (
        get_agent_payload,
        get_universal_tu_vi_payload,
        run_ziwei_stress_test,
        compare_ground_truth_canonical_astrolabe,
        generate_ziwei_vectors
    )
    from engine.lunar_solar import LOCAL_TZ
    from engine.annual_forecast import calculate_annual_forecast
    from engine.dan_dao_health import diagnose_dan_dao_health
    from engine.feng_shui import calculate_feng_shui_period9
    from engine.bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo
    from engine.synthesis_engine import run_master_synthesis
    from engine.memory_query import query_memory, get_memory_stats, get_person_journey
    from engine.person_profile import add_person, find_person, get_person
    from engine.similarity_finder import find_similar_cases, find_similar_persons
except ImportError:
    from agent_facade import (
        get_agent_payload,
        get_universal_tu_vi_payload,
        run_ziwei_stress_test,
        compare_ground_truth_canonical_astrolabe,
        generate_ziwei_vectors
    )
    from lunar_solar import LOCAL_TZ
    from annual_forecast import calculate_annual_forecast
    from dan_dao_health import diagnose_dan_dao_health
    from feng_shui import calculate_feng_shui_period9
    from bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo
    from synthesis_engine import run_master_synthesis
    from memory_query import query_memory, get_memory_stats, get_person_journey
    from person_profile import add_person, find_person, get_person
    from similarity_finder import find_similar_cases, find_similar_persons

def parse_dt_helper(t_str: Optional[str]) -> datetime:
    if not t_str:
        return datetime.now().replace(tzinfo=LOCAL_TZ)
    t_str = t_str.strip()
    for fmt in [
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M",
        "%d-%m-%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d"
    ]:
        try:
            return datetime.strptime(t_str, fmt).replace(tzinfo=LOCAL_TZ)
        except ValueError:
            continue
    return datetime.now().replace(tzinfo=LOCAL_TZ)

TOOLS_SCHEMA = [
    {
        "name": "metaphysics_agent_query",
        "description": "Truy xuất dữ liệu cấu trúc toàn diện 6 môn thuật số kinh điển cổ thư Á Đông (Kinh Dịch, Bát Tự, Tử Vi Đa Phái, Hà Lạc, Kỳ Môn, Tung Shing) tối ưu cho AI Agent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "Thời gian (DD/MM/YYYY HH:MM) hoặc để trống lấy hiện tại"},
                "question": {"type": "string", "description": "Mục tiêu vấn sự / câu hỏi cần giải quyết"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ (mặc định 1)"},
                "systems": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách phân hệ ['iching', 'bazi', 'tuvi', 'halac', 'kymon', 'timing', 'annual', 'health', 'fengshui']"
                },
                "school": {"type": "string", "enum": ["standard", "kham_thien", "nam_phai", "trung_chau", "luong_phai", "bac_phai", "hybrid"], "description": "Trường phái Tử Vi"},
                "astrolabe_type": {"type": "string", "enum": ["thien_ban", "dia_ban", "nhan_ban"], "description": "Loại Bàn Tử Vi"},
                "cuc_override": {"type": "integer", "enum": [2, 3, 4, 5, 6], "description": "Tùy biến Cục Số (2=Thủy, 3=Mộc, 4=Kim, 5=Thổ, 6=Hỏa)"}
            }
        }
    },
    {
        "name": "calculate_universal_tu_vi",
        "description": "Lập lá số Tử Vi Đẩu Số Đa Phái Toàn Diện (110+ sao, Miếu Vượng Đắc Hãm, Ma trận 12 Cung Phi Tinh, Tự Hóa/Hướng Tâm, Phương Viên Lộc Kỵ Toàn Đồ, Khâm Thiên Khí Đạo).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "Thời gian sinh (DD/MM/YYYY HH:MM)"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ"},
                "school": {"type": "string", "enum": ["standard", "kham_thien", "nam_phai", "trung_chau", "luong_phai", "bac_phai", "hybrid"], "description": "Trường phái tính toán"},
                "astrolabe_type": {"type": "string", "enum": ["thien_ban", "dia_ban", "nhan_ban"], "description": "Loại bàn (Thiên Bàn, Địa Bàn, Nhân Bàn)"},
                "cuc_override": {"type": "integer", "enum": [2, 3, 4, 5, 6], "description": "Ép Cục số tùy biến"}
            },
            "required": ["datetime_str"]
        }
    },
    {
        "name": "compare_canonical_astrolabe_ground_truth",
        "description": "Bóc tách định dạng 3 bảng 'Dùng cho AI - Nhấn sao chép' từ Canonical-Astrolabe-Engine và đối chiếu Zero-Diff 7 bước với Động Cơ nội bộ.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "markdown_text": {"type": "string", "description": "Toàn văn chuỗi Markdown 3 bảng sao chép từ Canonical-Astrolabe-Engine hoặc đường dẫn file"},
                "datetime_str": {"type": "string", "description": "Tùy chọn thời gian đối chiếu nếu không lấy từ Markdown"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "Giới tính (1: Nam, 0: Nữ)"},
                "school": {"type": "string", "description": "Trường phái cấu hình (standard, kham_thien, nam_phai, ...)"},
                "cuc_override": {"type": "integer", "description": "Tùy biến Cục Số nếu cần"}
            },
            "required": ["markdown_text"]
        }
    },
    {
        "name": "run_ziwei_stress_test",
        "description": "Chạy kiểm thử tải cao đa thế kỷ (1900-2100) với hàng ngàn vector ngẫu nhiên & ca biên, đo lường tốc độ <2ms/lá số và tỷ lệ 0 crash.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "num_vectors": {"type": "integer", "description": "Số lượng vector kiểm thử tải (mặc định 1000)"}
            }
        }
    },
    {
        "name": "generate_ziwei_test_vectors",
        "description": "Tạo sinh hàng loạt vector ngày giờ sinh ngẫu nhiên đa thế kỷ (1900-2100) và 6 nhóm ca biên phức tạp (năm nhuận, tiết khí, giờ Tý, cục số).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Số lượng vector ngẫu nhiên cần sinh (mặc định 100)"},
                "include_edge_cases": {"type": "boolean", "description": "Kèm theo bộ ca biên chuẩn (mặc định true)"},
                "seed": {"type": "integer", "description": "Seed khởi tạo ngẫu nhiên"}
            }
        }
    },
    {
        "name": "get_annual_forecast",
        "description": "Dự báo thời vận 12 tháng cả năm (Lục Hào 6 hào, Tử Bình Lưu Niên, Tử Vi Lưu Thái Tuế & Tứ Hóa, Kỳ Môn Niên Cục).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "year": {"type": "integer", "description": "Năm cần dự báo (VD: 2026)"},
                "question": {"type": "string", "description": "Chủ đề / vấn sự quan tâm"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ"}
            },
            "required": ["year"]
        }
    },
    {
        "name": "get_dan_dao_health_diagnosis",
        "description": "Chẩn đoán cân bằng ngũ tạng đông y, kinh lạc khí cơ và hướng dẫn dưỡng sinh Đan Đạo Đạo Gia.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "Ngày giờ sinh (DD/MM/YYYY HH:MM)"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ"}
            },
            "required": ["datetime_str"]
        }
    },
    {
        "name": "get_feng_shui_period9",
        "description": "Tính toán Phong Thủy Huyền Không Phi Tinh Vận 9 (2024-2043) và Bát Trạch Cung Phi cho 24 Sơn Hướng.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "facing_mountain": {"type": "string", "description": "Sơn Hướng trong 24 sơn (VD: 'Tý', 'Ngọ', 'Càn', 'Tốn')"},
                "birth_year": {"type": "integer", "description": "Năm sinh để tính Cung Phi Bát Trạch"}
            },
            "required": ["facing_mountain"]
        }
    },
    {
        "name": "get_master_synthesis",
        "description": "Tổng hợp Đại Hợp Trí Toàn Diện qua 6 môn thuật số kinh điển cổ thư Á Đông.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "Thời gian (DD/MM/YYYY HH:MM)"},
                "question": {"type": "string", "description": "Vấn sự cần giải quyết"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ"}
            }
        }
    },
    {
        "name": "memory_add_person",
        "description": "Thêm hoặc cập nhật hồ sơ cá nhân vào tầng nhớ L5, tự động trích xuất vân tay Bát Tự & Tử Vi.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Họ và tên hoặc danh xưng"},
                "birth_dt": {"type": "string", "description": "Ngày giờ sinh (DD/MM/YYYY HH:MM)"},
                "gender": {"type": "integer", "enum": [0, 1], "description": "1: Nam, 0: Nữ"},
                "relationship": {"type": "string", "description": "Quan hệ với người dùng (em trai, bạn thân, khách...)"},
                "notes": {"type": "string", "description": "Ghi chú đặc điểm cá nhân"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "memory_query_federated",
        "description": "Truy vấn hợp nhất đa tầng (L0-L5): Cổ thư kinh điển (L1), Quy tắc cao nhân (L2), Mẫu hình tinh luyện (L4), Hồ sơ cá nhân (L5).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Chủ đề / Vấn sự tra cứu"},
                "discipline": {"type": "string", "description": "Phân hệ thuật số"},
                "person_id": {"type": "integer", "description": "ID hồ sơ cá nhân"}
            }
        }
    },
    {
        "name": "memory_get_person_journey",
        "description": "Xem toàn bộ hành trình chiêm nghiệm và các cá nhân có cấu trúc mệnh lý tương đồng (L5 Resonance).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "person_id": {"type": "integer", "description": "ID hồ sơ cá nhân"}
            },
            "required": ["person_id"]
        }
    },
    {
        "name": "memory_get_system_stats",
        "description": "Xem báo cáo tổng hợp toàn bộ kho tri thức, tỷ lệ kiểm chứng thực tế và số lượng mẫu hình tinh luyện.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "calculate_bat_quai_me_tung_bo",
        "description": "Tính toán sơ đồ thân pháp Bát Quái Mê Tung Bộ (Lạc Thư Cửu Cung, Vũ Bộ Đạp Đẩu, Khí Cơ Đan Đạo, Hướng Dẫn Từng Bước Chân).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "datetime_str": {"type": "string", "description": "Thời điểm khởi bộ (DD/MM/YYYY HH:MM)"},
                "trajectory_type": {"type": "string", "enum": ["bat_quai_me_tung", "duong_don_thuan", "am_don_nghich"], "description": "Loại quỹ đạo thân pháp"},
                "start_palace": {"type": "integer", "description": "Cung khởi bước (1-9)"},
                "target_intent": {"type": "string", "description": "Dụng ý chiến lược khởi bộ"}
            }
        }
    }
]

def handle_rpc_request(req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    msg_id = req.get("id")
    
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS_SCHEMA
            }
        }
        
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        
        try:
            if name == "metaphysics_agent_query":
                dt = parse_dt_helper(args.get("datetime_str"))
                q = args.get("question", "")
                g = args.get("gender", 1)
                sys_list = args.get("systems", None)
                sch = args.get("school", "standard")
                ast = args.get("astrolabe_type", "thien_ban")
                cuc = args.get("cuc_override", None)
                
                res = get_agent_payload(
                    dt=dt,
                    question=q,
                    gender=g,
                    systems=sys_list,
                    school=sch,
                    astrolabe_type=ast,
                    cuc_override=cuc
                )
                
            elif name == "calculate_universal_tu_vi":
                dt = parse_dt_helper(args.get("datetime_str"))
                g = args.get("gender", 1)
                sch = args.get("school", "standard")
                ast = args.get("astrolabe_type", "thien_ban")
                cuc = args.get("cuc_override", None)
                res = get_universal_tu_vi_payload(
                    dt=dt,
                    gender=g,
                    school=sch,
                    astrolabe_type=ast,
                    cuc_override=cuc
                )
                
            elif name == "compare_canonical_astrolabe_ground_truth":
                md_text = args.get("markdown_text", "")
                dt_str = args.get("datetime_str")
                dt = parse_dt_helper(dt_str) if dt_str else None
                g = args.get("gender", 1)
                sch = args.get("school", "standard")
                cuc = args.get("cuc_override", None)
                res = compare_ground_truth_canonical_astrolabe(
                    content_or_filepath=md_text,
                    dt=dt,
                    gender=g,
                    school=sch,
                    cuc_override=cuc
                )
                
            elif name == "run_ziwei_stress_test":
                n_vec = args.get("num_vectors", 1000)
                res = run_ziwei_stress_test(num_vectors=n_vec)
                
            elif name == "generate_ziwei_test_vectors":
                cnt = args.get("count", 100)
                inc_edge = args.get("include_edge_cases", True)
                sd = args.get("seed", 42)
                res = generate_ziwei_vectors(count=cnt, include_edge_cases=inc_edge, seed=sd)
                
            elif name == "get_annual_forecast":
                yr = args.get("year", datetime.now().year)
                q = args.get("question", "")
                g = args.get("gender", 1)
                res = calculate_annual_forecast(yr, question=q, gender=g)
                
            elif name == "get_dan_dao_health_diagnosis":
                dt = parse_dt_helper(args.get("datetime_str"))
                g = args.get("gender", 1)
                res = diagnose_dan_dao_health(dt, gender=g)
                
            elif name == "get_feng_shui_period9":
                fm = args.get("facing_mountain", "Tý")
                by = args.get("birth_year", None)
                g = args.get("gender", 1)
                res = calculate_feng_shui_period9(fm, birth_year=by, gender=g)
                
            elif name == "memory_add_person":
                pid = add_person(
                    name=args.get("name"),
                    birth_dt=args.get("birth_dt"),
                    gender=args.get("gender", 1),
                    relationship=args.get("relationship"),
                    notes=args.get("notes")
                )
                res = get_person(pid)
                
            elif name == "memory_query_federated":
                res = query_memory(
                    question=args.get("question", ""),
                    discipline=args.get("discipline"),
                    person_id=args.get("person_id")
                )
                
            elif name == "memory_get_person_journey":
                res = get_person_journey(person_id=args.get("person_id"))
                
            elif name == "memory_get_system_stats":
                res = get_memory_stats()

            elif name == "get_master_synthesis":
                dt = parse_dt_helper(args.get("datetime_str"))
                q = args.get("question", "")
                g = args.get("gender", 1)
                res = run_master_synthesis(dt, question=q, gender=g)
                
            elif name == "calculate_bat_quai_me_tung_bo":
                dt = parse_dt_helper(args.get("datetime_str"))
                traj = args.get("trajectory_type", "bat_quai_me_tung")
                sp = args.get("start_palace", None)
                intent = args.get("target_intent", "Tự vệ chiến lược & Dưỡng sinh khí cơ")
                res = calculate_bat_quai_me_tung_bo(dt, trajectory_type=traj, start_palace=sp, target_intent=intent)
                
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Tool '{name}' not found"}
                }
                
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, ensure_ascii=False, indent=2, default=str)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Tool execution failed: {str(e)}"}
            }
            
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method '{method}' not found"}
    }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_rpc_request(req)
            sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res, ensure_ascii=False) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
