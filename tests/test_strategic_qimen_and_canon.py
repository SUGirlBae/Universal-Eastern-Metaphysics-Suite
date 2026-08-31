import pytest
from datetime import datetime
from engine.ky_mon_strategic import calculate_strategic_qimen
from engine.classical_canon_rag import search_classical_canon, get_canonical_citation_for_reading

def test_strategic_qimen_structure():
    dt = datetime(2026, 8, 30, 13, 0)
    res = calculate_strategic_qimen(dt)
    
    assert "palaces" in res
    assert len(res["palaces"]) == 8 # 8 directions
    assert "strategic_highlights" in res
    assert "cầu_tài_đầu_tư" in res["strategic_highlights"]
    assert "công_danh_ký_kết" in res["strategic_highlights"]
    assert "cross_strategies" in res
    assert "tu_vi_action" in res["cross_strategies"]
    assert "iching_remedy" in res["cross_strategies"]

def test_classical_canon_rag_search():
    results = search_classical_canon("Dụng thần", limit=3)
    assert len(results) >= 1
    assert any("Bát Tự" in r["translation"] or "Dụng thần" in r["verse"] for r in results)
    
    tu_vi_results = search_classical_canon("Vũ Tham", discipline="tu_vi")
    assert len(tu_vi_results) >= 1
    assert tu_vi_results[0]["book"] == "Tử Vi Đẩu Số Toàn Thư"

def test_canonical_citations_for_reading():
    cites = get_canonical_citation_for_reading("tu_vi", ["cơ lương", "vũ tham"])
    assert len(cites) >= 1
    assert "Trần Đoàn" in cites[0]["author"]
