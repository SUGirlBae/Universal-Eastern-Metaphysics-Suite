import pytest
from datetime import datetime
from engine.cross_matrix import cross_health_iching_synthesis, cross_feng_shui_iching_synthesis, format_cross_health_report, format_cross_feng_shui_report

def test_cross_health_iching():
    dt = datetime(2005, 3, 26, 4, 30)
    res = cross_health_iching_synthesis(dt, gender=1, question="Đau mỏi vai gáy")
    assert res["type"] == "Y_DICH_DONG_NGUYEN"
    assert "constitutional_zang_fu" in res
    assert "iching_dynamic_scan" in res
    rep = format_cross_health_report(res)
    assert "Y DỊCH ĐỒNG NGUYÊN" in rep

def test_cross_feng_shui_iching():
    res = cross_feng_shui_iching_synthesis(facing_mountain="Tý", birth_year=1990, question="Khảo sát phòng khách")
    assert res["type"] == "DUONG_TRACH_DONG_THAI"
    assert res["facing"] == "Tý"
    assert "spatial_period9_matrix" in res
    assert "iching_spatial_scan" in res
    rep = format_cross_feng_shui_report(res)
    assert "DƯƠNG TRẠCH ĐỘNG THÁI" in rep
