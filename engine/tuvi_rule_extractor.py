"""
Tu Vi Co Hoc Canonical Rule Extractor & Database Builder
Extracts structured multi-school rules (nguyennhan, ketqua, thamkhao, chinhxac)
from canonical-ziwei-archive.internal and stores them in an offline SQLite database.
"""
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

DEFAULT_RULES_DB = Path(__file__).resolve().parent.parent / "data" / "tuvi_canonical_rules.db"

def init_rules_db(db_path: Optional[Path] = None) -> Path:
    """Initialize the SQLite database for extracted Tử Vi rules."""
    db_path = db_path or DEFAULT_RULES_DB
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS tuvi_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger_text TEXT NOT NULL,
            palace_scope TEXT,           -- CUNG MỆNH, CUNG THÂN, etc.
            rule_type TEXT,              -- chinh_tinh, phu_tinh, tam_hop, phi_tinh, tu_hoa, etc.
            content TEXT NOT NULL,
            source_book TEXT,            -- Tên sách
            author TEXT,                 -- Tác giả / Dịch giả
            accuracy_score REAL,         -- 0.1 - 1.0 (from chinhxac-X)
            hash_key TEXT UNIQUE,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
    
    c.execute("CREATE INDEX IF NOT EXISTS idx_trigger ON tuvi_rules(trigger_text)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_palace ON tuvi_rules(palace_scope)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_source ON tuvi_rules(source_book)")
    
    # FTS5 table for fast semantic lookup of rules
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS tuvi_rules_fts USING fts5(
            trigger_text,
            content,
            source_book,
            content='tuvi_rules',
            content_rowid='id',
            tokenize='unicode61'
        )
    """)
    
    c.execute("""
        CREATE TRIGGER IF NOT EXISTS tuvi_rules_ai AFTER INSERT ON tuvi_rules BEGIN
            INSERT INTO tuvi_rules_fts(rowid, trigger_text, content, source_book)
            VALUES (new.id, new.trigger_text, new.content, new.source_book);
        END
    """)
    
    conn.commit()
    conn.close()
    return db_path

def parse_chart_html(html_content: str, db_path: Optional[Path] = None) -> Dict[str, Any]:
    """Parse all rule blocks from a Co Hoc chart HTML page."""
    db_path = init_rules_db(db_path)
    soup = BeautifulSoup(html_content, "html.parser")
    
    vung = soup.find("div", class_="vung-giai-doan")
    if not vung:
        return {"total_found": 0, "inserted": 0, "duplicates": 0}
        
    noi_dung = vung.find("div", class_="noi-dung") or vung
    
    current_palace = "TỔNG QUAN"
    
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    
    inserted = 0
    duplicates = 0
    
    for element in noi_dung.find_all(["h3", "div"]):
        if element.name == "h3" and "giaidoan-cung" in element.get("class", []):
            current_palace = element.get_text().strip()
            continue
            
        if element.name == "div" and "giaidoan" in element.get("class", []):
            # Extract accuracy score from class (e.g. chinhxac-9 -> 0.9)
            classes = element.get("class", [])
            acc = 0.7
            for cls in classes:
                m = re.search(r"chinhxac-(\d+)", cls)
                if m:
                    acc = int(m.group(1)) / 10.0
                    break
                    
            # Extract trigger
            h4 = element.find("h4", class_="nguyennhan")
            trigger = h4.get_text().strip() if h4 else ""
            if not trigger:
                continue
                
            # Extract content
            p = element.find("p", class_="ketqua")
            content = p.get_text("\n").strip() if p else ""
            if not content:
                continue
                
            # Extract source
            em = element.find("em", class_="thamkhao")
            raw_source = em.get_text().strip() if em else "Kinh nghiệm cổ truyền"
            
            # Split book and author if separated by "-"
            parts = [pt.strip() for pt in raw_source.split("-")]
            book = parts[0] if parts else raw_source
            author = " - ".join(parts[1:]) if len(parts) > 1 else ""
            
            # Classify rule type
            rule_type = "general"
            if "phi Hóa" in trigger:
                rule_type = "phi_tinh"
            elif "tự Hóa" in trigger:
                rule_type = "tu_hoa"
            elif "Tam hợp" in trigger:
                rule_type = "tam_hop"
            elif "hội hợp" in trigger or "đồng cung" in trigger:
                rule_type = "to_hop_sao"
            elif "Lai Nhân" in trigger:
                rule_type = "lai_nhan_cung"
            elif "Đại Vận" in current_palace or "VẬN NĂM" in current_palace:
                rule_type = "van_han"
                
            hash_key = f"{trigger}|{content[:50]}|{raw_source}"
            
            try:
                c.execute("""
                    INSERT INTO tuvi_rules (trigger_text, palace_scope, rule_type, content, source_book, author, accuracy_score, hash_key)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (trigger, current_palace, rule_type, content, book, author, acc, hash_key))
                inserted += 1
            except sqlite3.IntegrityError:
                duplicates += 1
                
    conn.commit()
    conn.close()
    
    return {"total_found": inserted + duplicates, "inserted": inserted, "duplicates": duplicates}

def search_tuvi_rules(query: str, palace: Optional[str] = None, limit: int = 5, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Search extracted Tử Vi rules via FTS5."""
    db_path = db_path or DEFAULT_RULES_DB
    if not db_path.exists():
        return []
        
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    sql = """
        SELECT r.id, r.trigger_text, r.palace_scope, r.rule_type, r.content,
               r.source_book, r.author, r.accuracy_score
        FROM tuvi_rules_fts
        JOIN tuvi_rules r ON tuvi_rules_fts.rowid = r.id
        WHERE tuvi_rules_fts MATCH ?
    """
    params = [query]
    if palace:
        sql += " AND r.palace_scope LIKE ?"
        params.append(f"%{palace}%")
        
    sql += " ORDER BY r.accuracy_score DESC LIMIT ?"
    params.append(limit)
    
    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()
    
    return [dict(r) for r in rows]

def get_rules_stats(db_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get statistics about the extracted Tử Vi rules database."""
    db_path = db_path or DEFAULT_RULES_DB
    if not db_path.exists():
        return {"total_rules": 0}
        
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tuvi_rules")
    total = c.fetchone()[0]
    
    c.execute("SELECT rule_type, COUNT(*) FROM tuvi_rules GROUP BY rule_type ORDER BY COUNT(*) DESC")
    by_type = {r[0]: r[1] for r in c.fetchall()}
    
    c.execute("SELECT source_book, COUNT(*) FROM tuvi_rules GROUP BY source_book ORDER BY COUNT(*) DESC LIMIT 10")
    by_source = {r[0]: r[1] for r in c.fetchall()}
    
    conn.close()
    return {"total_rules": total, "by_type": by_type, "top_sources": by_source}

query_tuvi_rules = search_tuvi_rules

