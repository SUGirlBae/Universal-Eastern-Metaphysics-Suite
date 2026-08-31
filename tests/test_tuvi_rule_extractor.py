import pytest
import sqlite3
from pathlib import Path
from engine.tuvi_rule_extractor import (
    init_rules_db,
    parse_chart_html,
    search_tuvi_rules,
    get_rules_stats
)

def test_tuvi_rules_db_init_and_search(tmp_path):
    test_db = tmp_path / "test_rules.db"
    init_rules_db(test_db)
    
    conn = sqlite3.connect(str(test_db))
    c = conn.cursor()
    c.execute("""
        INSERT INTO tuvi_rules (trigger_text, palace_scope, rule_type, content, source_book, author, accuracy_score, hash_key)
        VALUES ('Cung Mệnh có sao Thái dương', 'CUNG MỆNH', 'chinh_tinh', 'Chủ về thông minh, khẳng khái, nhiệt tình', 'Trung Châu tử vi đẩu số', 'Nguyễn Anh Vũ', 0.9, 'key1')
    """)
    conn.commit()
    conn.close()

    results = search_tuvi_rules("Thái dương", db_path=test_db)
    assert len(results) >= 1
    assert "Thái dương" in results[0]["trigger_text"]
    assert results[0]["accuracy_score"] == 0.9

    stats = get_rules_stats(test_db)
    assert stats["total_rules"] == 1
    assert stats["top_sources"]["Trung Châu tử vi đẩu số"] == 1

def test_production_rules_db_has_data():
    stats = get_rules_stats()
    # If production DB exists, ensure it has extracted rules
    if stats["total_rules"] > 0:
        assert stats["total_rules"] >= 1000
        assert "to_hop_sao" in stats["by_type"]
        assert "phi_tinh" in stats["by_type"]
