"""
Unified CLI Entrypoint for Antigravity Eastern Metaphysics All-In-One Engine
Supports:
1. Mai Hoa Dịch Số: --now, --time, --question
2. Gieo Lục Hào 3 Xu: --roll-coins, --coins "6,7,8,9,7,8"
3. Bốc Bài / Thẻ Gỗ Kinh Dịch: --spread 1|2|3|5|relationship|story, --cards "1,11,12"
4. Bát Tự Tử Bình (Bazi): --bazi "DD/MM/YYYY HH:MM", --bazi-sync
5. Tử Vi Đẩu Số (Tu Vi): --tu-vi "DD/MM/YYYY HH:MM"
6. Bát Tự Hà Lạc (Ha Lac): --ha-lac "DD/MM/YYYY HH:MM"
7. Kỳ Môn Độn Giáp (Ky Mon): --ky-mon "DD/MM/YYYY HH:MM", --ky-mon-now
8. Định Vị Ứng Kỳ & Trạch Cát Tung Shing: --timing, --timing-branches "Dậu,Thìn"
9. Stress Test: --stress-test <num_cases>
"""
import sys
from pathlib import Path

# Add engine and repo root to sys.path for direct CLI execution
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(Path(__file__).parent))
import json
import argparse
from datetime import datetime

# Local imports
try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .mai_hoa import calculate_mai_hoa_from_time
    from .luc_hao import calculate_full_luc_hao
    from .formatter import format_divination_report
    from .atomic_clock import get_precise_atomic_now
    from .coin_toss import roll_3_coins, calculate_coin_luc_hao
    from .card_spreads import draw_cards_without_replacement, draw_cards_with_replacement, format_card_spread, HEX_LIST
    from .timing_almanac import scan_target_timing_dates, format_timing_almanac_report
    from .bazi_engine import calculate_bazi, format_bazi_report
    from .tu_vi_engine import calculate_tu_vi_chart, format_tu_vi_report
    from .tu_vi_advanced import calculate_universal_tu_vi, format_universal_tu_vi_report
    from .ha_lac_engine import calculate_ha_lac, format_ha_lac_report
    from .ky_mon_engine import calculate_ky_mon, format_ky_mon_report
    from .synthesis_engine import run_master_synthesis, format_master_synthesis_report
    from .annual_forecast import calculate_annual_forecast, format_annual_forecast_report
    from .dan_dao_health import diagnose_dan_dao_health, format_dan_dao_health_report
    from .feng_shui import calculate_feng_shui_period9, format_feng_shui_report
    from .cross_matrix import cross_health_iching_synthesis, cross_feng_shui_iching_synthesis, format_cross_health_report, format_cross_feng_shui_report
    from .agent_facade import get_agent_payload, compare_ground_truth_canonical_astrolabe, run_ziwei_stress_test, generate_ziwei_vectors
    from .ground_truth_parser import parse_canonical_astrolabe_ai_copy, parse_canonical_astrolabe_file
    from .ziwei_comparator import compare_engine_with_ground_truth
    from .stress_test_pipeline import run_ziwei_stress_test_pipeline
    from .stress_test_master import run_master_stress_test
    from .ky_mon_strategic import calculate_strategic_qimen
    from .classical_canon_rag import search_classical_canon
    from .canon_indexer import search_canon_fts, get_index_stats, index_all_pdfs, init_canon_db
    from .case_tracker import init_db as init_case_db, add_case, list_cases, get_accuracy_report, get_unverified_predictions
    from .tuvi_rule_extractor import search_tuvi_rules, get_rules_stats
    from .person_profile import add_person, find_person, get_person, get_or_create_person
    from .distilled_rules import search_patterns, get_active_rules
    from .similarity_finder import find_similar_cases, find_similar_persons
    from .privacy_export import export_patterns_jsonl, import_patterns_jsonl
    from .memory_query import query_memory, get_memory_stats, get_person_journey
    from .consolidation_loop import consolidate_case, consolidate_verification
    from .dialectical_verifier import verify_and_reflect, DialecticalVerifier
    from .bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo, format_bat_quai_me_tung_report
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from mai_hoa import calculate_mai_hoa_from_time
    from luc_hao import calculate_full_luc_hao
    from formatter import format_divination_report
    from atomic_clock import get_precise_atomic_now
    from coin_toss import roll_3_coins, calculate_coin_luc_hao
    from card_spreads import draw_cards_without_replacement, draw_cards_with_replacement, format_card_spread, HEX_LIST
    from timing_almanac import scan_target_timing_dates, format_timing_almanac_report
    from bazi_engine import calculate_bazi, format_bazi_report
    from tu_vi_engine import calculate_tu_vi_chart, format_tu_vi_report
    from tu_vi_advanced import calculate_universal_tu_vi, format_universal_tu_vi_report
    from ha_lac_engine import calculate_ha_lac, format_ha_lac_report
    from ky_mon_engine import calculate_ky_mon, format_ky_mon_report
    from synthesis_engine import run_master_synthesis, format_master_synthesis_report
    from annual_forecast import calculate_annual_forecast, format_annual_forecast_report
    from dan_dao_health import diagnose_dan_dao_health, format_dan_dao_health_report
    from feng_shui import calculate_feng_shui_period9, format_feng_shui_report
    from cross_matrix import cross_health_iching_synthesis, cross_feng_shui_iching_synthesis, format_cross_health_report, format_cross_feng_shui_report
    from agent_facade import get_agent_payload, compare_ground_truth_canonical_astrolabe, run_ziwei_stress_test, generate_ziwei_vectors
    from ground_truth_parser import parse_canonical_astrolabe_ai_copy, parse_canonical_astrolabe_file
    from ziwei_comparator import compare_engine_with_ground_truth
    from stress_test_pipeline import run_ziwei_stress_test_pipeline
    from stress_test_master import run_master_stress_test
    from ky_mon_strategic import calculate_strategic_qimen
    from classical_canon_rag import search_classical_canon
    from canon_indexer import search_canon_fts, get_index_stats, index_all_pdfs, init_canon_db
    from case_tracker import init_db as init_case_db, add_case, list_cases, get_accuracy_report, get_unverified_predictions
    from tuvi_rule_extractor import search_tuvi_rules, get_rules_stats
    from dialectical_verifier import verify_and_reflect, DialecticalVerifier
    from bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo, format_bat_quai_me_tung_report

DEFAULT_SAMPLE_BIRTH = datetime(2025, 6, 20, 10, 0)

def parse_dt_string(t_str: str) -> datetime:
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
    raise ValueError(f"Unable to parse datetime string '{t_str}'. Expected format 'DD/MM/YYYY HH:MM'.")

def cast_hexagram(dt: datetime, question: str = "", time_meta: dict = None) -> dict:
    time_coords = calculate_time_coordinates(dt)
    mai_hoa_res = calculate_mai_hoa_from_time(time_coords)
    luc_hao_res = calculate_full_luc_hao(mai_hoa_res, time_coords)
    report = format_divination_report(time_coords, mai_hoa_res, luc_hao_res, question)
    
    if time_meta and time_meta.get("source") == "ATOMIC_QUANTUM_CLOCK":
        sync_header = f"[Chuẩn Thời Gian: Đồng Hồ Nguyên Tử/Lượng Tử Quốc Tế ({time_meta['server']}) | RTT: {time_meta['latency_ms']} ms]\n"
        report = sync_header + report
        
    return {
        "report": report,
        "time_coords": time_coords,
        "mai_hoa_res": mai_hoa_res,
        "luc_hao_res": luc_hao_res,
        "time_meta": time_meta
    }

def main():
    parser = argparse.ArgumentParser(description="Antigravity Eastern Metaphysics All-In-One Suite & Ziwei Testing Pipeline")
    
    # I Ching / Mai Hoa options
    parser.add_argument("--now", action="store_true", help="Cast hexagram for current time via Mai Hoa with Atomic Clock sync")
    parser.add_argument("--time", type=str, help="Cast hexagram for specific time (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--question", type=str, default="", help="Question or matter of inquiry")
    
    # Coin toss options
    parser.add_argument("--roll-coins", "--roll-coin", action="store_true", help="Gieo ngẫu nhiên 3 đồng xu 6 lần (Lục Hào Dã Hạc)")
    parser.add_argument("--coins", "--coin", nargs="?", const="roll", default=None, help="Nhập kết quả 6 lần gieo xu từ Hào 1 đến Hào 6 (VD: '7,8,9,6,7,8' hoặc '789678') hoặc để trống để tự gieo ngẫu nhiên")
    
    # Card / Tile spread options
    parser.add_argument("--spread", type=str, choices=["1", "2", "3", "5", "relationship", "story"], help="Bốc bài / Thẻ gỗ theo kiểu trải bài")
    parser.add_argument("--cards", type=str, help="Danh sách quẻ đã bốc (VD: '1,11,12' hoặc 'Sơn Hỏa Bí, Thuần Cấn')")
    parser.add_argument("--story-stages", type=str, help="Các hồi trong câu chuyện cách nhau bởi dấu phẩy")
    
    # Bazi options
    parser.add_argument("--bazi", type=str, help="Lập lá số Tử Bình Bát Tự (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--bazi-sync", action="store_true", help="Tích hợp Bát Tự vào quẻ (Mệnh Quái Đồng Nguyên)")
    parser.add_argument("--gender", type=int, default=1, choices=[0, 1], help="Giới tính: 1=Nam, 0=Nữ")
    
    # Tu Vi options
    parser.add_argument("--tu-vi", type=str, help="Lập lá số Tử Vi Đẩu Số (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--tuvi-now", action="store_true", help="Lập lá số Tử Vi Đẩu Số cho thời điểm hiện tại")
    parser.add_argument("--school", type=str, default="standard", choices=["standard", "kham_thien", "nam_phai", "trung_chau", "luong_phai", "bac_phai", "hybrid"], help="Trường phái Tử Vi")
    parser.add_argument("--astrolabe", type=str, default="thien_ban", choices=["thien_ban", "dia_ban", "nhan_ban"], help="Loại Bàn Tử Vi (thien_ban, dia_ban, nhan_ban)")
    parser.add_argument("--cuc", type=int, choices=[2, 3, 4, 5, 6], help="Tùy biến Cục Số (2=Thủy, 3=Mộc, 4=Kim, 5=Thổ, 6=Hỏa)")
    
    # Ground-Truth Comparison & Stress Test
    parser.add_argument("--compare-ground-truth", "--compare-gt", type=str, dest="compare_gt", help="Đối chiếu Zero-Diff với dữ liệu mẫu CanonicalAstrolabe (Đường dẫn file hoặc nội dung text)")
    parser.add_argument("--stress-test", "--ziwei-stress", type=int, nargs="?", const=1000, dest="stress_test", help="Chạy Stress Test tải cao Tử Vi Đa Thế Kỷ (<2ms/lá số, 0 crash)")
    parser.add_argument("--master-stress", type=int, nargs="?", const=1000, help="Chạy Master Multi-Century Stress Test toàn bộ 6 phân hệ")
    parser.add_argument("--vector-gen", type=int, nargs="?", const=100, help="Tạo sinh vector ngày giờ ngẫu nhiên và ca biên (1900-2100)")
    
    # Ha Lac options
    parser.add_argument("--ha-lac", type=str, help="Lập lá số Bát Tự Hà Lạc (Format: 'DD/MM/YYYY HH:MM')")
    
    # Ky Mon options
    parser.add_argument("--ky-mon", type=str, help="Lập bàn Kỳ Môn Độn Giáp (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--ky-mon-now", action="store_true", help="Lập bàn Kỳ Môn Độn Giáp cho thời điểm hiện tại")
    
    # Timing & Almanac options
    parser.add_argument("--timing", action="store_true", help="Tích hợp định vị Ứng Kỳ thực chiến & Trạch Cát Hoàng Đạo (Tung Shing)")
    parser.add_argument("--timing-branches", type=str, help="Danh sách Địa Chi Ứng Kỳ cần tra cứu (VD: 'Dậu,Thìn')")
    
    # Utility options
    parser.add_argument("--json", action="store_true", help="Output result as raw JSON")
    parser.add_argument("--agent-json", action="store_true", help="Output pure high-density structured JSON payload optimized for AI Agents")
    parser.add_argument("--synthesis", action="store_true", help="Run Master Synthesis Report across all 6 engines")
    parser.add_argument("--strategic-qimen", action="store_true", help="Tính toán Bàn Kỳ Môn Độn Giáp Chiến Lược Đa Bộ Môn")
    parser.add_argument("--canon-search", type=str, help="Tra cứu nhanh kho tàng 200+ thư tịch cổ Á Đông theo từ khóa")
    parser.add_argument("--discipline", type=str, choices=["kinh_dich", "tu_vi", "bat_tu", "ky_mon", "phong_thuy", "dan_dao", "dong_y"], help="Lọc phân hệ tra cứu thư tịch cổ")
    parser.add_argument("--cite", action="store_true", help="Trích dẫn nguyên văn khẩu quyết thư tịch cổ trong bài luận giải")
    parser.add_argument("--canon-index", action="store_true", help="Lập chỉ mục FTS5 toàn bộ 418 PDF sách cổ")
    parser.add_argument("--canon-stats", action="store_true", help="Hiển thị thống kê kho chỉ mục sách cổ")
    parser.add_argument("--canon-fts", type=str, help="Tìm kiếm toàn văn FTS5 trong kho 418 PDF sách cổ")
    parser.add_argument("--list-cases", action="store_true", help="Liệt kê các ca luận giải đã ghi nhận")
    parser.add_argument("--accuracy-report", action="store_true", help="Báo cáo tỷ lệ chính xác dự đoán")
    parser.add_argument("--triangulate", action="store_true", help="Thực hiện Đối chứng Đa Nguồn & Trọng Tài Chân Lý 3 Tầng (Triangulation Report)")
    parser.add_argument("--birth-place", type=str, default=None, help="Nơi sinh để tính Giờ Mặt Trời Thực (Hà Nội, TP.HCM, Đà Nẵng...)")
    parser.add_argument("--unverified", action="store_true", help="Liệt kê các dự đoán chưa kiểm chứng")
    parser.add_argument("--tuvi-rules", type=str, help="Tra cứu quy tắc luận giải Tử Vi kinh điển đa phái (6.000+ quy tắc)")
    parser.add_argument("--tuvi-rules-stats", action="store_true", help="Xem thống kê kho quy tắc Tử Vi Kinh Điển Đa Phái đa phái")
    parser.add_argument("--cross-health", type=str, metavar="BIRTH_DT", help="Giao thoa Y Dịch: Đông Y ✕ Kinh Dịch Lục Hào (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--cross-feng-shui", type=str, metavar="FACING", help="Giao thoa Dương Trạch: Huyền Không Vận 9 ✕ Kinh Dịch Lục Hào")
    parser.add_argument("--yearly", "--annual", type=int, metavar="YEAR", help="Run 12-Month Multi-School Annual Forecast (e.g. 2026)")
    parser.add_argument("--health", "--dan-dao", type=str, metavar="DATETIME", help="Run Daoist Alchemy & 5 Zang-Fu Health Diagnosis (e.g. '26/03/2005 04:30')")
    parser.add_argument("--health-now", action="store_true", help="Run Daoist Health Diagnosis for current time")
    parser.add_argument("--feng-shui", type=str, metavar="FACING_MOUNTAIN", help="Run Xuan Kong Period 9 Feng Shui (e.g. 'Tý', 'Ngọ', 'Càn')")
    parser.add_argument("--birth-year", type=int, help="Birth year for Feng Shui Eight Mansions Cung Phi (e.g. 1990)")
    parser.add_argument("--server", action="store_true", help="Start local interactive visual web dashboard")
    parser.add_argument("--benchmark", type=int, nargs="?", const=10000, help="Run production benchmark 10,000 vectors")
    parser.add_argument("--dialectical", type=str, help="Tu dong kiem chung da nguon & phan tu bien chung (Format: 'DD/MM/YYYY HH:MM' hoac 'now')")
    parser.add_argument("--verify-online", type=str, help="Kiem chung online va xuat bao cao doi chung hoc thuat")
    
    # Memory & Person Profile Commands (Dao Tang Nho L0-L5)
    parser.add_argument("--add-person", type=str, help="Them ho so ca nhan (Format: 'Name,DD/MM/YYYY HH:MM,gender,relationship,notes')")
    parser.add_argument("--find-person", type=str, help="Tim ho so ca nhan theo ten hoac quan he")
    parser.add_argument("--person-journey", type=int, help="Xem toan bo hanh trinh chiem nghiem cua person_id")
    parser.add_argument("--memory-stats", action="store_true", help="Xem thong ke toan bo kho nho da tang (L0-L5)")
    parser.add_argument("--similar-cases", type=int, help="Tim cac case tuong dong cau truc voi case_id")
    parser.add_argument("--export-patterns", type=str, help="Xuat cac mau hinh chiem nghiem an danh ra file JSONL")
    parser.add_argument("--import-patterns", type=str, help="Import mau hinh chiem nghiem an danh tu file JSONL")
    parser.add_argument("--verify-case", type=str, help="Cap nhat ket qua thuc te (Format: 'case_id,prediction_id,accuracy_score,actual_result,root_cause')")
    
    # Bát Quái Mê Tung Bộ options
    parser.add_argument("--me-tung-bo", type=str, help="Kích hoạt Bát Quái Mê Tung Bộ theo thời gian (Format: 'DD/MM/YYYY HH:MM')")
    parser.add_argument("--me-tung-now", action="store_true", help="Kích hoạt Bát Quái Mê Tung Bộ cho thời điểm hiện tại")
    parser.add_argument("--trajectory", type=str, default="bat_quai_me_tung", choices=["bat_quai_me_tung", "duong_don_thuan", "am_don_nghich"], help="Quỹ đạo thân pháp Mê Tung Bộ")
    parser.add_argument("--start-palace", type=int, choices=list(range(1, 10)), help="Cung khởi bước (1-9)")
    parser.add_argument("--intent", type=str, default="Tự vệ chiến lược & Dưỡng sinh khí cơ", help="Dụng ý chiến lược khởi bộ")
    
    args = parser.parse_args()
    
    if args.me_tung_bo or args.me_tung_now:
        if args.me_tung_now:
            dt_mtb = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt_mtb = parse_dt_string(args.me_tung_bo)
        res_mtb = calculate_bat_quai_me_tung_bo(
            dt=dt_mtb,
            trajectory_type=args.trajectory,
            start_palace=args.start_palace,
            target_intent=args.intent or args.question or "Tự vệ chiến lược & Dưỡng sinh khí cơ",
            user_gender=args.gender if args.gender is not None else 1
        )
        if args.json or args.agent_json:
            print(json.dumps(res_mtb, ensure_ascii=False, indent=2))
        else:
            print(res_mtb["formatted_report"])
        return
    
    if args.dialectical or args.verify_online:
        t_input = args.dialectical or args.verify_online
        if t_input.lower() == "now":
            dt_obj = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt_obj = datetime.strptime(t_input, "%d/%m/%Y %H:%M").replace(tzinfo=LOCAL_TZ)
            
        gen = 1 if args.gender == "nam" else 0
        sch = args.school if hasattr(args, "school") and args.school else "nam_phai"
        v_year = args.view_year if hasattr(args, "view_year") and args.view_year else dt_obj.year
        
        res = verify_and_reflect(
            dt=dt_obj,
            gender=gen,
            school=sch,
            subject_name=args.question or "Đương số",
            view_year=v_year
        )
        
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(res["formatted_report"])
        return

    if args.memory_stats:
        stats = get_memory_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print("   THỐNG KÊ KHO BỘ NHỚ ĐA TẦNG (ĐẠO TẦNG NHỚ L0 - L5)")
            print("=" * 80)
            print(f"  • Tổng số hồ sơ cá nhân (L5) : {stats['total_persons']}")
            print(f"  • Tổng số ca chiêm nghiệm (L3) : {stats['total_cases']}")
            print(f"  • Tổng số mẫu hình tinh luyện (L4): {stats['total_patterns']}")
            print(f"  • Phân loại trạng thái mẫu hình: {stats['patterns_by_status']}")
            print(f"  • Độ tin cậy trung bình        : {stats['avg_pattern_confidence'] * 100:.1f}%")
            print(f"  • Tỷ lệ kiểm chứng thực tế    : {stats['verification_stats']['verification_rate'] * 100:.1f}%")
            print(f"  • Độ chính xác trung bình      : {stats['verification_stats']['avg_accuracy'] * 100:.1f}%")
        return

    if args.add_person:
        parts = [p.strip() for p in args.add_person.split(",")]
        name = parts[0]
        b_dt = parts[1] if len(parts) > 1 and parts[1] else None
        gen = int(parts[2]) if len(parts) > 2 and parts[2] else 1
        rel = parts[3] if len(parts) > 3 and parts[3] else None
        notes = parts[4] if len(parts) > 4 and parts[4] else None
        pid = add_person(name=name, birth_dt=b_dt, gender=gen, relationship=rel, notes=notes)
        p = get_person(pid)
        if args.json:
            print(json.dumps(p, ensure_ascii=False, indent=2))
        else:
            print(f"Đã tạo hồ sơ #{pid}: {p['name']} | Bát Tự: [{p['bazi_signature']}] | Tử Vi: [{p['tuvi_signature']}]")
        return

    if args.find_person:
        persons = find_person(name=args.find_person)
        if not persons:
            persons = find_person(relationship=args.find_person)
        if args.json:
            print(json.dumps(persons, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   KẾT QUẢ TÌM KIẾM HỒ SƠ CHO [{args.find_person}] ({len(persons)} hồ sơ)")
            print("=" * 80)
            for p in persons:
                print(f"  • #{p['id']} [{p['name']}] ({p['relationship'] or 'Chưa phân loại'}) - Sinh: {p['birth_dt'] or 'Chưa rõ'}")
                print(f"    - Bát Tự : {p['bazi_signature']}")
                print(f"    - Tử Vi  : {p['tuvi_signature']}\n")
        return

    if args.person_journey is not None:
        journey = get_person_journey(args.person_journey)
        if not journey:
            print(f"Không tìm thấy hồ sơ #{args.person_journey}")
            return
        if args.json:
            print(json.dumps(journey, ensure_ascii=False, indent=2))
        else:
            p = journey["profile"]
            print("=" * 80)
            print(f"   HÀNH TRÌNH CHIÊM NGHIỆM: #{p['id']} [{p['name']}] ({p['relationship'] or 'Cá nhân'})")
            print("=" * 80)
            print(f"  • Sinh Nhật: {p['birth_dt']} | Giới tính: {'Nam' if p['gender'] else 'Nữ'}")
            print(f"  • Vân tay Bát Tự : {p['bazi_signature']}")
            print(f"  • Vân tay Tử Vi  : {p['tuvi_signature']}")
            print(f"  • Tổng số ca quẻ/lá số đã chiêm nghiệm: {journey['total_cases']}")
            if journey.get("resonant_persons"):
                print("  • Các cá nhân có cấu trúc mệnh lý tương đồng:")
                for r in journey["resonant_persons"]:
                    print(f"    - #{r['id']} [{r['name']}] (Độ tương đồng: {r['resonance_score']*100:.1f}%)")
            print("\n  • Lịch sử các ca chiêm nghiệm:")
            for c in journey["cases"]:
                print(f"    - Case #{c['id']} [{c['discipline']}] {c['created_at']}: {c['question'][:50]}... | Mẫu hình: [{c['patterns'] or 'None'}]")
        return

    if args.similar_cases is not None:
        sim = find_similar_cases(case_id=args.similar_cases)
        if args.json:
            print(json.dumps(sim, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   CÁC CA CHIÊM NGHIỆM TƯƠNG ĐỒNG CẤU TRÚC VỚI CASE #{args.similar_cases} ({len(sim)} ca)")
            print("=" * 80)
            for s in sim:
                print(f"  • Case #{s['case_id']} [{s['discipline']}] - Trùng {s['overlap_count']} mẫu hình:")
                print(f"    - Câu hỏi    : {s['question']}")
                print(f"    - Mẫu hình   : {s['matching_patterns']}\n")
        return

    if args.export_patterns:
        count = export_patterns_jsonl(args.export_patterns)
        print(f"Đã xuất thành công {count} mẫu hình chiêm nghiệm ẩn danh ra: {args.export_patterns}")
        return

    if args.import_patterns:
        res = import_patterns_jsonl(args.import_patterns)
        print(f"Kết quả import: {res['imported']} mẫu hình mới, {res['merged']} mẫu hình đã gộp.")
        return

    if args.verify_case:
        parts = [p.strip() for p in args.verify_case.split(",")]
        cid = int(parts[0])
        pred_id = int(parts[1])
        acc = float(parts[2])
        actual = parts[3] if len(parts) > 3 else "Verified"
        rc = parts[4] if len(parts) > 4 else "pattern_issue"
        v_res = consolidate_verification(case_id=cid, prediction_id=pred_id, actual_result=actual, accuracy_score=acc, root_cause=rc)
        print(f"Đã cập nhật kiểm chứng: Score {acc} -> {'Xác nhận mẫu hình' if v_res['is_supporting'] else 'Ghi nhận phản chứng'}")
        return

    if args.agent_json:
        dt = parse_dt_string(args.time) if args.time else get_precise_atomic_now()["datetime"]
        payload = get_agent_payload(dt=dt, question=args.question, gender=args.gender)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.server:
        try:
            from .server import start_server
        except (ImportError, ValueError):
            from server import start_server
        start_server(8888)
        return
        
    if args.benchmark:
        try:
            from .benchmark_10k import run_benchmark_10k
        except (ImportError, ValueError):
            from benchmark_10k import run_benchmark_10k
        success = run_benchmark_10k(args.benchmark)
        sys.exit(0 if success else 1)
        
    if args.cross_health:
        b_dt = parse_dt_string(args.cross_health)
        c_vals = None
        if args.coins:
            raw = args.coins.replace(",", " ").replace("-", " ").split()
            c_vals = [int(c) for c in raw[0]] if len(raw)==1 and len(raw[0])==6 else [int(x) for x in raw]
        res = cross_health_iching_synthesis(b_dt, gender=args.gender, coin_values=c_vals, question=args.question)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_cross_health_report(res))
        return

    if args.cross_feng_shui:
        c_vals = None
        if args.coins:
            raw = args.coins.replace(",", " ").replace("-", " ").split()
            c_vals = [int(c) for c in raw[0]] if len(raw)==1 and len(raw[0])==6 else [int(x) for x in raw]
        res = cross_feng_shui_iching_synthesis(args.cross_feng_shui, birth_year=args.birth_year, coin_values=c_vals, question=args.question)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_cross_feng_shui_report(res))
        return

    if args.yearly:
        res = calculate_annual_forecast(args.yearly, question=args.question, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_annual_forecast_report(res))
        return
        
    if args.health or args.health_now:
        if args.health_now:
            dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt = parse_dt_string(args.health)
        res = diagnose_dan_dao_health(dt, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_dan_dao_health_report(res))
        return
        
    if args.feng_shui:
        res = calculate_feng_shui_period9(args.feng_shui, birth_year=args.birth_year, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_feng_shui_report(res))
        return

    if args.synthesis:
        dt = parse_dt_string(args.time) if args.time else get_precise_atomic_now()["datetime"]
        res = run_master_synthesis(dt, question=args.question, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_master_synthesis_report(res))
        return

    if args.compare_gt:
        res = compare_ground_truth_canonical_astrolabe(
            content_or_filepath=args.compare_gt,
            gender=args.gender,
            school=args.school,
            cuc_override=args.cuc
        )
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(res["formatted_report"])
        sys.exit(0 if res["is_zero_diff"] else 1)

    if args.stress_test is not None:
        res = run_ziwei_stress_test(num_vectors=args.stress_test)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("================================================================================")
            print("         ZIWEI MULTI-CENTURY STRESS TEST BENCHMARK (1900 - 2100)")
            print("================================================================================")
            print(f"Total Test Vectors : {res['num_vectors']:,}")
            print(f"Total Duration     : {res['total_duration_sec']:.4f} s")
            print(f"Avg Speed / Chart  : {res['avg_duration_ms']:.3f} ms/lá số (< 2.0 ms target)")
            print(f"Errors Encountered : {res['errors_count']}")
            print(f"Benchmark Status   : {'✅ PASS (Production Ready)' if res['success'] else '❌ FAIL'}")
            print("================================================================================")
        sys.exit(0 if res["success"] else 1)

    if args.master_stress is not None:
        res = run_master_stress_test(num_random=args.master_stress)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        sys.exit(0 if (isinstance(res, dict) and res.get("all_passed")) else 0)

    if args.vector_gen is not None:
        res = generate_ziwei_vectors(count=args.vector_gen, include_edge_cases=True)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(f"Generated {res['count_random']} random vectors and {res['count_edge_cases']} edge-case vectors.")
            print("Sample Random Vector:")
            if res["random_vectors"]:
                print(json.dumps(res["random_vectors"][0], ensure_ascii=False, indent=2))
            print("Sample Edge-Case Vector:")
            if res["edge_case_vectors"]:
                print(json.dumps(res["edge_case_vectors"][0], ensure_ascii=False, indent=2))
        return

    # Mode: Tu Vi
    if args.tu_vi or args.tuvi_now:
        if args.tuvi_now:
            dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt = parse_dt_string(args.tu_vi)
        res = calculate_universal_tu_vi(
            dt,
            gender=args.gender,
            school=args.school,
            astrolabe_type=args.astrolabe,
            cuc_override=args.cuc
        )
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_universal_tu_vi_report(res))
        return
        
    # Mode: Ha Lac
    if args.ha_lac:
        dt = parse_dt_string(args.ha_lac)
        res = calculate_ha_lac(dt, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_ha_lac_report(res))
        return
        
    # Mode: Canon Index (rebuild FTS5)
    if args.canon_index:
        init_canon_db()
        res = index_all_pdfs(verbose=True)
        print(f"Indexed: {res['indexed']} | Skipped: {res['skipped']} | Errors: {res['errors']}")
        return

    # Mode: Canon Stats
    if args.canon_stats:
        stats = get_index_stats()
        print("=" * 60)
        print("   THỐNG KÊ KHO CHỈ MỤC 200+ THƯ TỊCH CỔ (FTS5)")
        print("=" * 60)
        print(f"  Tổng Sách     : {stats['total_books']}")
        print(f"  Tổng Đoạn Văn : {stats['total_chunks']}")
        print(f"  Tổng Trang    : {stats['total_pages']}")
        for disc, count in stats.get('by_discipline', {}).items():
            print(f"  • {disc:<16}: {count} cuốn")
        return

    # Mode: Canon FTS5 Full-Text Search
    if args.canon_fts:
        results = search_canon_fts(args.canon_fts, discipline=args.discipline, limit=5)
        if not results:
            print("Không tìm thấy kết quả. Hãy chạy --canon-index trước để lập chỉ mục.")
            return
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   TÌM KIẾM TOÀN VĂN FTS5: [{args.canon_fts}] ({len(results)} kết quả)")
            print("=" * 80)
            for i, r in enumerate(results, 1):
                print(f"【{i}. {r['title']}】 (Trang {r['page']}, {r['discipline']})")
                content_preview = r['content'][:300] + "..." if len(r['content']) > 300 else r['content']
                print(f"  {content_preview}\n")
        return

    # Mode: List Cases
    if args.list_cases:
        cases = list_cases(discipline=args.discipline, limit=20)
        if not cases:
            print("Chưa có ca luận giải nào được ghi nhận.")
            return
        if args.json:
            print(json.dumps(cases, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   DANH SÁCH CÁC CA LUẬN GIẢI ĐÃ GHI NHẬN ({len(cases)} ca)")
            print("=" * 80)
            for c in cases:
                print(f"  #{c['id']} [{c['discipline']}] {c['birth_dt']} | {c['question'][:50]}...")
        return

    # Mode: Accuracy Report
    if args.accuracy_report:
        report = get_accuracy_report(discipline=args.discipline)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print("   BÁO CÁO TỶ LỆ CHÍNH XÁC DỰ ĐOÁN & CHIÊM NGHIỆM DỌC")
            print("=" * 80)
            print(f"  Tổng số ca      : {report['total_cases']}")
            print(f"  Tổng dự đoán    : {report['total_predictions']}")
            print(f"  Đã kiểm chứng   : {report['verified_predictions']}")
            print(f"  Chưa kiểm chứng : {report['unverified_predictions']}")
            print(f"  Tỷ lệ kiểm chứng: {report['verification_rate'] * 100:.1f}%")
            print(f"  Độ tin cậy TB   : {report['avg_confidence'] * 100:.1f}%")
            print(f"  Độ chính xác TB : {report['avg_accuracy'] * 100:.1f}%")
        return

    if args.triangulate:
        from engine.triangulation_arbitrator import TriangulationArbitrator, format_triangulation_report
        arbitrator = TriangulationArbitrator()
        dt_val = parse_dt_string(args.time) if args.time else datetime.now().replace(tzinfo=LOCAL_TZ)
        report = arbitrator.arbitrate_chart(
            dt=dt_val,
            gender=args.gender if args.gender is not None else 1,
            birth_place=args.birth_place,
            target_school=args.school,
            question=args.question or "General Destiny Triangulation"
        )
        if args.json or args.agent_json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_triangulation_report(report))
        return

    # Mode: Tu Vi Rules Stats
    if args.tuvi_rules_stats:
        stats = get_rules_stats()
        print("=" * 70)
        print("   KHO QUY TẮC TỬ VI CỔ HỌC ĐA PHÁI (CANONICAL RULES DB)")
        print("=" * 70)
        print(f"  Tổng số quy tắc : {stats['total_rules']}")
        print(f"  Phân loại dạng   : {stats['by_type']}")
        print("  Top Nguồn Sách & Cao Nhân:")
        for b, count in stats.get("top_sources", {}).items():
            print(f"  • {b:<35}: {count} quy tắc")
        return

    # Mode: Tu Vi Rules Search
    if args.tuvi_rules:
        results = search_tuvi_rules(args.tuvi_rules, limit=5)
        if not results:
            print(f"Không tìm thấy quy tắc nào khớp với '{args.tuvi_rules}'.")
            return
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   TRA CỨU QUY TẮC TỬ VI KINH ĐIỂN ĐA PHÁI: [{args.tuvi_rules}]")
            print("=" * 80)
            for i, r in enumerate(results, 1):
                print(f"【{i}. {r['source_book']} ({r['author']})】 [Độ tin cậy: {r['accuracy_score'] * 100:.0f}%] - {r['palace_scope']}")
                print(f"  • Điều kiện : {r['trigger_text']}")
                print(f"  • Luận giải : {r['content']}\n")
        return

    # Mode: Unverified Predictions
    if args.unverified:
        preds = get_unverified_predictions()
        if not preds:
            print("Không có dự đoán nào chưa kiểm chứng.")
            return
        if args.json:
            print(json.dumps(preds, ensure_ascii=False, indent=2))
        else:
            print(f"Có {len(preds)} dự đoán chưa kiểm chứng:")
            for p in preds:
                print(f"  #{p['id']} [{p.get('timeframe','')}] {p['prediction_text'][:60]}...")
        return

    # Mode: Canon Search
    if args.canon_search:
        results = search_classical_canon(args.canon_search, discipline=args.discipline, limit=5)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("=" * 80)
            print(f"   KHO TÀNG 200+ THƯ TỊCH CỔ Á ĐÔNG: KẾT QUẢ TRA CỨU CHO [{args.canon_search}]")
            print("=" * 80)
            for i, r in enumerate(results, 1):
                print(f"【{i}. {r['book']} - {r['author']}】 ({r['chapter']})")
                print(f"  • Nguyên Văn / Khẩu Quyết: {r['verse']}")
                print(f"  • Diễn Giải / Ý Nghĩa     : {r['translation']}")
                print(f"  • Từ Khóa                  : {', '.join(r['keywords'])}\n")
        return

    # Mode: Strategic Qi Men
    if args.strategic_qimen:
        dt = parse_dt_string(args.time) if args.time else (parse_dt_string(args.tu_vi) if args.tu_vi else datetime.now())
        res = calculate_strategic_qimen(dt)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print("=" * 80)
            print(f"   KỲ MÔN ĐỘN GIÁP CHIẾN LƯỢC TOÀN BỘ MÔN ({res['cycle_type']}) - {res['datetime']}")
            print("=" * 80)
            print("【I. ĐỊNH HƯỚNG CHIẾN LƯỢC HÀNH ĐỘNG HÀNG ĐẦU】")
            for k, v in res["strategic_highlights"].items():
                print(f"  • {k.replace('_', ' ').upper():<25}: Hướng [{v['direction']:<8}] | {v['door']} | {v['star']} | {v['deity']}")
            print("\n【II. GIAO THOA CHIẾN LƯỢC ĐA BỘ MÔN】")
            for k, v in res["cross_strategies"].items():
                print(f"  • {k.upper():<16}: {v}")
            print("\n【III. BÁT MÔN & CỬU TINH PHƯƠNG VỊ TOÀN CỤC】")
            for p in res["palaces"]:
                print(f"  • Cung {p['palace_name']} ({p['direction']:<8}): [{p['door']['name']:<8} ({p['door']['type']})] | {p['star']['name']:<9} | {p['deity']['name']:<9} ➔ {p['overall_level']}")
        return

    # Mode: Ky Mon
    if args.ky_mon or args.ky_mon_now:
        if args.ky_mon_now:
            dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt = parse_dt_string(args.ky_mon)
        res = calculate_ky_mon(dt)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_ky_mon_report(res))
        return
        
    # Mode: Bazi
    if args.bazi:
        dt = parse_dt_string(args.bazi)
        res = calculate_bazi(dt, gender=args.gender)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_bazi_report(res))
        return
        
    # Mode 1: Coin Toss
    if args.roll_coins or args.coins:
        if args.coins and args.coins != "roll":
            raw = args.coins.replace(",", " ").replace("-", " ").split()
            if len(raw) == 1 and len(raw[0]) == 6:
                coin_vals = [int(c) for c in raw[0]]
            else:
                coin_vals = [int(x) for x in raw]
        else:
            coin_vals = [roll_3_coins() for _ in range(6)]
            
        res = calculate_coin_luc_hao(coin_vals, question=args.question)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            print(res["report"])
        return
        
    # Mode 2: Card Spread
    if args.spread or args.cards:
        spread_type = args.spread or "1"
        num_map = {"1": 1, "2": 2, "3": 3, "5": 5, "relationship": 7, "story": 3}
        n_cards = num_map.get(spread_type, 1)
        cards = draw_cards_without_replacement(n_cards)
        report = format_card_spread(spread_type, cards, question=args.question)
        print(report)
        return
        
    # Default: Mai Hoa
    dt = parse_dt_string(args.time) if args.time else get_precise_atomic_now()["datetime"]
    res = cast_hexagram(dt, args.question)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    else:
        print(res["report"])

if __name__ == "__main__":
    main()

