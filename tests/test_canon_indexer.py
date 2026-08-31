import pytest
import sqlite3
from pathlib import Path
from engine.canon_indexer import (
    init_canon_db,
    chunk_text,
    classify_discipline,
    search_canon_fts,
    get_index_stats
)

def test_chunk_text():
    sample = "Đây là câu thứ nhất. Đây là câu thứ hai. Đây là câu thứ ba dài hơn một chút để thử nghiệm phân mảnh văn bản tự động trong hệ thống RAG thư tịch cổ."
    chunks = chunk_text(sample, max_chars=50, overlap=10)
    assert len(chunks) >= 2
    assert all(len(c) <= 100 for c in chunks)

def test_classify_discipline():
    assert classify_discipline("Tử vi đẩu số chính tinh cung mệnh", "tu_vi.pdf") == "tu_vi"
    assert classify_discipline("Bốc phệ hào quẻ lục hào dã hạc", "tang_san.pdf") == "kinh_dich"
    assert classify_discipline("Tử bình nhật chủ thập thần cách cục", "chan_thuyen.pdf") == "bat_tu"
    assert classify_discipline("Bát môn cửu tinh kỳ môn độn giáp", "ky_mon.pdf") == "ky_mon"
    assert classify_discipline("Huyền không cửu vận phong thủy bát trạch", "tham_thi.pdf") == "phong_thuy"
    assert classify_discipline("Kim đan chu thiên tĩnh tọa đan điền", "khue_chi.pdf") == "dan_dao"
    assert classify_discipline("Hoàng đế nội kinh tố vấn tạng phủ kinh mạch", "noi_kinh.pdf") == "dong_y"

def test_canon_fts_search_or_stats(tmp_path):
    test_db = tmp_path / "test_canon.db"
    init_canon_db(test_db)
    
    conn = sqlite3.connect(str(test_db))
    c = conn.cursor()
    c.execute("""
        INSERT INTO books (file_path, file_hash, title, author, discipline, total_pages, total_chunks)
        VALUES ('dummy.pdf', 'hash123', 'Tử Vi Toàn Thư', 'Trần Đoàn', 'tu_vi', 10, 1)
    """)
    book_id = c.lastrowid
    c.execute("""
        INSERT INTO chunks (book_id, page_num, chunk_index, content, discipline)
        VALUES (?, 1, 0, 'Cơ Lương hội hợp thiện đàm binh, Cự Nhật đồng cung quan bộ thanh vân', 'tu_vi')
    """, (book_id,))
    conn.commit()
    conn.close()

    res = search_canon_fts("Cơ Lương", db_path=test_db)
    assert len(res) >= 1
    assert "Cơ Lương" in res[0]["content"]
    assert res[0]["title"] == "Tử Vi Toàn Thư"

    stats = get_index_stats(test_db)
    assert stats["total_books"] == 1
    assert stats["total_chunks"] == 1
    assert stats["by_discipline"]["tu_vi"] == 1
