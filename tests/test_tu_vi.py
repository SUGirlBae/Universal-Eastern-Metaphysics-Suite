import pytest
from datetime import datetime
from engine.tu_vi_engine import calculate_tu_vi_chart

def test_tu_vi_calculation():
    dt = datetime(2025, 6, 20, 10, 0)
    res = calculate_tu_vi_chart(dt, gender=1)
    assert len(res["palaces"]) == 12
    assert "cuc_name" in res
    assert "four_transformations" in res
