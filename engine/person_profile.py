"""
Person Profile Module (L5: Individual Profile & Resonance Layer)
Manages individual destiny coordinates, relationships, notes,
and auto-computes Bazi / Ziwei structural signatures.
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Union, Dict, Any, List

try:
    from .case_tracker import _get_connection, _ensure_schema, _resolve_db_path, DEFAULT_DB_PATH
    from .bazi_engine import calculate_bazi
    from .tu_vi_advanced import calculate_universal_tu_vi
    from .lunar_solar import LOCAL_TZ
except (ImportError, ValueError):
    from case_tracker import _get_connection, _ensure_schema, _resolve_db_path, DEFAULT_DB_PATH
    from bazi_engine import calculate_bazi
    from tu_vi_advanced import calculate_universal_tu_vi
    from lunar_solar import LOCAL_TZ

def parse_dt(dt_val: Optional[Union[str, datetime, date]]) -> Optional[datetime]:
    if dt_val is None:
        return None
    if isinstance(dt_val, datetime):
        return dt_val if dt_val.tzinfo else dt_val.replace(tzinfo=LOCAL_TZ)
    if isinstance(dt_val, date):
        return datetime(dt_val.year, dt_val.month, dt_val.day, 0, 0, tzinfo=LOCAL_TZ)
    
    dt_str = str(dt_val).strip()
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
            return datetime.strptime(dt_str, fmt).replace(tzinfo=LOCAL_TZ)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(dt_str).replace(tzinfo=LOCAL_TZ)
    except Exception:
        return None

def compute_bazi_signature(birth_dt: Union[str, datetime, date], gender: int = 1) -> str:
    """Compute Bazi signature string (e.g. 'Nhâm_tháng_Hợi_năm_Kỷ_Mão_Hàn')."""
    dt = parse_dt(birth_dt)
    if not dt:
        return ""
    try:
        bazi = calculate_bazi(dt, gender=gender)
        pillars = bazi.get("pillars", {})
        
        year_cc = pillars.get("year", {}).get("can_chi", "").replace(" ", "_")
        month_parts = pillars.get("month", {}).get("can_chi", "").split()
        month_branch = month_parts[1] if len(month_parts) > 1 else ""
        
        day_parts = pillars.get("day", {}).get("can_chi", "").split()
        day_stem = day_parts[0] if day_parts else ""
        
        season = "Hàn" if month_branch in ["Hợi", "Tý", "Sửu"] else ("Nhiệt" if month_branch in ["Tỵ", "Ngọ", "Mùi"] else "Ôn")
        
        sig = f"{day_stem}_tháng_{month_branch}_năm_{year_cc}_{season}"
        return sig
    except Exception:
        return ""

def compute_tuvi_signature(birth_dt: Union[str, datetime, date], gender: int = 1) -> str:
    """Compute Ziwei signature string (e.g. 'Tử_Vi_Tham_Lang_Mệnh_Mão_Thủy_Nhị_Cục')."""
    dt = parse_dt(birth_dt)
    if not dt:
        return ""
    try:
        tuvi = calculate_universal_tu_vi(dt, gender=gender)
        cp = tuvi.get("client_profile", {})
        cuc_name = cp.get("cuc_name", "").replace(" ", "_")
        menh_branch = cp.get("menh_branch", "")
        
        palaces = tuvi.get("palaces", [])
        menh_stars = []
        for p in palaces:
            if p.get("is_menh"):
                menh_stars = [s.get("name", "") for s in p.get("main_stars", [])]
                break
                
        stars_str = "_".join(menh_stars) if menh_stars else "Vô_Chính_Diệu"
        sig = f"{stars_str}_Mệnh_{menh_branch}_{cuc_name}".replace(" ", "_")
        return sig
    except Exception:
        return ""

def add_person(
    name: str,
    birth_dt: Optional[Union[str, datetime, date]] = None,
    gender: int = 1,
    birth_place: Optional[str] = None,
    relationship: Optional[str] = None,
    notes: Optional[str] = None,
    preferred_school: str = "standard",
    db_path: Optional[Union[str, Path]] = None
) -> int:
    """Add a new person profile to L5 memory."""
    if not name or not name.strip():
        raise ValueError("Name cannot be empty.")
    
    dt_obj = parse_dt(birth_dt)
    dt_str = dt_obj.isoformat() if dt_obj else (str(birth_dt) if birth_dt else None)
    
    bazi_sig = compute_bazi_signature(dt_obj, gender=gender) if dt_obj else None
    tuvi_sig = compute_tuvi_signature(dt_obj, gender=gender) if dt_obj else None
    
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO person_profiles (name, birth_dt, gender, birth_place, relationship, notes, preferred_school, bazi_signature, tuvi_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name.strip(), dt_str, gender, birth_place, relationship, notes, preferred_school, bazi_sig, tuvi_sig)
        )
        person_id = cursor.lastrowid
        conn.commit()
        return person_id
    finally:
        conn.close()

def get_person(person_id: int, db_path: Optional[Union[str, Path]] = None) -> Optional[Dict[str, Any]]:
    """Retrieve person profile by ID."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person_profiles WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def find_person(
    name: Optional[str] = None,
    birth_dt: Optional[Union[str, datetime, date]] = None,
    relationship: Optional[str] = None,
    db_path: Optional[Union[str, Path]] = None
) -> List[Dict[str, Any]]:
    """Search persons by name, birth date, or relationship."""
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        query = "SELECT * FROM person_profiles WHERE 1=1"
        params = []
        
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name.strip()}%")
        if birth_dt:
            dt_obj = parse_dt(birth_dt)
            if dt_obj:
                query += " AND birth_dt LIKE ?"
                params.append(f"{dt_obj.strftime('%Y-%m-%d')}%")
        if relationship:
            query += " AND relationship LIKE ?"
            params.append(f"%{relationship.strip()}%")
            
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()

def update_person(
    person_id: int,
    db_path: Optional[Union[str, Path]] = None,
    **kwargs
) -> bool:
    """Update arbitrary fields of a person profile."""
    if not kwargs:
        return False
        
    allowed_fields = {
        "name", "birth_dt", "gender", "birth_place", "relationship",
        "notes", "preferred_school", "bazi_signature", "tuvi_signature"
    }
    updates = []
    params = []
    
    # Check if birth_dt changed, recompute signatures
    if "birth_dt" in kwargs:
        dt_obj = parse_dt(kwargs["birth_dt"])
        gender = kwargs.get("gender", 1)
        kwargs["birth_dt"] = dt_obj.isoformat() if dt_obj else kwargs["birth_dt"]
        if "bazi_signature" not in kwargs and dt_obj:
            kwargs["bazi_signature"] = compute_bazi_signature(dt_obj, gender=gender)
        if "tuvi_signature" not in kwargs and dt_obj:
            kwargs["tuvi_signature"] = compute_tuvi_signature(dt_obj, gender=gender)

    for k, v in kwargs.items():
        if k in allowed_fields:
            updates.append(f"{k} = ?")
            params.append(v)
            
    if not updates:
        return False
        
    updates.append("updated_at = datetime('now', 'localtime')")
    params.append(person_id)
    
    conn = _get_connection(db_path)
    try:
        _ensure_schema(conn)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE person_profiles SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_or_create_person(
    name: str,
    birth_dt: Optional[Union[str, datetime, date]] = None,
    gender: int = 1,
    relationship: Optional[str] = None,
    notes: Optional[str] = None,
    preferred_school: str = "standard",
    db_path: Optional[Union[str, Path]] = None,
    **kwargs
) -> int:
    """Find person by name (and optionally birth_dt). If not found, create new."""
    existing = find_person(name=name, birth_dt=birth_dt, db_path=db_path)
    if existing:
        return existing[0]["id"]
    return add_person(
        name=name,
        birth_dt=birth_dt,
        gender=gender,
        relationship=relationship,
        notes=notes,
        preferred_school=preferred_school,
        db_path=db_path
    )
