"""
Consolidation Loop Module (Session-End Reflection & Verification Ingestion Engine)
Inspired by Letta/Mem0 consolidation loops:
1. Session-End Consolidation: Automatically extracts patterns, seeds L4, links L5 person.
2. Verification Consolidation: Ingests ground-truth outcomes, updates pattern confidence & thresholds.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .case_tracker import _get_connection, _ensure_schema, verify_prediction
    from .pattern_extractor import (
        extract_iching_patterns,
        extract_bazi_patterns,
        extract_tuvi_patterns,
        extract_cross_patterns
    )
    from .distilled_rules import add_or_update_pattern, add_counter_evidence, recalculate_confidence
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, verify_prediction
    from pattern_extractor import (
        extract_iching_patterns,
        extract_bazi_patterns,
        extract_tuvi_patterns,
        extract_cross_patterns
    )
    from distilled_rules import add_or_update_pattern, add_counter_evidence, recalculate_confidence

def consolidate_case(
    case_id: int,
    engine_result: Dict[str, Any],
    discipline: str,
    person_id: Optional[int] = None,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Consolidate reading output into memory patterns and profile links."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # Link person if provided
        if person_id is not None:
            cursor.execute("UPDATE cases SET person_id = ? WHERE id = ?", (person_id, case_id))
            conn.commit()
    finally:
        conn.close()
        
    extracted = []
    disc = discipline.lower().strip()
    
    if disc in ["kinh_dich", "luc_hao", "mai_hoa"]:
        extracted.extend(extract_iching_patterns(engine_result))
    elif disc in ["bat_tu", "bazi"]:
        extracted.extend(extract_bazi_patterns(engine_result))
    elif disc in ["tu_vi", "ziwei"]:
        extracted.extend(extract_tuvi_patterns(engine_result))
    elif disc in ["synthesis", "cross_discipline"]:
        # If composite synthesis payload
        p_by_d = {}
        if "luc_hao_res" in engine_result:
            p_by_d["kinh_dich"] = extract_iching_patterns(engine_result["luc_hao_res"])
            extracted.extend(p_by_d["kinh_dich"])
        if "bazi" in engine_result:
            p_by_d["bat_tu"] = extract_bazi_patterns(engine_result["bazi"])
            extracted.extend(p_by_d["bat_tu"])
        if "tu_vi" in engine_result:
            p_by_d["tu_vi"] = extract_tuvi_patterns(engine_result["tu_vi"])
            extracted.extend(p_by_d["tu_vi"])
        extracted.extend(extract_cross_patterns(p_by_d))
        
    # Ingest into distilled rules
    updated_patterns = []
    for pat in extracted:
        res = add_or_update_pattern(
            pattern_signature=pat["signature"],
            case_id=case_id,
            is_supporting=True,
            reason=pat.get("description"),
            discipline_scope=pat.get("discipline", discipline),
            description=pat.get("description"),
            dao_root=pat.get("dao_root"),
            db_path=db_path
        )
        updated_patterns.append(res)
        
    return {
        "case_id": case_id,
        "person_id": person_id,
        "patterns_extracted_count": len(extracted),
        "patterns": updated_patterns
    }

def consolidate_verification(
    case_id: int,
    prediction_id: int,
    actual_result: str,
    accuracy_score: float,
    notes: Optional[str] = None,
    root_cause: str = "pattern_issue",
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Ingest verification outcome and update linked pattern confidence."""
    # 1. Update outcome in case_tracker
    verify_prediction(
        prediction_id=prediction_id,
        actual_result=actual_result,
        accuracy_score=accuracy_score,
        notes=notes,
        db_path=db_path
    )
    
    # 2. Find all patterns linked to this case
    conn = _get_connection(db_path)
    linked_patterns = []
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.id, p.pattern_signature, pc.id as pc_id
            FROM patterns p
            JOIN pattern_cases pc ON p.id = pc.pattern_id
            WHERE pc.case_id = ?
            """,
            (case_id,)
        )
        linked_patterns = [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()
        
    is_supporting = (accuracy_score >= 0.6)
    affected = []
    
    for lp in linked_patterns:
        sig = lp["pattern_signature"]
        if is_supporting:
            res = add_or_update_pattern(
                pattern_signature=sig,
                case_id=case_id,
                is_supporting=True,
                reason=f"Verified success: {actual_result} (Score: {accuracy_score})",
                db_path=db_path
            )
        else:
            res = add_counter_evidence(
                pattern_signature=sig,
                case_id=case_id,
                reason=f"Verified mismatch: {actual_result} (Score: {accuracy_score})",
                root_cause=root_cause,
                db_path=db_path
            )
        affected.append(res)
        
    return {
        "case_id": case_id,
        "prediction_id": prediction_id,
        "accuracy_score": accuracy_score,
        "is_supporting": is_supporting,
        "patterns_affected": affected
    }
