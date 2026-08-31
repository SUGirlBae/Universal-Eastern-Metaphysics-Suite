import pytest
from datetime import datetime
from engine.annual_forecast import (
    calculate_annual_forecast,
    format_annual_forecast_report,
    get_year_canchi,
    YEAR_CAN_TU_HOA
)

def test_annual_forecast_basic():
    res = calculate_annual_forecast(2026, question="Kinh doanh tài chính")
    assert res["target_year"] == 2026
    assert res["year_canchi"] == "Bính Ngọ"
    assert res["thai_tue_palace"] == "Cung Ngọ"
    assert len(res["six_lines_forecast"]) == 6
    assert "iching_annual_hex" in res
    assert "luu_tu_hoa" in res
    assert "qimen_annual_guidance" in res

def test_annual_forecast_with_birth_dt():
    birth = datetime(1990, 2, 4, 6, 0)
    res = calculate_annual_forecast(birth, target_year=2026, gender=1, question="Định hướng sự nghiệp")
    assert res["target_year"] == 2026
    assert res["ha_lac_annual"] is not None
    assert "active_hex" in res["ha_lac_annual"]
    assert "active_line" in res["ha_lac_annual"]

def test_year_canchi_conversion():
    can, chi = get_year_canchi(2024)
    assert f"{can} {chi}" == "Giáp Thìn"
    can, chi = get_year_canchi(2026)
    assert f"{can} {chi}" == "Bính Ngọ"

def test_annual_forecast_report_formatting():
    res = calculate_annual_forecast(2026, question="Vận trình tổng thể")
    rep = format_annual_forecast_report(res)
    assert "BÁO CÁO DỰ BÁO THỜI VẬN 12 THÁNG" in rep
    assert "QUẺ CHIÊM NIÊN VẬN 12 THÁNG" in rep
    assert "LƯU TỨ HÓA" in rep
    assert "KỲ MÔN ĐỘN GIÁP" in rep
