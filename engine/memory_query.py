"""
Unified Memory Query Module (L0 - L5 Multi-Tier Federated Retrieval API)
Coordinates across classical canon, expert rules, distilled patterns,
case histories, and individual person profiles.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .case_tracker import _get_connection, _ensure_schema, get_accuracy_report
    from .person_profile import get_person
    from .distilled_rules import get_active_rules, search_patterns
    from .similarity_finder import find_similar_cases, find_similar_persons
    from .classical_canon_rag import search_classical_canon
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, get_accuracy_report
    from person_profile import get_person
    from distilled_rules import get_active_rules, search_patterns
    from similarity_finder import find_similar_cases, find_similar_persons
    from classical_canon_rag import search_classical_canon

def query_memory(
    question: str = "",
    discipline: Optional[str] = None,
    person_id: Optional[int] = None,
    pattern_signatures: Optional[List[str]] = None,
    include_canon: bool = True,
    include_patterns: bool = True,
    include_cases: bool = True,
    limit: int = 5,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """Execute federated multi-tier query across the memory stack."""
    results = {
        "person_profile": None,
        "active_patterns": [],
        "similar_cases": [],
        "canon_citations": []
    }
    
    # 1. Person Profile (L5)
    if person_id is not None:
        results["person_profile"] = get_person(person_id, db_path=db_path)
        
    # 2. Active Patterns (L4)
    if include_patterns:
        if pattern_signatures:
            matched = []
            for sig in pattern_signatures:
                pats = search_patterns(keyword=sig, db_path=db_path)
                matched.extend(pats)
            results["active_patterns"] = matched[:limit]
        else:
            active = get_active_rules(discipline=discipline, min_confidence=0.1, db_path=db_path)
            if not active and discipline:
                active = search_patterns(discipline=discipline, db_path=db_path)
            if not active:
                active = search_patterns(db_path=db_path)
            results["active_patterns"] = active[:limit]
            
    # 3. Similar Cases (L3)
    if include_cases:
        results["similar_cases"] = find_similar_cases(
            pattern_signatures=pattern_signatures,
            discipline=discipline,
            exclude_person_id=person_id,
            limit=limit,
            db_path=db_path
        )
        
    # 4. Classical Canon (L1)
    if include_canon and question:
        try:
            results["canon_citations"] = search_classical_canon(question, discipline=discipline, limit=limit)
        except Exception:
            results["canon_citations"] = []
            
    return results

def get_memory_stats(db_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Retrieve comprehensive statistics across all memory layers."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # Persons
        cursor.execute("SELECT COUNT(*) FROM person_profiles")
        n_persons = cursor.fetchone()[0]
        
        # Cases
        cursor.execute("SELECT COUNT(*) FROM cases")
        n_cases = cursor.fetchone()[0]
        
        # Patterns by status
        cursor.execute("SELECT status, COUNT(*) as cnt FROM patterns GROUP BY status")
        status_map = {r["status"]: r["cnt"] for r in cursor.fetchall()}
        
        cursor.execute("SELECT AVG(confidence) FROM patterns")
        avg_conf = cursor.fetchone()[0] or 0.0
        
        # Case accuracy
        acc_rep = get_accuracy_report(db_path=db_path)
        
        return {
            "total_persons": n_persons,
            "total_cases": n_cases,
            "total_patterns": sum(status_map.values()),
            "patterns_by_status": status_map,
            "avg_pattern_confidence": round(avg_conf, 3),
            "verification_stats": acc_rep
        }
    finally:
        conn.close()

def get_person_journey(person_id: int, db_path: Optional[Union[str, Path]] = None) -> Optional[Dict[str, Any]]:
    """Construct complete longitudinal consultation journey of an individual."""
    profile = get_person(person_id, db_path=db_path)
    if not profile:
        return None
        
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # Get cases of this person
        cursor.execute(
            """
            SELECT c.id, c.question, c.discipline, c.created_at,
                   GROUP_CONCAT(p.pattern_signature, ', ') as patterns
            FROM cases c
            LEFT JOIN pattern_cases pc ON c.id = pc.case_id
            LEFT JOIN patterns p ON p.id = pc.pattern_id
            WHERE c.person_id = ?
            GROUP BY c.id
            ORDER BY c.id DESC
            """,
            (person_id,)
        )
        cases = [dict(r) for r in cursor.fetchall()]
        
        # Find resonant similar individuals
        similar_people = find_similar_persons(person_id=person_id, limit=3, db_path=db_path)
        
        return {
            "profile": profile,
            "total_cases": len(cases),
            "cases": cases,
            "resonant_persons": similar_people
        }
    finally:
        conn.close()
