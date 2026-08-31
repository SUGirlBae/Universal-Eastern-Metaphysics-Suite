try:
    from .ky_mon_strategic import calculate_strategic_qimen
    from .classical_canon_rag import search_classical_canon, get_canonical_citation_for_reading
    from .tuvi_rule_extractor import search_tuvi_rules
    from .triangulation_arbitrator import TriangulationArbitrator, format_triangulation_report
except (ImportError, ValueError):
    from ky_mon_strategic import calculate_strategic_qimen
    from classical_canon_rag import search_classical_canon, get_canonical_citation_for_reading
    from tuvi_rule_extractor import search_tuvi_rules
    from triangulation_arbitrator import TriangulationArbitrator, format_triangulation_report

"""
Agent-First Metaphysics Facade
Provides ultra-high density, machine-readable structured JSON payloads
optimized specifically for AI Agent tool use, function calling, and LLM reasoning.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

try:
    from .lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from .mai_hoa import calculate_mai_hoa_from_time
    from .luc_hao import calculate_full_luc_hao
    from .bazi_engine import calculate_bazi
    from .tu_vi_engine import calculate_tu_vi_chart
    from .tu_vi_advanced import calculate_universal_tu_vi, format_universal_tu_vi_report
    from .ha_lac_engine import calculate_ha_lac
    from .ky_mon_engine import calculate_ky_mon
    from .timing_almanac import scan_target_timing_dates
    from .knowledge_graph import analyze_wuxing_interaction, analyze_branch_pair
    from .annual_forecast import calculate_annual_forecast
    from .dan_dao_health import diagnose_dan_dao_health
    from .feng_shui import calculate_feng_shui_period9
    from .bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo
    from .ground_truth_parser import parse_canonical_astrolabe_ai_copy, parse_canonical_astrolabe_file
    from .ziwei_comparator import compare_engine_with_ground_truth
    from .stress_test_pipeline import run_ziwei_stress_test_pipeline
except (ImportError, ValueError):
    from lunar_solar import calculate_time_coordinates, LOCAL_TZ
    from mai_hoa import calculate_mai_hoa_from_time
    from luc_hao import calculate_full_luc_hao
    from bazi_engine import calculate_bazi
    from tu_vi_engine import calculate_tu_vi_chart
    from tu_vi_advanced import calculate_universal_tu_vi, format_universal_tu_vi_report
    from ha_lac_engine import calculate_ha_lac
    from ky_mon_engine import calculate_ky_mon
    from timing_almanac import scan_target_timing_dates
    from knowledge_graph import analyze_wuxing_interaction, analyze_branch_pair
    from annual_forecast import calculate_annual_forecast
    from dan_dao_health import diagnose_dan_dao_health
    from feng_shui import calculate_feng_shui_period9
    from bat_quai_me_tung_bo import calculate_bat_quai_me_tung_bo
    from ground_truth_parser import parse_canonical_astrolabe_ai_copy, parse_canonical_astrolabe_file
    from ziwei_comparator import compare_engine_with_ground_truth
    from stress_test_pipeline import run_ziwei_stress_test_pipeline

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

def get_agent_payload(
    dt: Optional[datetime] = None,
    question: str = "",
    gender: int = 1,
    birth_place: Optional[str] = None,
    longitude: Optional[float] = None,
    systems: Optional[List[str]] = None,
    school: str = "hybrid",
    astrolabe_type: str = "thien_ban",
    cuc_override: Optional[int] = None,
    triangulate: bool = False
) -> Dict[str, Any]:
    """
    Returns a unified high-density context payload tailored for AI reasoning.
    Zero ASCII clutter, 100% structured data + reasoning scaffolding.
    Utilizes calculate_universal_tu_vi as the primary high-performance engine.
    """
    if dt is None:
        dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        
    if systems is None:
        systems = ["iching", "bazi", "tuvi", "halac", "kymon", "timing", "annual", "health", "fengshui"]
        
    payload: Dict[str, Any] = {
        "schema_version": "2.2.0-agent",
        "timestamp_iso": dt.isoformat(),
        "query_target": question or "General Destiny & Strategic Divination",
        "gender": "male" if gender == 1 else "female",
        "data": {}
    }
    
    # 1. Time Coordinates
    tc = calculate_time_coordinates(dt)
    payload["data"]["time_coords"] = {
        "solar_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "lunar_datetime": f"{tc['lunar_day']:02d}/{tc['lunar_month']:02d}/{tc['lunar_year']}",
        "pillars": {
            "year": tc["can_chi_year"],
            "month": tc["can_chi_month"],
            "day": tc["can_chi_day"],
            "hour": tc["can_chi_hour"]
        },
        "solar_term": tc["tiet_khi"]
    }
    
    # 2. I Ching & Luc Hao
    if "iching" in systems:
        mh = calculate_mai_hoa_from_time(tc)
        lh = calculate_full_luc_hao(mh, tc)
        payload["data"]["iching"] = {
            "main_hexagram": {
                "name": lh["hex_name"],
                "symbol": lh["hex_symbol"],
                "palace": lh["palace_name"],
                "element": lh["palace_elem"],
                "rank_name": lh.get("palace_rank_name", ""),
                "tags": lh.get("hex_tags", []),
                "lines": lh["lines"]
            },
            "moving_line": lh["moving_line"],
            "transformed_hexagram": {
                "name": lh["t_hex_name"],
                "tags": lh.get("t_hex_tags", [])
            },
            "tuan_khong": lh.get("empty_branches", [])
        }
        
    # 3. Bazi
    if "bazi" in systems:
        bz = calculate_bazi(dt, gender=gender)
        payload["data"]["bazi"] = {
            "day_master": bz["day_master"],
            "pillars": bz["pillars"],
            "current_dayun": bz["current_dayun"],
            "all_dayun": bz["dayun_list"]
        }
        
    # 4. Tu Vi (Universal Engine v3.0: 110+ stars, 12 Cung Phi Tinh, Tự Hóa/Hướng Tâm, Phương Viên Toàn Đồ, Khâm Thiên routes)
    if "tuvi" in systems:
        tv = calculate_universal_tu_vi(
            dt,
            gender=gender,
            school=school,
            astrolabe_type=astrolabe_type,
            cuc_override=cuc_override
        )
        # Match top canonical rules for this chart
        matched_rules = []
        try:
            for p in tv["palaces"]:
                if p["is_menh"] or p["is_than"]:
                    for s in p.get("main_stars", []):
                        found = search_tuvi_rules(s, limit=2)
                        for r in found:
                            if r not in matched_rules:
                                matched_rules.append(r)
        except Exception:
            pass

        payload["data"]["tuvi"] = {
            "schema_version": tv.get("schema_version", "3.1.0-universal-ziwei"),
            "school": tv.get("school", school),
            "astrolabe_type": tv.get("astrolabe_type", astrolabe_type),
            "cuc_name": tv["client_profile"]["cuc_name"],
            "cuc_num": tv["client_profile"]["cuc_num"],
            "menh_branch": tv["client_profile"]["menh_branch"],
            "than_branch": tv["client_profile"]["than_branch"],
            "client_profile": tv["client_profile"],
            "four_transformations": tv.get("flying_stars", {}).get("birth_year_si_hua", {}),
            "palaces": tv["palaces"],
            "flying_stars": tv.get("flying_stars", {}),
            "flying_intensity": tv.get("flying_intensity", {}),
            "matched_canonical_rules": matched_rules[:8],
            "transits": tv.get("transits", {}),
            "ha_lac_hexagrams": tv.get("ha_lac_hexagrams", {})
        }
        
    # 5. Ha Lac
    if "halac" in systems:
        hl = calculate_ha_lac(dt, gender=gender)
        payload["data"]["halac"] = {
            "thien_tong": hl["thien_tong"],
            "dia_tong": hl["dia_tong"],
            "tien_thien_hex": hl["tien_thien"]["hex_name"],
            "hau_thien_hex": hl["hau_thien"]["hex_name"],
            "nguyen_khi_line": hl["nguyen_khi"],
            "hoa_cong_line": hl["hoa_cong"]
        }
        
    # 6. Ky Mon
    if "kymon" in systems:
        km = calculate_ky_mon(dt)
        payload["data"]["kymon"] = {
            "dun_type": km["dun_type"],
            "lead_star": km["lead_star"],
            "lead_gate": km["lead_gate"],
            "palaces": km["palaces"]
        }

    # 7. Annual Forecast
    if "annual" in systems:
        ann = calculate_annual_forecast(dt, target_year=dt.year)
        payload["data"]["annual"] = ann

    # 8. Daoist Health & Alchemy
    if "health" in systems:
        hlth = diagnose_dan_dao_health(dt, gender=gender)
        payload["data"]["health"] = hlth

    # 9. Feng Shui Period 9
    if "fengshui" in systems:
        fs = calculate_feng_shui_period9("Tý")
        payload["data"]["fengshui"] = fs

    # 10. Bát Quái Mê Tung Bộ (Daoist Spatial Footwork)
    if "me_tung_bo" in systems or "footwork" in systems:
        mtb = calculate_bat_quai_me_tung_bo(dt, user_gender=gender)
        payload["data"]["me_tung_bo"] = mtb

    # 11. AI Reasoning Guidance & Rules Checklist
    guidance = [
        "1. Dùng các thuộc tính có cấu trúc (structured attributes) ở trên để đối chiếu khách quan, không phán đoán mơ hồ.",
        "2. Kiểm tra quan hệ ngũ hành giữa Nhật Chủ Bát Tự và Cung Thế Lục Hào.",
        "3. Lấy hào động làm then chốt biến động và xác định Ứng Kỳ.",
        "4. Tham chiếu Tam Cát Môn (Khai, Hưu, Sinh) trong Kỳ Môn để tìm hướng mưu sự.",
        "5. Đối chiếu Quẻ Tiên/Hậu Thiên Hà Lạc để đánh giá đại cục đường dài.",
        "6. Khâm Thiên Khí Đạo: Đối chiếu Tứ Hóa Năm Sinh (A-B-C-D), Tự Hóa và Hướng Tâm để nhận diện xung phá / lộc xuất.",
        "7. Phương Viên Lộc Kỵ Toàn Đồ: Đánh giá số lượng Lộc Quyền Khoa Kỵ tại bản cung và đối cung để phán đoán cát hung toàn cục."
    ]
    payload["reasoning_scaffolding"] = guidance
    
    # 10. Pre-Flight Triangulation & Epistemological Truth Arbitration (Tier 1 > Tier 2 > Tier 3)
    if triangulate:
        arbitrator = TriangulationArbitrator()
        triangulation_res = arbitrator.arbitrate_chart(
            dt=dt,
            gender=gender,
            birth_place=birth_place,
            longitude=longitude,
            discipline="synthesis",
            target_school=school,
            question=question
        )
        payload["data"]["triangulation"] = {
            "epistemological_hierarchy": triangulation_res["epistemological_hierarchy"],
            "consensus_score": triangulation_res["consensus_score"],
            "consensus_percentage": triangulation_res["consensus_percentage"],
            "coordinates": triangulation_res["coordinates"],
            "discrepancy_analysis": triangulation_res["discrepancy_analysis"],
            "grounded_master_citations": triangulation_res["grounded_master_citations"]
        }
    # Dual-schema compatibility: coordinates_meta and domain_systems aliases
    payload["coordinates_meta"] = payload["data"]["time_coords"]
    domain_map = {}
    if "iching" in payload["data"]:
        domain_map["iching_divination"] = payload["data"]["iching"]
    if "bazi" in payload["data"]:
        domain_map["bazi_four_pillars"] = payload["data"]["bazi"]
    if "tuvi" in payload["data"]:
        domain_map["tu_vi_astrolabe"] = payload["data"]["tuvi"]
    if "halac" in payload["data"]:
        domain_map["ha_lac_destiny"] = payload["data"]["halac"]
    if "kymon" in payload["data"]:
        domain_map["ky_mon_strategic"] = payload["data"]["kymon"]
    if "annual" in payload["data"]:
        domain_map["annual_forecast"] = payload["data"]["annual"]
    if "health" in payload["data"]:
        domain_map["daoist_health"] = payload["data"]["health"]
    if "fengshui" in payload["data"]:
        domain_map["feng_shui_period9"] = payload["data"]["fengshui"]
    payload["domain_systems"] = domain_map

    if "triangulation" in payload["data"]:
        payload["triangulation_arbitration"] = payload["data"]["triangulation"]

    payload["agent_workflow_sop"] = {
        "step_1_metadata": "BẮT BUỘC in nguyên văn bảng technical metadata lên đầu phản hồi (Rule 24, 25).",
        "step_2_interpretation": "Luận giải đa tầng: Dụng thần Bát Tự Điều Hầu, Tứ Hóa & Lục Sát Tinh Tử Vi (Rule 26), Ứng kỳ Lục Hào (Rule 27 nếu hỏi thời tiết).",
        "step_3_multi_school": "Nếu có dị biệt trường phái, trình bày song song và đặt câu hỏi hiệu chuẩn thực chứng (Rule 28).",
        "step_4_formatting": "BẮT BUỘC dùng mũi tên Unicode `→` (U+2192) hoặc ASCII `->`, KHÔNG dùng LaTeX `\\rightarrow` (Rule 29)."
    }

    return payload

def get_universal_tu_vi_payload(
    dt: Optional[datetime] = None,
    gender: int = 1,
    school: str = "standard",
    astrolabe_type: str = "thien_ban",
    cuc_override: Optional[int] = None
) -> Dict[str, Any]:
    """
    Dedicated high-density payload for Universal Tu Vi calculations.
    """
    if dt is None:
        dt = datetime.now().replace(tzinfo=LOCAL_TZ)
    return calculate_universal_tu_vi(
        dt,
        gender=gender,
        school=school,
        astrolabe_type=astrolabe_type,
        cuc_override=cuc_override
    )

def run_ziwei_stress_test(num_vectors: int = 1000) -> Dict[str, Any]:
    """
    Execute high-throughput multi-century stress testing pipeline.
    """
    return run_ziwei_stress_test_pipeline(num_vectors=num_vectors)

def compare_ground_truth_canonical_astrolabe(
    content_or_filepath: str,
    dt: Optional[datetime] = None,
    gender: int = 1,
    school: str = "standard",
    cuc_override: Optional[int] = None
) -> Dict[str, Any]:
    """
    Parse CanonicalAstrolabe 3-table format and run 7-step Zero-Diff comparison against Engine.
    """
    import os
    if os.path.exists(content_or_filepath):
        gt_data = parse_canonical_astrolabe_file(content_or_filepath)
    else:
        gt_data = parse_canonical_astrolabe_ai_copy(content_or_filepath)
        
    if dt is None:
        prof = gt_data.get("profile", {})
        dt_str = prof.get("birth_date_str") or prof.get("birth_date_raw", "")
        if dt_str:
            try:
                dt = parse_dt_string(dt_str)
            except Exception:
                dt = datetime.now().replace(tzinfo=LOCAL_TZ)
        else:
            dt = datetime.now().replace(tzinfo=LOCAL_TZ)
            
    p_gender = gt_data.get("profile", {}).get("gender", "Nam")
    if p_gender in ["Nữ", "nu", "Nu", "female", 0]:
        gender = 0
    else:
        gender = 1
        
    engine_chart = calculate_universal_tu_vi(
        dt,
        gender=gender,
        school=school,
        cuc_override=cuc_override
    )
    
    report = compare_engine_with_ground_truth(engine_chart, gt_data)
    
    return {
        "is_zero_diff": report.is_zero_diff,
        "total_diffs": report.total_diffs,
        "root_causes": list(report.root_causes),
        "summary_by_step": report.summary_by_step,
        "formatted_report": report.format_report(),
        "diff_details": [d.to_dict() for d in report.diff_details]
    }

def generate_ziwei_vectors(
    count: int = 100,
    include_edge_cases: bool = True,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Generate deterministic random and edge-case vectors from 1900 to 2100.
    """
    try:
        from tools.ziwei_vector_generator import generate_random_vectors, generate_edge_case_vectors
    except ImportError:
        import sys
        from pathlib import Path
        curr = Path(__file__).resolve().parent
        for _ in range(4):
            if (curr / "tools").is_dir():
                if str(curr) not in sys.path:
                    sys.path.insert(0, str(curr))
                break
            curr = curr.parent
        from tools.ziwei_vector_generator import generate_random_vectors, generate_edge_case_vectors

    rand_vecs = generate_random_vectors(count=count, seed=seed)
    edge_vecs = generate_edge_case_vectors() if include_edge_cases else []
    
    all_vecs = rand_vecs + edge_vecs
    return {
        "total_count": len(all_vecs),
        "count_random": len(rand_vecs),
        "count_edge_cases": len(edge_vecs),
        "vectors": all_vecs,
        "random_vectors": rand_vecs,
        "edge_case_vectors": edge_vecs
    }
