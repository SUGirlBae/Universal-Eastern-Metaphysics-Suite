"""
Similarity Finder Module (Structural Metaphysical Resonance Engine)
Finds common patterns, formulaic intersections, and destiny resonances
between distinct individuals without conflating personal narratives.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List, Set

try:
    from .case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from .pattern_extractor import normalize_pattern_signature
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from pattern_extractor import normalize_pattern_signature

def compute_pattern_overlap(patterns_a: List[str], patterns_b: List[str]) -> float:
    """Compute Jaccard similarity index between two pattern sets."""
    if not patterns_a or not patterns_b:
        return 0.0
    set_a = {normalize_pattern_signature(p) for p in patterns_a}
    set_b = {normalize_pattern_signature(p) for p in patterns_b}
    
    inter = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return round(len(inter) / len(union), 3) if union else 0.0

def compute_bazi_resonance(sig_a: str, sig_b: str) -> float:
    """Calculate structural resonance score between two Bazi signatures."""
    if not sig_a or not sig_b:
        return 0.0
    parts_a = set(sig_a.lower().split("_"))
    parts_b = set(sig_b.lower().split("_"))
    
    # Exclude trivial tokens
    noise = {"tháng", "năm", "mệnh", "cục"}
    p_a = parts_a - noise
    p_b = parts_b - noise
    
    if not p_a or not p_b:
        return 0.0
        
    inter = p_a.intersection(p_b)
    union = p_a.union(p_b)
    return round(len(inter) / len(union), 3)

def find_similar_cases(
    case_id: Optional[int] = None,
    pattern_signatures: Optional[List[str]] = None,
    discipline: Optional[str] = None,
    exclude_person_id: Optional[int] = None,
    limit: int = 10,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """Find other cases sharing structural patterns with the target case."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        target_sigs = set(pattern_signatures or [])
        if case_id is not None and not target_sigs:
            cursor.execute(
                """
                SELECT p.pattern_signature
                FROM patterns p
                JOIN pattern_cases pc ON p.id = pc.pattern_id
                WHERE pc.case_id = ?
                """,
                (case_id,)
            )
            target_sigs = {r["pattern_signature"] for r in cursor.fetchall()}
            
        if not target_sigs:
            return []
            
        placeholders = ",".join(["?"] * len(target_sigs))
        query = f"""
            SELECT c.id as case_id, c.birth_dt, c.question, c.discipline, c.person_id,
                   COUNT(pc.pattern_id) as overlap_count,
                   GROUP_CONCAT(p.pattern_signature, ', ') as matching_patterns
            FROM cases c
            JOIN pattern_cases pc ON c.id = pc.case_id
            JOIN patterns p ON p.id = pc.pattern_id
            WHERE p.pattern_signature IN ({placeholders})
        """
        params = list(target_sigs)
        
        if case_id is not None:
            query += " AND c.id != ?"
            params.append(case_id)
        if exclude_person_id is not None:
            query += " AND (c.person_id IS NULL OR c.person_id != ?)"
            params.append(exclude_person_id)
        if discipline:
            query += " AND c.discipline = ?"
            params.append(discipline)
            
        query += f" GROUP BY c.id ORDER BY overlap_count DESC, c.id DESC LIMIT {limit}"
        
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()

def find_similar_persons(
    person_id: Optional[int] = None,
    bazi_signature: Optional[str] = None,
    limit: int = 5,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """Find individuals with structurally resonant destiny signatures."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        target_sig = bazi_signature
        target_pid = person_id
        
        if person_id is not None and not target_sig:
            cursor.execute("SELECT bazi_signature FROM person_profiles WHERE id = ?", (person_id,))
            row = cursor.fetchone()
            if row:
                target_sig = row["bazi_signature"]
                
        if not target_sig:
            return []
            
        cursor.execute("SELECT * FROM person_profiles")
        all_persons = [dict(r) for r in cursor.fetchall()]
        
        scored = []
        for p in all_persons:
            if target_pid and p["id"] == target_pid:
                continue
            res_score = compute_bazi_resonance(target_sig, p.get("bazi_signature") or "")
            if res_score > 0.2:
                p_copy = dict(p)
                p_copy["resonance_score"] = res_score
                scored.append(p_copy)
                
        scored.sort(key=lambda x: x["resonance_score"], reverse=True)
        return scored[:limit]
    finally:
        conn.close()
