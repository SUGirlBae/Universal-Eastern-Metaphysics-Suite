import pytest
from datetime import datetime
from engine.timing_almanac import (
    calculate_timing_almanac,
    scan_target_timing_dates,
    calculate_luc_dieu,
    format_timing_almanac_report
)

def test_timing_scan():
    dt = datetime(2026, 8, 30, 2, 0)
    dates = scan_target_timing_dates(dt, ["Dậu", "Thìn"], days_limit=45)
    assert len(dates) >= 1
    assert "day_can_chi" in dates[0]
    assert "truc" in dates[0]
    assert "hoang_dao" in dates[0]
    assert "luc_dieu" in dates[0]

def test_calculate_timing_almanac():
    dt = datetime(2026, 8, 30, 14, 30)
    res = calculate_timing_almanac(dt)
    assert "truc_12" in res
    assert "tu_28" in res
    assert "luc_dieu" in res
    assert "hoang_dao_than" in res
    assert isinstance(res["is_hoang_dao"], bool)
    assert "auspicious_activities" in res
    assert "taboo_activities" in res

def test_luc_dieu_calculation():
    # Month 1, Day 1 -> Đại An
    assert "Đại An" in calculate_luc_dieu(1, 1)
    # Month 1, Day 2 -> Lưu Niên
    assert "Lưu Niên" in calculate_luc_dieu(1, 2)
    # Month 1, Day 3 -> Tốc Hỷ
    assert "Tốc Hỷ" in calculate_luc_dieu(1, 3)

def test_timing_almanac_report_formatting():
    dt = datetime(2026, 8, 30, 14, 30)
    dates = scan_target_timing_dates(dt, ["Tý", "Ngọ"], days_limit=30)
    rep = format_timing_almanac_report(dates, context_reason="Khởi công xây dựng")
    assert "TRẠCH CÁT HOÀNG ĐẠO" in rep
    assert "Dương Lịch" in rep
    assert "Âm Lịch" in rep
