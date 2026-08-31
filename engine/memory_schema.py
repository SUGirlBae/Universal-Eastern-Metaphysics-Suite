"""
Memory Schema & Migration Engine for Eastern Metaphysics Suite
Supports L0-L5 Multi-Layer Cognitive Memory:
- L5: person_profiles
- L4: patterns, pattern_cases, distilled_rules
- L3: cases, predictions, outcomes
"""

import sqlite3
from typing import Optional, Union
from pathlib import Path

MEMORY_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS person_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_dt TEXT,
    gender INTEGER DEFAULT 1,
    birth_place TEXT,
    relationship TEXT,
    notes TEXT,
    preferred_school TEXT DEFAULT 'standard',
    bazi_signature TEXT,
    tuvi_signature TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_signature TEXT NOT NULL UNIQUE,
    pattern_type TEXT DEFAULT 'single',
    discipline_scope TEXT,
    description TEXT,
    dao_root TEXT,
    canon_refs TEXT,
    confidence REAL DEFAULT 0.0,
    support_count INTEGER DEFAULT 0,
    contradict_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'draft',
    valid_from TEXT,
    valid_until TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS pattern_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    is_supporting INTEGER DEFAULT 1,
    reason TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (pattern_id) REFERENCES patterns(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE,
    UNIQUE(pattern_id, case_id)
);

CREATE INDEX IF NOT EXISTS idx_person_name ON person_profiles(name);
CREATE INDEX IF NOT EXISTS idx_person_bazi ON person_profiles(bazi_signature);
CREATE INDEX IF NOT EXISTS idx_patterns_sig ON patterns(pattern_signature);
CREATE INDEX IF NOT EXISTS idx_patterns_status ON patterns(status);
CREATE INDEX IF NOT EXISTS idx_patterns_confidence ON patterns(confidence);
CREATE INDEX IF NOT EXISTS idx_pattern_cases_pat ON pattern_cases(pattern_id);
CREATE INDEX IF NOT EXISTS idx_pattern_cases_case ON pattern_cases(case_id);
"""

def migrate_schema(conn: sqlite3.Connection) -> None:
    """Apply memory schema and perform non-breaking migrations."""
    conn.executescript(MEMORY_SCHEMA_SQL)
    
    cursor = conn.cursor()
    
    # 1. Check if person_id column exists in cases table
    cursor.execute("PRAGMA table_info(cases)")
    case_cols = [row[1] for row in cursor.fetchall()]
    if "person_id" not in case_cols:
        cursor.execute("ALTER TABLE cases ADD COLUMN person_id INTEGER REFERENCES person_profiles(id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cases_person ON cases(person_id)")
        
    # 2. Check if preferred_school column exists in person_profiles table
    cursor.execute("PRAGMA table_info(person_profiles)")
    person_cols = [row[1] for row in cursor.fetchall()]
    if "preferred_school" not in person_cols:
        cursor.execute("ALTER TABLE person_profiles ADD COLUMN preferred_school TEXT DEFAULT 'standard'")
        
    conn.commit()
