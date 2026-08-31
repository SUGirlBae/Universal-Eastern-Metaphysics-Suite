import pytest
from datetime import datetime
from engine.dan_dao_health import (
    calculate_dan_dao_health,
    diagnose_dan_dao_health,
    format_dan_dao_health_report,
    get_current_meridian_hour,
    TICH_QUAI_12,
    ZANG_FU_MAP
)

def test_dan_dao_health_calculation():
    dt = datetime(2005, 3, 26, 4, 30)
    res = calculate_dan_dao_health(dt, gender=1)
    
    assert "tich_quai" in res
    assert "tiet_khi" in res
    assert "ty_ngo_luu_chu" in res
    assert "luc_tu_quyet" in res
    assert "dan_hoa_quy_nguyen" in res
    assert "organ_diagnosis" in res
    assert "element_balance" in res
    assert "excess_organ" in res
    assert "deficient_organ" in res
    assert "alchemy_guidance" in res

def test_tich_quai_12_coverage():
    # Verify all 12 lunar months have valid Hexagram and advice
    for month in range(1, 13):
        assert month in TICH_QUAI_12
        assert "hex_name" in TICH_QUAI_12[month]
        assert "advice" in TICH_QUAI_12[month]

def test_ty_ngo_luu_chu_hours():
    key_ty, m_ty = get_current_meridian_hour(23)
    assert "Đởm Kinh" in m_ty["meridian"]
    
    key_ngo, m_ngo = get_current_meridian_hour(12)
    assert "Tâm Kinh" in m_ngo["meridian"]

def test_dan_dao_health_report_formatting():
    dt = datetime(1990, 2, 4, 6, 0)
    res = diagnose_dan_dao_health(dt, gender=1)
    rep = format_dan_dao_health_report(res)
    assert "CHẨN ĐOÁN KHÍ CƠ TẠNG PHỦ" in rep
    assert "Tham Đồng Khế 12 Tịch Quái" in rep
    assert "TÝ NGỌ LƯU CHÚ" in rep
    assert "Lục Tự Quyết" in rep
