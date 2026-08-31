"""
Privacy Export Module (Zero-Telemetry Anonymized Pattern Exchange Engine)
Enables peer-to-peer and git-based pattern synchronization without leaking
any personally identifiable information (PII).
"""

import sqlite3
import json
import hashlib
import platform
import os
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from .distilled_rules import recalculate_confidence
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from distilled_rules import recalculate_confidence

def generate_contributor_hash(salt: str = "dao_tang_nho_v4") -> str:
    """Generate deterministic, irreversible machine fingerprint."""
    raw_node = f"{platform.node()}_{os.environ.get('USERNAME', 'agent')}_{salt}"
    return hashlib.sha256(raw_node.encode("utf-8")).hexdigest()[:16]

def anonymize_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize case data into pure structural format (zero PII)."""
    clean = {
        "discipline": case_data.get("discipline", "synthesis"),
        "question_category": case_data.get("category", "destiny"),
        "contributor_hash": generate_contributor_hash()
    }
    if "chart_summary" in case_data and case_data["chart_summary"]:
        try:
            cs = json.loads(case_data["chart_summary"]) if isinstance(case_data["chart_summary"], str) else case_data["chart_summary"]
            clean["chart_structure"] = {k: v for k, v in cs.items() if k not in ["name", "notes", "client"]}
        except Exception:
            clean["chart_structure"] = {}
            
    return clean

def export_patterns_jsonl(
    output_path: Union[str, Path],
    discipline: Optional[str] = None,
    min_confidence: float = 0.3,
    db_path: Optional[Union[str, Path]] = None
) -> int:
    """Export validated/candidate patterns into an anonymized JSONL file."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = _get_connection(db_path)
    count = 0
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        query = "SELECT * FROM patterns WHERE confidence >= ?"
        params = [min_confidence]
        if discipline:
            query += " AND (discipline_scope LIKE ? OR discipline_scope LIKE '%cross%')"
            params.append(f"%{discipline}%")
            
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        
        with out_file.open("w", encoding="utf-8") as f:
            for r in rows:
                item = {
                    "pattern_signature": r["pattern_signature"],
                    "pattern_type": r["pattern_type"],
                    "discipline_scope": r["discipline_scope"],
                    "description": r["description"],
                    "dao_root": r["dao_root"],
                    "canon_refs": r["canon_refs"],
                    "confidence": r["confidence"],
                    "support_count": r["support_count"],
                    "contradict_count": r["contradict_count"],
                    "status": r["status"],
                    "contributor_hash": generate_contributor_hash()
                }
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1
                
        return count
    finally:
        conn.close()

def import_patterns_jsonl(
    input_path: Union[str, Path],
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, int]:
    """Import and merge anonymized patterns from a JSONL file."""
    in_file = Path(input_path)
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found: {in_file}")
        
    conn = _get_connection(db_path)
    imported = 0
    merged = 0
    sigs_to_recalc = []
    
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        with in_file.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line.strip())
                sig = data.get("pattern_signature")
                if not sig:
                    continue
                    
                cursor.execute("SELECT * FROM patterns WHERE pattern_signature = ?", (sig,))
                existing = cursor.fetchone()
                
                if existing:
                    new_sup = existing["support_count"] + data.get("support_count", 0)
                    new_con = existing["contradict_count"] + data.get("contradict_count", 0)
                    cursor.execute(
                        "UPDATE patterns SET support_count = ?, contradict_count = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                        (new_sup, new_con, existing["id"])
                    )
                    merged += 1
                else:
                    cursor.execute(
                        """
                        INSERT INTO patterns (
                            pattern_signature, pattern_type, discipline_scope, description,
                            dao_root, canon_refs, confidence, support_count, contradict_count,
                            status, valid_from
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
                        """,
                        (
                            sig, data.get("pattern_type", "single"), data.get("discipline_scope"),
                            data.get("description"), data.get("dao_root"), data.get("canon_refs"),
                            data.get("confidence", 0.0), data.get("support_count", 1),
                            data.get("contradict_count", 0), data.get("status", "draft")
                        )
                    )
                    imported += 1
                sigs_to_recalc.append(sig)
                
        conn.commit()
    finally:
        conn.close()
        
    # Recalculate after closing connection
    for sig in set(sigs_to_recalc):
        recalculate_confidence(sig, db_path=db_path)
        
    return {"imported": imported, "merged": merged}
