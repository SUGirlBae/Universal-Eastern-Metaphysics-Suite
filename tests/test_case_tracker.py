"""
Tests for Case Tracker Database Module
Eastern Metaphysics All-In-One Engine
"""

import pytest
import sqlite3
import json
from datetime import datetime, date, timedelta
from pathlib import Path

from engine.case_tracker import (
    init_db,
    add_case,
    add_prediction,
    verify_prediction,
    get_case,
    list_cases,
    get_accuracy_report,
    get_unverified_predictions,
    delete_case,
    DEFAULT_DB_PATH
)


@pytest.fixture
def temp_db(tmp_path):
    """Fixture providing an isolated temporary SQLite database path."""
    db_file = tmp_path / "test_case_tracker.db"
    init_db(db_file)
    return db_file


def test_init_db(tmp_path):
    """Test database initialization and schema creation."""
    db_file = tmp_path / "init_test.db"
    res_path = init_db(db_file)
    
    assert Path(res_path).exists()
    
    # Verify tables exist
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    assert "cases" in tables
    assert "predictions" in tables
    assert "outcomes" in tables


def test_add_case(temp_db):
    """Test adding various case types with structured chart summary."""
    birth_dt = datetime(1990, 5, 15, 8, 30)
    chart_data = {
        "bazi": {"day_master": "Giáp Mộc", "month_branch": "Tỵ"},
        "tu_vi": {"cuc": "Mộc Tam Cục", "menh_palace": "Thìn"}
    }
    
    case_id = add_case(
        birth_dt=birth_dt,
        gender=1,
        question="Sự nghiệp và tài lộc năm 2026",
        discipline="tu_vi",
        chart_summary=chart_data,
        interpretation="Mệnh Vũ Khúc Hóa Lộc, đại vận thuận lợi cho khởi nghiệp công nghệ.",
        db_path=temp_db
    )
    
    assert isinstance(case_id, int)
    assert case_id > 0
    
    # Verify retrieval
    case = get_case(case_id, db_path=temp_db)
    assert case is not None
    assert case["id"] == case_id
    assert case["gender"] == 1
    assert case["discipline"] == "tu_vi"
    assert case["question"] == "Sự nghiệp và tài lộc năm 2026"
    assert case["chart_summary_parsed"]["bazi"]["day_master"] == "Giáp Mộc"
    assert "Vũ Khúc Hóa Lộc" in case["interpretation"]
    assert case["predictions"] == []


def test_add_prediction(temp_db):
    """Test adding testable predictions to a case."""
    case_id = add_case(
        birth_dt="1988-11-20T14:00:00",
        gender=0,
        question="Hôn nhân và gia đạo",
        discipline="kinh_dich",
        chart_summary={"hexagram": "Phong Lôi Ích", "moving_line": 2},
        interpretation="Quẻ Ích biến Phong Trạch Trung Phu, tin vui hôn nhân vào cuối năm.",
        db_path=temp_db
    )
    
    pred_id = add_prediction(
        case_id=case_id,
        prediction_text="Kết hôn hoặc đính hôn vào quý 4/2026",
        timeframe="2026 Q4",
        confidence=0.85,
        category="relationship",
        db_path=temp_db
    )
    
    assert isinstance(pred_id, int)
    assert pred_id > 0
    
    # Verify non-existent case raises error
    with pytest.raises(ValueError, match="Case ID 99999 does not exist"):
        add_prediction(
            case_id=99999,
            prediction_text="Invalid case test",
            db_path=temp_db
        )
        
    # Verify empty prediction raises error
    with pytest.raises(ValueError, match="prediction_text must not be empty"):
        add_prediction(
            case_id=case_id,
            prediction_text="",
            db_path=temp_db
        )


def test_verify_prediction(temp_db):
    """Test recording real-world outcomes and calculating accuracy."""
    case_id = add_case(
        question="Đầu tư bất động sản",
        discipline="ky_mon",
        interpretation="Trực Sử Sinh Môn đáo Cấn, lợi nhuận lớn vào mùa Thu.",
        db_path=temp_db
    )
    
    pred_id = add_prediction(
        case_id=case_id,
        prediction_text="Chốt lời bất động sản thành công trong tháng 8 âm lịch",
        timeframe="Tháng 8 ÂL 2026",
        confidence=0.75,
        category="wealth",
        db_path=temp_db
    )
    
    outcome_id = verify_prediction(
        prediction_id=pred_id,
        actual_result="Bán nhà thành công tháng 8 ÂL với lợi nhuận 25%",
        accuracy_score=0.95,
        notes="Đúng thời điểm và đúng hướng Đông Bắc như dự báo.",
        db_path=temp_db
    )
    
    assert isinstance(outcome_id, int)
    assert outcome_id > 0
    
    # Check case retrieval reflects verified outcome
    case = get_case(case_id, db_path=temp_db)
    assert len(case["predictions"]) == 1
    pred = case["predictions"][0]
    assert pred["outcome"] is not None
    assert pred["outcome"]["accuracy_score"] == 0.95
    assert "25%" in pred["outcome"]["actual_result"]
    assert pred["outcome"]["notes"] == "Đúng thời điểm và đúng hướng Đông Bắc như dự báo."


def test_get_accuracy_report(temp_db):
    """Test generating statistics and accuracy reports by discipline and category."""
    # Case 1: Tu Vi (Career)
    c1 = add_case(discipline="tu_vi", question="Thăng tiến công việc", db_path=temp_db)
    p1 = add_prediction(c1, "Được đề bạt làm giám đốc khối Q2", category="career", confidence=0.8, db_path=temp_db)
    verify_prediction(p1, "Chính thức bổ nhiệm chức danh Director vào tháng 5", accuracy_score=1.0, db_path=temp_db)
    
    # Case 2: Tu Vi (Wealth)
    p2 = add_prediction(c1, "Thu nhập tăng gấp đôi", category="wealth", confidence=0.6, db_path=temp_db)
    verify_prediction(p2, "Thu nhập tăng 40%", accuracy_score=0.6, db_path=temp_db)
    
    # Case 3: Kinh Dich (Health)
    c2 = add_case(discipline="kinh_dich", question="Sức khỏe hồi phục", db_path=temp_db)
    p3 = add_prediction(c2, "Khỏi bệnh sau tiết Lập Thu", category="health", confidence=0.7, db_path=temp_db)
    verify_prediction(p3, "Hồi phục hoàn toàn sau Lập Thu 3 ngày", accuracy_score=0.9, db_path=temp_db)
    
    # Case 4: Unverified prediction
    p4 = add_prediction(c2, "Đi du lịch nước ngoài vào mùa đông", category="other", confidence=0.5, db_path=temp_db)
    
    # Global report
    report_all = get_accuracy_report(db_path=temp_db)
    assert report_all["total_cases"] == 2
    assert report_all["total_predictions"] == 4
    assert report_all["verified_predictions"] == 3
    assert report_all["unverified_predictions"] == 1
    assert report_all["verification_rate"] == 0.75
    # (1.0 + 0.6 + 0.9) / 3 = 0.8333
    assert pytest.approx(report_all["avg_accuracy"], 0.01) == 0.8333
    
    # Check category breakdown
    assert "career" in report_all["by_category"]
    assert report_all["by_category"]["career"]["avg_accuracy"] == 1.0
    assert report_all["by_category"]["career"]["verified"] == 1
    assert report_all["by_category"]["wealth"]["avg_accuracy"] == 0.6
    assert report_all["by_category"]["health"]["avg_accuracy"] == 0.9
    assert report_all["by_category"]["other"]["verified"] == 0
    
    # Check discipline breakdown
    assert "tu_vi" in report_all["by_discipline"]
    assert report_all["by_discipline"]["tu_vi"]["cases"] == 1
    assert report_all["by_discipline"]["tu_vi"]["predictions"] == 2
    assert report_all["by_discipline"]["tu_vi"]["verified"] == 2
    assert pytest.approx(report_all["by_discipline"]["tu_vi"]["avg_accuracy"], 0.01) == 0.8
    
    # Discipline-filtered report
    report_tu_vi = get_accuracy_report(discipline="tu_vi", db_path=temp_db)
    assert report_tu_vi["discipline_filter"] == "tu_vi"
    assert report_tu_vi["total_cases"] == 1
    assert report_tu_vi["total_predictions"] == 2
    assert report_tu_vi["verified_predictions"] == 2
    assert pytest.approx(report_tu_vi["avg_accuracy"], 0.01) == 0.8


def test_list_cases_and_pagination(temp_db):
    """Test listing cases with discipline filtering and pagination."""
    add_case(discipline="bat_tu", question="Bát Tự 1", db_path=temp_db)
    add_case(discipline="bat_tu", question="Bát Tự 2", db_path=temp_db)
    c3 = add_case(discipline="ky_mon", question="Kỳ Môn 1", db_path=temp_db)
    add_prediction(c3, "Thắng kiện", category="career", db_path=temp_db)
    
    cases_all = list_cases(db_path=temp_db)
    assert len(cases_all) == 3
    
    cases_bazi = list_cases(discipline="bat_tu", db_path=temp_db)
    assert len(cases_bazi) == 2
    assert all(c["discipline"] == "bat_tu" for c in cases_bazi)
    
    cases_kymon = list_cases(discipline="ky_mon", db_path=temp_db)
    assert len(cases_kymon) == 1
    assert cases_kymon[0]["prediction_count"] == 1
    assert cases_kymon[0]["verified_count"] == 0
    
    # Pagination
    paged = list_cases(limit=1, offset=1, db_path=temp_db)
    assert len(paged) == 1


def test_unverified_predictions_query(temp_db):
    """Test querying unverified predictions with age filters."""
    c_id = add_case(question="Dự đoán chưa kiểm chứng", discipline="synthesis", db_path=temp_db)
    
    p1 = add_prediction(c_id, "Dự đoán 1 chưa kiểm chứng", db_path=temp_db)
    p2 = add_prediction(c_id, "Dự đoán 2 đã kiểm chứng", db_path=temp_db)
    verify_prediction(p2, "Đã xảy ra", accuracy_score=1.0, db_path=temp_db)
    
    # Query all unverified
    unverified_all = get_unverified_predictions(days_old=0, db_path=temp_db)
    assert len(unverified_all) == 1
    assert unverified_all[0]["prediction_id"] == p1
    assert unverified_all[0]["question"] == "Dự đoán chưa kiểm chứng"
    assert unverified_all[0]["discipline"] == "synthesis"


def test_delete_case_cascade(temp_db):
    """Test cascade deletion of case, predictions, and outcomes."""
    c_id = add_case(question="Xóa kiểm thử", discipline="phong_thuy", db_path=temp_db)
    p_id = add_prediction(c_id, "Dự đoán phong thủy", db_path=temp_db)
    o_id = verify_prediction(p_id, "Kết quả", accuracy_score=0.8, db_path=temp_db)
    
    # Delete case
    success = delete_case(c_id, db_path=temp_db)
    assert success is True
    
    # Verify case is gone
    assert get_case(c_id, db_path=temp_db) is None
    
    # Verify prediction and outcome are cascaded in SQLite
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE id = ?", (p_id,))
    assert cursor.fetchone()[0] == 0
    cursor.execute("SELECT COUNT(*) FROM outcomes WHERE id = ?", (o_id,))
    assert cursor.fetchone()[0] == 0
    conn.close()
