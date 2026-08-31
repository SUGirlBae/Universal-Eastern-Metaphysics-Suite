import pytest
from engine.coin_toss import parse_coin_values, calculate_coin_luc_hao

def test_coin_toss_all_yang():
    pri, trans, dong = parse_coin_values([9, 9, 9, 9, 9, 9])
    assert pri == (1, 1) # Bát Thuần Càn
    assert trans == (8, 8) # Bát Thuần Khôn
    assert dong == [1, 2, 3, 4, 5, 6]

def test_coin_toss_static():
    pri, trans, dong = parse_coin_values([7, 8, 7, 8, 7, 8])
    assert dong == []
    res = calculate_coin_luc_hao([7, 8, 7, 8, 7, 8])
    assert len(res["lines"]) == 6
    assert res["moving_lines"] == []
