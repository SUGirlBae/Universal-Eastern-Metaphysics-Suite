import pytest
from datetime import datetime
from engine.ha_lac_engine import calculate_ha_lac, format_ha_lac_report, reduce_ha_lac_num

def test_ha_lac_basic_calculation():
    dt = datetime(2025, 6, 20, 10, 0)
    res = calculate_ha_lac(dt, gender=1)
    
    assert "tien_thien" in res
    assert "hau_thien" in res
    assert "thien_so" in res
    assert "dia_so" in res
    assert "nguyen_khi_hao" in res
    assert "hoa_cong_hao" in res
    assert "dai_van_timeline" in res
    assert "annual_lines" in res
    assert len(res["annual_lines"]) == 100
    assert len(res["dai_van_timeline"]) >= 6
    assert 1 <= res["nguyen_khi_hao"] <= 6
    assert 1 <= res["hoa_cong_hao"] <= 6

def test_ha_lac_gender_polarity_and_center_five_rule():
    # Test Palace 5 reduction rule
    # Duong Nam / Am Nu: Heaven 5 -> 7 (Cấn), Earth 5 -> 8 (Khôn)
    assert reduce_ha_lac_num(5, is_heaven=True, is_duong_nam_or_am_nu=True) == 7
    assert reduce_ha_lac_num(5, is_heaven=False, is_duong_nam_or_am_nu=True) == 8
    
    # Am Nam / Duong Nu: Heaven 5 -> 8 (Khôn), Earth 5 -> 7 (Cấn)
    assert reduce_ha_lac_num(5, is_heaven=True, is_duong_nam_or_am_nu=False) == 8
    assert reduce_ha_lac_num(5, is_heaven=False, is_duong_nam_or_am_nu=False) == 7

def test_ha_lac_report_formatting():
    dt = datetime(1990, 2, 4, 6, 0)
    res = calculate_ha_lac(dt, gender=1)
    rep = format_ha_lac_report(res)
    assert "BÁT TỰ HÀ LẠC" in rep
    assert "QUẺ TIÊN THIÊN" in rep
    assert "QUẺ HẬU THIÊN" in rep
    assert "Hào Nguyên Khí" in rep
    assert "Hào Hóa Công" in rep
