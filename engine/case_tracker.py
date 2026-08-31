try:
    from .memory_schema import migrate_schema
except (ImportError, ValueError):
    from memory_schema import migrate_schema

"""
Case Tracker Database Module
Eastern Metaphysics All-In-One Engine

Tracks divination/destiny readings, specific predictions, real-world outcomes,
and historical accuracy metrics across all 8 metaphysical disciplines:
- kinh_dich (I Ching / Plum Blossom / Six Lines)
- tu_vi (Zi Wei Dou Shu)
- bat_tu (BaZi / Four Pillars)
- ky_mon (Qi Men Dun Jia)
- phong_thuy (Feng Shui)
- dan_dao (Internal Alchemy / Daoist Medicine)
- dong_y (Traditional Chinese Medicine)
- synthesis (Master Cross-Discipline Synthesis)

Zero external dependencies (SQLite3 + Python standard library only).
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union

# Default DB Path: data/case_tracker.db relative to project root
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "case_tracker.db"

VALID_DISCIPLINES = {
    "kinh_dich",
    "tu_vi",
    "bat_tu",
    "ky_mon",
    "phong_thuy",
    "dan_dao",
    "dong_y",
    "synthesis"
}

VALID_CATEGORIES = {
    "career",
    "health",
    "wealth",
    "relationship",
    "education",
    "other"
}

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    birth_dt TEXT,              -- ISO format birth datetime
    gender INTEGER DEFAULT 1,  -- 1=Male, 0=Female
    question TEXT,             -- User's question/concern
    discipline TEXT,           -- kinh_dich/tu_vi/bat_tu/ky_mon/phong_thuy/dan_dao/dong_y/synthesis
    chart_summary TEXT,        -- JSON summary of key chart data
    interpretation TEXT,       -- The interpretation/reading given
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    prediction_text TEXT NOT NULL,  -- What was predicted
    timeframe TEXT,                 -- When it should manifest (e.g. "2026 Q4", "Đại Vận 35-44")
    confidence REAL DEFAULT 0.7,   -- 0.0-1.0 confidence level
    category TEXT,                 -- career/health/wealth/relationship/education/other
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    actual_result TEXT NOT NULL,    -- What actually happened
    accuracy_score REAL,           -- 0.0 (wrong) to 1.0 (exact match)
    verified_at TEXT DEFAULT (datetime('now', 'localtime')),
    notes TEXT,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_cases_discipline ON cases(discipline);
CREATE INDEX IF NOT EXISTS idx_cases_created ON cases(created_at);
CREATE INDEX IF NOT EXISTS idx_predictions_case ON predictions(case_id);
CREATE INDEX IF NOT EXISTS idx_predictions_category ON predictions(category);
CREATE INDEX IF NOT EXISTS idx_predictions_created ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_outcomes_prediction ON outcomes(prediction_id);
"""


def _resolve_db_path(db_path: Optional[Union[str, Path]] = None) -> Union[str, Path]:
    """Resolve database path or fallback to default."""
    if db_path is None:
        return DEFAULT_DB_PATH
    if isinstance(db_path, str) and db_path == ":memory:":
        return ":memory:"
    return Path(db_path)


def _get_connection(db_path: Optional[Union[str, Path]] = None) -> sqlite3.Connection:
    """Create and configure a SQLite connection with foreign keys and row factory."""
    resolved = _resolve_db_path(db_path)
    if isinstance(resolved, Path):
        resolved.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(resolved))
    else:
        conn = sqlite3.connect(resolved)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Execute schema creation statements and memory migrations."""
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    migrate_schema(conn)


def init_db(db_path: Optional[Union[str, Path]] = None) -> str:
    """
    Initialize SQLite database and schema.
    Creates necessary directories if they do not exist.
    
    Args:
        db_path: Optional custom path or ':memory:'. Defaults to data/case_tracker.db.
        
    Returns:
        Absolute string path of the initialized database.
    """
    resolved = _resolve_db_path(db_path)
    conn = _get_connection(resolved)
    try:
        _ensure_schema(conn)
    finally:
        conn.close()
        
    if isinstance(resolved, Path):
        return str(resolved.resolve())
    return str(resolved)


def add_case(
    birth_dt: Optional[Union[str, datetime, date]] = None,
    gender: int = 1,
    question: str = "",
    discipline: str = "synthesis",
    chart_summary: Optional[Union[str, Dict[str, Any], List[Any]]] = None,
    interpretation: str = "",
    db_path: Optional[Union[str, Path]] = None
) -> int:
    """
    Insert a new reading/consultation case.
    
    Args:
        birth_dt: ISO format datetime string or datetime/date object.
        gender: 1 for Male, 0 for Female.
        question: User's question or concern.
        discipline: Metaphysics discipline (e.g. 'tu_vi', 'kinh_dich', 'synthesis').
        chart_summary: Chart details (dict, list, or JSON string).
        interpretation: Text interpretation or diagnosis given.
        db_path: Optional database path.
        
    Returns:
        The auto-generated case_id (int).
    """
    # Normalize birth_dt
    if isinstance(birth_dt, (datetime, date)):
        birth_dt_str = birth_dt.isoformat()
    elif birth_dt is not None:
        birth_dt_str = str(birth_dt)
    else:
        birth_dt_str = None

    # Normalize chart_summary to JSON string
    if chart_summary is not None and not isinstance(chart_summary, str):
        chart_summary_str = json.dumps(chart_summary, ensure_ascii=False)
    else:
        chart_summary_str = chart_summary

    gender_val = 1 if gender in (1, True, "1", "male", "Male", "Nam") else 0

    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cases (birth_dt, gender, question, discipline, chart_summary, interpretation)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (birth_dt_str, gender_val, question, discipline, chart_summary_str, interpretation)
        )
        case_id = cursor.lastrowid
        conn.commit()
        return case_id
    finally:
        conn.close()


def add_prediction(
    case_id: int,
    prediction_text: str,
    timeframe: Optional[str] = None,
    confidence: float = 0.7,
    category: str = "other",
    db_path: Optional[Union[str, Path]] = None
) -> int:
    """
    Add a specific testable prediction for a given case.
    
    Args:
        case_id: ID of the parent case.
        prediction_text: What was predicted.
        timeframe: Target manifestation timeframe (e.g., '2026 Q4', 'Tháng 8/2026').
        confidence: Confidence level between 0.0 and 1.0 (default 0.7).
        category: 'career', 'health', 'wealth', 'relationship', 'education', 'other'.
        db_path: Optional database path.
        
    Returns:
        The auto-generated prediction_id (int).
    """
    if not prediction_text or not prediction_text.strip():
        raise ValueError("prediction_text must not be empty.")
        
    conf = max(0.0, min(1.0, float(confidence)))
    cat = category.strip().lower() if category else "other"

    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # Verify case exists
        cursor.execute("SELECT id FROM cases WHERE id = ?", (case_id,))
        if not cursor.fetchone():
            raise ValueError(f"Case ID {case_id} does not exist.")
            
        cursor.execute(
            """
            INSERT INTO predictions (case_id, prediction_text, timeframe, confidence, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (case_id, prediction_text.strip(), timeframe, conf, cat)
        )
        prediction_id = cursor.lastrowid
        conn.commit()
        return prediction_id
    finally:
        conn.close()


def verify_prediction(
    prediction_id: int,
    actual_result: str,
    accuracy_score: float,
    notes: Optional[str] = None,
    db_path: Optional[Union[str, Path]] = None
) -> int:
    """
    Record an actual outcome and verify the accuracy of a prediction.
    
    Args:
        prediction_id: ID of the prediction being verified.
        actual_result: Description of what actually transpired.
        accuracy_score: Score from 0.0 (completely wrong) to 1.0 (exact match).
        notes: Additional contextual notes or analysis.
        db_path: Optional database path.
        
    Returns:
        The auto-generated outcome_id (int).
    """
    if not actual_result or not actual_result.strip():
        raise ValueError("actual_result must not be empty.")
        
    score = max(0.0, min(1.0, float(accuracy_score)))

    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # Verify prediction exists
        cursor.execute("SELECT id FROM predictions WHERE id = ?", (prediction_id,))
        if not cursor.fetchone():
            raise ValueError(f"Prediction ID {prediction_id} does not exist.")
            
        cursor.execute(
            """
            INSERT INTO outcomes (prediction_id, actual_result, accuracy_score, notes)
            VALUES (?, ?, ?, ?)
            """,
            (prediction_id, actual_result.strip(), score, notes)
        )
        outcome_id = cursor.lastrowid
        conn.commit()
        return outcome_id
    finally:
        conn.close()


def get_case(case_id: int, db_path: Optional[Union[str, Path]] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieve full case details including all predictions and verified outcomes.
    
    Args:
        case_id: ID of the case to retrieve.
        db_path: Optional database path.
        
    Returns:
        Dictionary representation of case with nested predictions & outcomes,
        or None if case_id is not found.
    """
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
        case_row = cursor.fetchone()
        if not case_row:
            return None
            
        case_data = dict(case_row)
        
        # Attempt parsing chart_summary if JSON
        if case_data.get("chart_summary"):
            try:
                case_data["chart_summary_parsed"] = json.loads(case_data["chart_summary"])
            except (json.JSONDecodeError, TypeError):
                case_data["chart_summary_parsed"] = None
        else:
            case_data["chart_summary_parsed"] = None

        # Fetch predictions for this case
        cursor.execute(
            "SELECT * FROM predictions WHERE case_id = ? ORDER BY id ASC",
            (case_id,)
        )
        prediction_rows = cursor.fetchall()
        
        predictions = []
        for p_row in prediction_rows:
            p_dict = dict(p_row)
            # Fetch latest outcome for prediction
            cursor.execute(
                "SELECT * FROM outcomes WHERE prediction_id = ? ORDER BY id DESC LIMIT 1",
                (p_dict["id"],)
            )
            outcome_row = cursor.fetchone()
            p_dict["outcome"] = dict(outcome_row) if outcome_row else None
            predictions.append(p_dict)
            
        case_data["predictions"] = predictions
        return case_data
    finally:
        conn.close()


def list_cases(
    discipline: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """
    List cases with summary metrics, optionally filtered by discipline.
    
    Args:
        discipline: Optional filter ('tu_vi', 'kinh_dich', etc.).
        limit: Maximum number of cases to return (default 20).
        offset: Offset for pagination (default 0).
        db_path: Optional database path.
        
    Returns:
        List of case dictionaries with prediction counts and verification counts.
    """
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                c.*,
                COUNT(DISTINCT p.id) AS prediction_count,
                COUNT(DISTINCT o.id) AS verified_count
            FROM cases c
            LEFT JOIN predictions p ON c.id = p.case_id
            LEFT JOIN outcomes o ON p.id = o.prediction_id
        """
        params: List[Any] = []
        if discipline:
            query += " WHERE c.discipline = ?"
            params.append(discipline)
            
        query += " GROUP BY c.id ORDER BY c.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            if d.get("chart_summary"):
                try:
                    d["chart_summary_parsed"] = json.loads(d["chart_summary"])
                except Exception:
                    d["chart_summary_parsed"] = None
            else:
                d["chart_summary_parsed"] = None
            results.append(d)
            
        return results
    finally:
        conn.close()


def get_accuracy_report(
    discipline: Optional[str] = None,
    db_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive accuracy and verification statistics.
    
    Args:
        discipline: Optional filter by discipline.
        db_path: Optional database path.
        
    Returns:
        Dictionary containing overall stats, average accuracy, category breakdown,
        and discipline breakdown.
    """
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        # 1. Total cases
        if discipline:
            cursor.execute("SELECT COUNT(*) FROM cases WHERE discipline = ?", (discipline,))
        else:
            cursor.execute("SELECT COUNT(*) FROM cases")
        total_cases = cursor.fetchone()[0]
        
        # 2. Total predictions & average confidence
        pred_query = """
            SELECT COUNT(p.id), AVG(p.confidence)
            FROM predictions p
            JOIN cases c ON p.case_id = c.id
        """
        params: List[Any] = []
        if discipline:
            pred_query += " WHERE c.discipline = ?"
            params.append(discipline)
            
        cursor.execute(pred_query, params)
        pred_row = cursor.fetchone()
        total_predictions = pred_row[0] or 0
        avg_confidence = round(pred_row[1], 4) if pred_row[1] is not None else 0.0
        
        # 3. Verified predictions & average accuracy
        verified_query = """
            SELECT 
                COUNT(DISTINCT p.id) AS verified_count,
                AVG(o.accuracy_score) AS avg_accuracy
            FROM predictions p
            JOIN cases c ON p.case_id = c.id
            JOIN outcomes o ON p.id = o.prediction_id
        """
        if discipline:
            verified_query += " WHERE c.discipline = ?"
            cursor.execute(verified_query, (discipline,))
        else:
            cursor.execute(verified_query)
            
        ver_row = cursor.fetchone()
        verified_predictions = ver_row[0] or 0
        avg_accuracy = round(ver_row[1], 4) if ver_row[1] is not None else 0.0
        
        unverified_predictions = max(0, total_predictions - verified_predictions)
        verification_rate = round(verified_predictions / total_predictions, 4) if total_predictions > 0 else 0.0
        
        # 4. Breakdown by category
        cat_query = """
            SELECT 
                p.category,
                COUNT(DISTINCT p.id) AS total_preds,
                COUNT(DISTINCT o.id) AS verified_preds,
                AVG(p.confidence) AS avg_conf,
                AVG(o.accuracy_score) AS avg_acc
            FROM predictions p
            JOIN cases c ON p.case_id = c.id
            LEFT JOIN outcomes o ON p.id = o.prediction_id
        """
        if discipline:
            cat_query += " WHERE c.discipline = ?"
            cat_query += " GROUP BY p.category ORDER BY total_preds DESC"
            cursor.execute(cat_query, (discipline,))
        else:
            cat_query += " GROUP BY p.category ORDER BY total_preds DESC"
            cursor.execute(cat_query)
            
        by_category: Dict[str, Any] = {}
        for r in cursor.fetchall():
            cat_name = r["category"] or "other"
            by_category[cat_name] = {
                "total": r["total_preds"],
                "verified": r["verified_preds"],
                "avg_confidence": round(r["avg_conf"], 4) if r["avg_conf"] is not None else 0.0,
                "avg_accuracy": round(r["avg_acc"], 4) if r["avg_acc"] is not None else 0.0
            }

        # 5. Breakdown by discipline (if discipline is None)
        by_discipline: Dict[str, Any] = {}
        if discipline is None:
            disc_query = """
                SELECT 
                    c.discipline,
                    COUNT(DISTINCT c.id) AS total_c,
                    COUNT(DISTINCT p.id) AS total_p,
                    COUNT(DISTINCT o.id) AS verified_p,
                    AVG(o.accuracy_score) AS avg_acc
                FROM cases c
                LEFT JOIN predictions p ON c.id = p.case_id
                LEFT JOIN outcomes o ON p.id = o.prediction_id
                GROUP BY c.discipline
                ORDER BY total_c DESC
            """
            cursor.execute(disc_query)
            for r in cursor.fetchall():
                d_name = r["discipline"] or "unknown"
                by_discipline[d_name] = {
                    "cases": r["total_c"],
                    "predictions": r["total_p"],
                    "verified": r["verified_p"],
                    "avg_accuracy": round(r["avg_acc"], 4) if r["avg_acc"] is not None else 0.0
                }
                
        return {
            "discipline_filter": discipline or "all",
            "total_cases": total_cases,
            "total_predictions": total_predictions,
            "verified_predictions": verified_predictions,
            "unverified_predictions": unverified_predictions,
            "verification_rate": verification_rate,
            "avg_confidence": avg_confidence,
            "avg_accuracy": avg_accuracy,
            "by_category": by_category,
            "by_discipline": by_discipline
        }
    finally:
        conn.close()


def get_unverified_predictions(
    days_old: int = 30,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve predictions that have not yet been verified with an outcome.
    
    Args:
        days_old: Minimum age in days since prediction was recorded (default 30).
                  Set to 0 to return all unverified predictions regardless of age.
        db_path: Optional database path.
        
    Returns:
        List of unverified prediction dictionaries with parent case context.
    """
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        
        if days_old > 0:
            query = """
                SELECT 
                    p.id AS prediction_id,
                    p.case_id,
                    p.prediction_text,
                    p.timeframe,
                    p.confidence,
                    p.category,
                    p.created_at AS prediction_created_at,
                    c.birth_dt,
                    c.gender,
                    c.question,
                    c.discipline
                FROM predictions p
                JOIN cases c ON p.case_id = c.id
                LEFT JOIN outcomes o ON p.id = o.prediction_id
                WHERE o.id IS NULL
                  AND (julianday('now', 'localtime') - julianday(p.created_at)) >= ?
                ORDER BY p.created_at ASC
            """
            cursor.execute(query, (days_old,))
        else:
            query = """
                SELECT 
                    p.id AS prediction_id,
                    p.case_id,
                    p.prediction_text,
                    p.timeframe,
                    p.confidence,
                    p.category,
                    p.created_at AS prediction_created_at,
                    c.birth_dt,
                    c.gender,
                    c.question,
                    c.discipline
                FROM predictions p
                JOIN cases c ON p.case_id = c.id
                LEFT JOIN outcomes o ON p.id = o.prediction_id
                WHERE o.id IS NULL
                ORDER BY p.created_at ASC
            """
            cursor.execute(query)
            
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_case(case_id: int, db_path: Optional[Union[str, Path]] = None) -> bool:
    """
    Delete a case and all cascading predictions and outcomes.
    
    Args:
        case_id: ID of the case to delete.
        db_path: Optional database path.
        
    Returns:
        True if a row was deleted, False otherwise.
    """
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        return deleted
    finally:
        conn.close()
