import pytest
from engine.feng_shui import (
    calculate_flying_stars_period9,
    calculate_feng_shui_period9,
    format_feng_shui_report,
    degree_to_mountain,
    fly_stars
)

def test_degree_to_mountain_conversion():
    assert degree_to_mountain(0.0) == "Tý"
    assert degree_to_mountain(180.0) == "Ngọ"
    assert degree_to_mountain(90.0) == "Mão"
    assert degree_to_mountain(270.0) == "Dậu"

def test_flying_stars_period9_canonical_chart():
    # Tọa Ngọ Hướng Tý
    res = calculate_flying_stars_period9("Tý", birth_year=1990, gender=1)
    assert res["period_number"] == 9
    assert res["facing"] == "Tý"
    assert res["sitting"] == "Ngọ"
    assert res["facing_palace"] == "Khảm"
    assert res["sitting_palace"] == "Ly"
    assert len(res["palaces_grid"]) == 9
    assert "five_yellow_remedy" in res
    assert "two_black_remedy" in res
    assert "special_formations" in res
    assert res["cung_phi_personal"]["group"] == "Đông Tứ Mệnh"

def test_flying_stars_by_numeric_degree():
    # Facing 180 degrees (Facing Ngọ, Sitting Tý)
    res = calculate_flying_stars_period9(180.0, birth_year=1985, gender=0)
    assert res["facing"] == "Ngọ"
    assert res["sitting"] == "Tý"
    assert res["cung_phi_personal"]["group"] == "Đông Tứ Mệnh"

def test_feng_shui_report_formatting():
    res = calculate_flying_stars_period9("Càn", birth_year=1995, gender=1)
    rep = format_feng_shui_report(res)
    assert "HUYỀN KHÔNG PHI TINH VẬN 9" in rep
    assert "TINH BÀN HUYỀN KHÔNG 9 CUNG" in rep
    assert "HÓA GIẢI SÁT TINH" in rep
