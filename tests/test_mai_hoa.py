import pytest
from datetime import datetime
from engine.lunar_solar import calculate_time_coordinates
from engine.mai_hoa import calculate_mai_hoa_from_time
from engine.luc_hao import calculate_full_luc_hao

def test_mai_hoa_calculation():
    dt = datetime(2026, 8, 29, 17, 36)
    time_coords = calculate_time_coordinates(dt)
    mh = calculate_mai_hoa_from_time(time_coords)
    lh = calculate_full_luc_hao(mh, time_coords)
    
    assert mh["moving_line"] in range(1, 7)
    assert len(lh["hex_symbol"]) > 0
    assert len(lh["lines"]) == 6
    assert lh["the_line"] in range(1, 7)
    assert lh["ung_line"] in range(1, 7)
