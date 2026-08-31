import pytest
from datetime import datetime
from engine.bazi_engine import calculate_bazi

def test_bazi_sample_profile():
    dt = datetime(2025, 6, 20, 10, 0)
    res = calculate_bazi(dt, gender=1)
    
    assert res["pillars"]["year"]["can_chi"] == "Ất Tỵ"
    assert res["pillars"]["month"]["can_chi"] == "Nhâm Ngọ"
    assert res["pillars"]["day"]["can_chi"] == "Canh Thân"
    assert res["pillars"]["time"]["can_chi"] == "Tân Tỵ"
    assert res["day_master"]["can"] == "Canh"
    assert len(res["dayun_list"]) >= 8
