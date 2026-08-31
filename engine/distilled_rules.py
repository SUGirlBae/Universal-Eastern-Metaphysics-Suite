"""
Distilled Rules Module (L4: Distilled Knowledge & Three-Tier Threshold Engine)
Implements autonomous pattern crystallization, bi-temporal validation,
and root-cause counter-evidence adjudication.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from .pattern_extractor import normalize_pattern_signature
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, _resolve_db_path
    from pattern_extractor import normalize_pattern_signature

def recalculate_confidence(pattern_signature: str, db_path: Optional[Union[str, Path]] = None) -> float:
    """Calculate calibrated confidence score (0.0 - 0.95)."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT support_count, contradict_count, canon_refs FROM patterns WHERE pattern_signature = ?", (pattern_signature,))
        row = cursor.fetchone()
        if not row:
            return 0.0
            
        sup = row["support_count"]
        con = row["contradict_count"]
        canon_refs = json.loads(row["canon_refs"]) if row["canon_refs"] else []
        
        total = sup + con
        if total == 0:
            base = 0.0
        else:
            base = sup / total
            
        canon_bonus = 0.10 if canon_refs else 0.0
        conf = min(0.95, round(base * 0.85 + canon_bonus, 3))
        
        cursor.execute("UPDATE patterns SET confidence = ?, updated_at = datetime('now', 'localtime') WHERE pattern_signature = ?", (conf, pattern_signature))
        conn.commit()
        return conf
    finally:
        conn.close()

def add_or_update_pattern(
    pattern_signature: str,
    case_id: int,
    is_supporting: bool = True,
    reason: Optional[str] = None,
    discipline_scope: Optional[Union[str, List[str]]] = None,
    description: Optional[str] = None,
    dao_root: Optional[str] = None,
    canon_refs: Optional[Union[str, List[str]]] = None,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Ingest a case into a pattern and advance its state along the Three-Tier Threshold:
    - Tier 1 (1 support): draft
    - Tier 2 (3+ supports): candidate
    - Tier 3 (7+ supports AND canon backed): validated
    """
    sig = normalize_pattern_signature(pattern_signature)
    disc_scope_str = json.dumps(discipline_scope, ensure_ascii=False) if isinstance(discipline_scope, list) else discipline_scope
    canon_refs_str = json.dumps(canon_refs, ensure_ascii=False) if isinstance(canon_refs, list) else canon_refs
    
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # 1. Get or create pattern record
        cursor.execute("SELECT * FROM patterns WHERE pattern_signature = ?", (sig,))
        pat = cursor.fetchone()
        
        if not pat:
            cursor.execute(
                """
                INSERT INTO patterns (
                    pattern_signature, discipline_scope, description, dao_root,
                    canon_refs, support_count, contradict_count, status, valid_from
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', datetime('now', 'localtime'))
                """,
                (sig, disc_scope_str, description, dao_root, canon_refs_str, 0, 0)
            )
            pattern_id = cursor.lastrowid
        else:
            pattern_id = pat["id"]
            # Update fields if provided
            if description and not pat["description"]:
                cursor.execute("UPDATE patterns SET description = ? WHERE id = ?", (description, pattern_id))
            if canon_refs_str and not pat["canon_refs"]:
                cursor.execute("UPDATE patterns SET canon_refs = ? WHERE id = ?", (canon_refs_str, pattern_id))
            if dao_root and not pat["dao_root"]:
                cursor.execute("UPDATE patterns SET dao_root = ? WHERE id = ?", (dao_root, pattern_id))
                
        # 2. Link case in pattern_cases
        cursor.execute(
            """
            INSERT OR IGNORE INTO pattern_cases (pattern_id, case_id, is_supporting, reason)
            VALUES (?, ?, ?, ?)
            """,
            (pattern_id, case_id, 1 if is_supporting else 0, reason)
        )
        
        # 3. Recount supports and contradicts from pattern_cases
        cursor.execute("SELECT COUNT(*) FROM pattern_cases WHERE pattern_id = ? AND is_supporting = 1", (pattern_id,))
        sup_cnt = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pattern_cases WHERE pattern_id = ? AND is_supporting = 0", (pattern_id,))
        con_cnt = cursor.fetchone()[0]
        
        # 4. Check status transition
        cursor.execute("SELECT canon_refs, status FROM patterns WHERE id = ?", (pattern_id,))
        p_row = cursor.fetchone()
        has_canon = bool(p_row["canon_refs"])
        curr_status = p_row["status"]
        
        new_status = curr_status
        if con_cnt >= 3 and curr_status == "validated":
            new_status = "suspended"
        elif sup_cnt >= 7 and has_canon:
            new_status = "validated"
        elif sup_cnt >= 3:
            new_status = "candidate"
        elif sup_cnt >= 1 and curr_status == "draft":
            new_status = "draft"
            
        cursor.execute(
            "UPDATE patterns SET support_count = ?, contradict_count = ?, status = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
            (sup_cnt, con_cnt, new_status, pattern_id)
        )
        conn.commit()
        
        # 5. Recalculate confidence
        recalculate_confidence(sig, db_path=db_path)
        
        cursor.execute("SELECT * FROM patterns WHERE id = ?", (pattern_id,))
        return dict(cursor.fetchone())
    finally:
        conn.close()

def get_pattern(pattern_signature: str, db_path: Optional[Union[str, Path]] = None) -> Optional[Dict[str, Any]]:
    """Fetch pattern by signature."""
    sig = normalize_pattern_signature(pattern_signature)
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patterns WHERE pattern_signature = ?", (sig,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def search_patterns(
    discipline: Optional[str] = None,
    status: Optional[str] = None,
    min_confidence: Optional[float] = None,
    keyword: Optional[str] = None,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """Search and filter patterns."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        query = "SELECT * FROM patterns WHERE 1=1"
        params = []
        
        if discipline:
            query += " AND discipline_scope LIKE ?"
            params.append(f"%{discipline}%")
        if status:
            query += " AND status = ?"
            params.append(status)
        if min_confidence is not None:
            query += " AND confidence >= ?"
            params.append(min_confidence)
        if keyword:
            query += " AND (pattern_signature LIKE ? OR description LIKE ? OR dao_root LIKE ?)"
            kw = f"%{keyword.strip()}%"
            params.extend([kw, kw, kw])
            
        query += " ORDER BY confidence DESC, support_count DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()

def add_counter_evidence(
    pattern_signature: str,
    case_id: int,
    reason: str,
    root_cause: str = "pattern_issue",
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Register counter-evidence with root-cause analysis.
    root_cause: 'missing_variable' | 'bad_input' | 'pattern_issue' | 'unknown'
    """
    sig = normalize_pattern_signature(pattern_signature)
    
    # If bad_input (e.g. wrong birth hour or unfocused querent), do not count against the pattern formula
    is_hard_contradiction = (root_cause in ["pattern_issue", "unknown"])
    
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM patterns WHERE pattern_signature = ?", (sig,))
        pat = cursor.fetchone()
        if not pat:
            raise ValueError(f"Pattern '{sig}' does not exist.")
        pattern_id = pat["id"]
        
        full_reason = f"[{root_cause.upper()}] {reason}"
        cursor.execute(
            """
            INSERT OR REPLACE INTO pattern_cases (pattern_id, case_id, is_supporting, reason)
            VALUES (?, ?, ?, ?)
            """,
            (pattern_id, case_id, 0 if is_hard_contradiction else 1, full_reason)
        )
        conn.commit()
    finally:
        conn.close()
        
    # Re-adjudicate pattern state
    return add_or_update_pattern(sig, case_id=case_id, is_supporting=(not is_hard_contradiction), reason=full_reason, db_path=db_path)

def get_active_rules(discipline: Optional[str] = None, min_confidence: float = 0.5, db_path: Optional[Union[str, Path]] = None) -> List[Dict[str, Any]]:
    """Retrieve all validated rules currently in active circulation."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        query = "SELECT * FROM patterns WHERE status IN ('validated', 'candidate') AND valid_until IS NULL AND confidence >= ?"
        params = [min_confidence]
        if discipline:
            query += " AND (discipline_scope LIKE ? OR discipline_scope LIKE '%cross%')"
            params.append(f"%{discipline}%")
            
        query += " ORDER BY confidence DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()
