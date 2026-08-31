import pytest
from datetime import datetime
from engine.synthesis_engine import run_master_synthesis
from engine.knowledge_graph import analyze_wuxing_interaction, analyze_branch_pair

def test_master_synthesis():
    dt = datetime(2025, 6, 20, 10, 0)
    res = run_master_synthesis(dt, question="Kiểm thử đại tổng hợp", gender=1)
    
    assert "i_ching" in res
    assert "bazi" in res
    assert "tu_vi" in res
    assert "ha_lac" in res
    assert "ky_mon" in res
    assert len(res["synthesis_insights"]) >= 3

def test_knowledge_graph():
    rel = analyze_wuxing_interaction("Kim", "Thủy")
    assert "Sinh Xuất" in rel
    
    branch_rel = analyze_branch_pair("Tý", "Sửu")
    assert any("Lục Hợp" in b for b in branch_rel)
