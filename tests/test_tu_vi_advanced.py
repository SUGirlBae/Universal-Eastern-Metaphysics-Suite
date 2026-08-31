import pytest
from datetime import datetime
from engine.tu_vi_advanced import calculate_universal_tu_vi, format_universal_tu_vi_report

def test_universal_tu_vi_schools():
    dt = datetime(1999, 12, 6, 1, 55)
    
    # 1. Standard / Khâm Thiên
    res_kt = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")
    assert res_kt["school"] == "kham_thien"
    assert res_kt["client_profile"]["cuc_name"] == "Hỏa Lục Cục"
    assert res_kt["client_profile"]["menh_branch"] == "Tuất"
    assert res_kt["client_profile"]["than_branch"] == "Tý"
    assert len(res_kt["palaces"]) == 12
    
    # Verify Cung Thân / Phúc Đức has Đồng Âm
    phuc_palace = next(p for p in res_kt["palaces"] if p["branch_name"] == "Tý")
    assert "Thiên Đồng" in phuc_palace["main_stars"]
    assert "Thái Âm" in phuc_palace["main_stars"]
    
    # 2. Trung Châu Phái
    res_tc = calculate_universal_tu_vi(dt, gender=1, school="trung_chau")
    assert res_tc["school"] == "trung_chau"
    
    # 3. Nam Phái with 110+ stars
    res_np = calculate_universal_tu_vi(dt, gender=1, school="nam_phai")
    all_minor_names = []
    for p in res_np["palaces"]:
        all_minor_names.extend([s["name"] for s in p["minor_stars"]])
    assert "Tả Phụ" in all_minor_names
    assert "Hữu Bật" in all_minor_names
    assert "Kình Dương" in all_minor_names
    assert "Đà La" in all_minor_names
    assert "Lộc Tồn" in all_minor_names
    assert "Thái Tuế" in all_minor_names
    assert "Trường Sinh" in all_minor_names

def test_flying_stars_and_self_transformations():
    dt = datetime(1999, 12, 6, 1, 55)
    res = calculate_universal_tu_vi(dt, gender=1, school="kham_thien")
    flying = res["flying_stars"]["palace_flying_stars"]
    assert len(flying) == 12
    
    # Cung Phúc Bính Tý tự hóa Lộc (Thiên Đồng)
    phuc_f = next(f for f in flying if f["branch_name"] == "Tý")
    assert any("Tự hóa Lộc" in st for st in phuc_f["self_transformations"])

def test_dia_ban_astrolabe():
    dt = datetime(1999, 12, 6, 1, 55)
    res_dia = calculate_universal_tu_vi(dt, gender=1, astrolabe_type="dia_ban")
    assert res_dia["astrolabe_type"] == "dia_ban"
    # In Địa Bàn, Mệnh index is shifted to Thân index (Tý)
    menh_p = next(p for p in res_dia["palaces"] if p["is_menh"])
    assert menh_p["branch_name"] == "Tý"

def test_performance_sub_5ms():
    import time
    dt = datetime(1999, 12, 6, 1, 55)
    t0 = time.perf_counter()
    for _ in range(50):
        calculate_universal_tu_vi(dt, gender=1, school="kham_thien")
    dur = (time.perf_counter() - t0) / 50
    assert dur < 0.005 # strictly sub 5ms
