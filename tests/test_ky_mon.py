import pytest
from datetime import datetime
from engine.ky_mon_engine import calculate_ky_mon_chart, calculate_ky_mon, format_ky_mon_report
from engine.ky_mon_strategic import calculate_strategic_qimen

def test_ky_mon_calculation():
    dt = datetime(2025, 6, 20, 10, 0)
    res = calculate_ky_mon(dt)
    assert "dun_type" in res
    assert len(res["palaces"]) == 9
    assert len(res["auspicious_patterns"]) >= 1

def test_ky_mon_chart_canonical_structure():
    dt_winter = datetime(2026, 1, 15, 10, 0) # Duong Don
    chart_winter = calculate_ky_mon_chart(dt_winter)
    assert chart_winter["don_type"] == "Duong"
    assert "lead_star" in chart_winter
    assert "lead_gate" in chart_winter
    assert "tuan_thu" in chart_winter
    assert len(chart_winter["palaces"]) == 9
    
    # Check that each palace has all 4 layers (di_ban, thien_ban, gate, star, spirit)
    for pid in range(1, 10):
        p = chart_winter["palaces"][pid]
        assert "di_ban" in p
        assert "thien_ban" in p
        assert "star" in p
        assert "gate" in p
        assert "spirit" in p

    dt_summer = datetime(2026, 7, 15, 10, 0) # Am Don
    chart_summer = calculate_ky_mon_chart(dt_summer)
    assert chart_summer["don_type"] == "Am"

def test_ky_mon_strategic_integration():
    dt = datetime(2026, 8, 30, 14, 30)
    strat = calculate_strategic_qimen(dt)
    assert "strategic_highlights" in strat
    assert "cầu_tài_đầu_tư" in strat["strategic_highlights"]
    assert "công_danh_ký_kết" in strat["strategic_highlights"]
    assert "cross_strategies" in strat
    assert len(strat["palaces"]) == 8

def test_ky_mon_report_formatting():
    dt = datetime(2026, 8, 30, 14, 30)
    chart = calculate_ky_mon_chart(dt)
    rep = format_ky_mon_report(chart)
    assert "KỲ MÔN ĐỘN GIÁP" in rep
    assert "Thiên Bàn / Nghi" in rep
    assert "Cửu Tinh" in rep
    assert "Bát Môn" in rep
    assert "Bát Thần" in rep
