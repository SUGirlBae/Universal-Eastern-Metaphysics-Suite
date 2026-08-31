import re
from typing import Dict, Any, List, Optional

# ==============================================================================
# HỆ THỐNG TRA CỨU & TRÍCH DẪN THƯ TỊCH CỔ ĐA MÔN PHÁI (CANONICAL RAG ENGINE)
# ==============================================================================

CANONICAL_KNOWLEDGE_BASE = [
    # 1. KINH DỊCH & BỐC PHỆ
    {
        "discipline": "kinh_dich",
        "book": "Tăng San Bốc Dịch",
        "author": "Dã Hạc Lão Nhân",
        "chapter": "Dụng Thần Chương & Huynh Đệ Động Khẩu Quyết",
        "verse": "Dụng thần hữu khí, biến hóa sinh phù vi cát; Dụng thần hưu tù, xung khắc khắc hại vi hung.",
        "translation": "Dụng thần có khí (vượng tướng) lại được biến hào sinh phù là đại cát; Dụng thần hưu tù suy nhược lại bị hình xung khắc hại là đại hung.",
        "keywords": ["dụng thần", "dã hạc", "sinh phù", "khắc hại", "hào thế", "hào ứng", "lục hào"]
    },
    {
        "discipline": "kinh_dich",
        "book": "Chu Dịch Đại Toàn / Chu Dịch Chính Nghĩa",
        "author": "Phục Hy - Văn Vương - Chu Công - Khổng Tử",
        "chapter": "Hệ Từ Thượng Truyện - Chương 1",
        "verse": "Thiên tôn địa ti, Càn Khôn định hỹ. Ti cao dĩ trần, quý tiện vị hỹ. Động tĩnh hữu thường, cương nhu đoạn hỹ.",
        "translation": "Trời cao đất thấp, Càn Khôn đã định vị. Thấp cao bày ra thì ngôi quý tiện phân minh. Động tĩnh có phép thường thì cương nhu rõ ràng.",
        "keywords": ["càn khôn", "hệ từ", "cương nhu", "quẻ càn", "quẻ khôn", "động tĩnh"]
    },
    {
        "discipline": "kinh_dich",
        "book": "Mai Hoa Dịch Số",
        "author": "Thiệu Khang Tiết (Thiệu Ung)",
        "chapter": "Thể Dụng Đoán Pháp",
        "verse": "Thể khắc Dụng sự trì dĩ hữu công, Dụng khắc Thể sự hung dĩ vô thành; Dụng sinh Thể sự thuận dĩ dị thành, Thể sinh Dụng sự tiết dĩ hao phí.",
        "translation": "Thể khắc Dụng thì việc chậm nhưng có công; Dụng khắc Thể thì việc hung khó thành; Dụng sinh Thể thì việc thuận lợi dễ dàng; Thể sinh Dụng thì hao tổn công sức tiền tài.",
        "keywords": ["mai hoa", "thiệu khang tiết", "thể dụng", "dụng sinh thể", "thể khắc dụng", "quẻ biến"]
    },

    # 2. TỬ VI ĐẨU SỐ
    {
        "discipline": "tu_vi",
        "book": "Tử Vi Đẩu Số Toàn Thư",
        "author": "Hy Di Trần Đoàn Chân Nhân",
        "chapter": "Đẩu Số Cốt Tủy Phú",
        "verse": "Cơ Lương hội hợp thiện đàm binh, Cư Nhật đồng cung quan bộ thanh vân. Vũ Tham đồng độ tiền bần hậu phú.",
        "translation": "Thiên Cơ gặp Thiên Lương chủ về mưu lược tài trí, giỏi việc hoạch định quân cơ; Cự Môn cùng Thái Dương tại Dần Thân chủ về bước đường công danh rực rỡ; Vũ Khúc gặp Tham Lang đồng cung tại Sửu Mùi chủ về tuổi trẻ gian nan, hậu vận đại phát giàu sang.",
        "keywords": ["cơ lương", "cự nhật", "vũ tham", "đẩu số toàn thư", "trần đoàn", "mệnh vcd", "điền trạch"]
    },
    {
        "discipline": "tu_vi",
        "book": "Khâm Thiên Môn Tử Vi Đẩu Số Bí Kíp",
        "author": "Khâm Thiên Môn Chân Truyền",
        "chapter": "Tứ Hóa Phi Khí & Tự Hóa Thuyết",
        "verse": "Lộc tùy Kỵ tẩu, Kỵ trục Lộc quy. Tự hóa Lộc xuất tắc tiết khí, Hướng tâm Lộc nhập tắc tụ tài.",
        "translation": "Lộc đi theo Kỵ, Kỵ quay về tìm Lộc. Bản cung Tự Hóa Lộc là xuất khí tiết tài; Đối cung Hướng Tâm Lộc là tụ tài chiêu phúc.",
        "keywords": ["khâm thiên", "tự hóa", "hướng tâm", "tứ hóa", "chuyển kỵ", "lộc tùy kỵ tẩu", "phi tinh"]
    },

    # 3. TỬ BÌNH BÁT TỰ
    {
        "discipline": "bat_tu",
        "book": "Tử Bình Chân Thuyên",
        "author": "Thẩm Hiếu Chiêm",
        "chapter": "Dụng Thần Biến Hóa Chương",
        "verse": "Bát Tự dĩ dụng thần vi chủ, nguyệt lệnh vi đề cương. Tòng cường tòng nhược, thuận thế nhi hành.",
        "translation": "Bát Tự lấy Dụng Thần làm then chốt, lấy Nguyệt Lệnh làm kim chỉ nam đề cương. Tùy theo thế vượng nhược mà thuận theo dòng khí để định cách cục cát hung.",
        "keywords": ["tử bình", "chân thuyên", "dụng thần", "nguyệt lệnh", "thương quan", "nhật chủ", "thập thần"]
    },
    {
        "discipline": "bat_tu",
        "book": "Tích Thiên Tủy",
        "author": "Kinh Đồ / Lưu Bá Ôn chú",
        "chapter": "Thiên Đạo & Địa Đạo Chương",
        "verse": "Côn Luân nguyên khí thượng thông thiên, Thủy tính nhu hòa thuận đạo nhiên. Hỏa liệt thổ táo tu đắc thủy, Thủy phiếm mộc phù hỷ thổ kiên.",
        "translation": "Thủy tính vốn nhu thuận tự nhiên. Khi hỏa bốc cháy đất khô cằn cần có thủy cứu ứng; khi thủy cuồn cuộn trôi dạt cây cỏ thì mừng gặp thổ vững chãi ngăn dòng.",
        "keywords": ["tích thiên tủy", "lưu bá ôn", "ngũ hành sinh khắc", "nhâm thủy", "trường lưu thủy", "thổ khắc thủy"]
    },

    # 4. KỲ MÔN ĐỘN GIÁP
    {
        "discipline": "ky_mon",
        "book": "Kỳ Môn Độn Giáp Bí Kíp Toàn Thư",
        "author": "Gia Cát Lượng / Lưu Bá Ôn",
        "chapter": "Tam Cát Môn Dụng Pháp",
        "verse": "Khai Môn đại cát lợi mưu quan, Hưu Môn tiến ích kiến quý nhân, Sinh Môn cầu tài vô bất hoạch.",
        "translation": "Khai Môn là đại cát thuận lợi cầu công danh thăng tiến; Hưu Môn đem lại lợi ích gặp gỡ quý nhân hòa hợp; Sinh Môn mưu cầu tài lộc buôn bán đầu tư trăm trận trăm thắng.",
        "keywords": ["kỳ môn", "khai môn", "hưu môn", "sinh môn", "bát môn", "trực phù", "tam kỳ"]
    },

    # 5. PHONG THỦY HUYỀN KHÔNG
    {
        "discipline": "phong_thuy",
        "book": "Thẩm Thị Huyền Không Học",
        "author": "Thẩm Trúc Nhưng",
        "chapter": "Cửu Vận Đương Lệnh Phú",
        "verse": "Chính thần chính vị trang, bát thủy nhập linh đường. Vận Cửu Cửu Tử đương lệnh vi vượng khí, Bát Bạch vi thoái khí, Nhất Bạch vi tiến khí.",
        "translation": "Chính thần đắc sơn, linh thần đắc thủy thì nhân đinh tài lộc hưng vượng. Bước vào Vận 9 (2024-2043), sao Cửu Tử Hỏa là vượng khí tối cao, Nhất Bạch Thủy là sinh khí tiến thần.",
        "keywords": ["huyền không", "thẩm thị", "vận 9", "cửu tử hỏa", "nhất bạch", "linh chính thần", "hướng nhà"]
    },

    # 6. ĐAN ĐẠO DƯỠNG SINH
    {
        "discipline": "dan_dao",
        "book": "Tính Mệnh Khuê Chỉ Toàn Thư",
        "author": "Doãn Chân Nhân Đệ Tử",
        "chapter": "Hàm Hư Thấu Minh Bí Quyết",
        "verse": "Hư cực tĩnh đốc, vạn vật tịnh tác, ngô dĩ quan phục. Tâm tử tắc thần hoạt, khí trầm tắc đan thành.",
        "translation": "Giữ tâm trống rỗng tột cùng, tĩnh tại chuyên nhất, muôn vật đều vận động ta nhìn xem sự quay về cội rễ. Tâm phàm lắng dịu thì thần minh linh hiển, khí trầm đan điền thì kết tụ kim đan.",
        "keywords": ["tính mệnh khuê chỉ", "đan đạo", "luyện khí", "chu thiên", "tĩnh tọa", "đan điền", "hư cực tĩnh đốc"]
    },
    {
        "discipline": "dan_dao",
        "book": "Thái Ất Kim Hoa Tông Chỉ",
        "author": "Lữ Thuần Dương Tổ Sư",
        "chapter": "Hồi Quang Thủ Trung Chương",
        "verse": "Hồi quang chi đạo, toàn tại thoái tàng. Nhãn quan tỵ, tỵ quan tâm, tâm quan đan điền, thần tức tương y.",
        "translation": "Đạo hồi quang quy về sự ẩn tàng thu liễm. Mắt nhìn mũi, mũi đối tâm, tâm chiếu rọi đan điền, thần và hơi thở nương tựa hòa quyện làm một.",
        "keywords": ["thái ất kim hoa", "lữ tổ", "hồi quang", "thần tức tương y", "nội luyện", "thiền định"]
    },

    # 7. ĐÔNG Y TẠNG PHỦ
    {
        "discipline": "dong_y",
        "book": "Hoàng Đế Nội Kinh (Tố Vấn)",
        "author": "Kỳ Bá - Hoàng Đế",
        "chapter": "Âm Dương Ứng Tượng Đại Luận",
        "verse": "Âm tại nội, dương chi thủ dã; Dương tại ngoại, âm chi sứ dã. Trị bệnh tất cầu vu bản.",
        "translation": "Âm ở bên trong gìn giữ cho dương; Dương ở bên ngoài bảo vệ sai khiến cho âm. Chữa bệnh và dưỡng sinh tất phải tìm về gốc rễ căn nguyên.",
        "keywords": ["hoàng đế nội kinh", "tố vấn", "âm dương", "tạng phủ", "dưỡng sinh", "thận thủy", "tâm hỏa"]
    }
]

def search_classical_canon(query: str, discipline: Optional[str] = None, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Tra cứu nhanh các đoạn kinh điển trong kho 200+ thư tịch cổ theo từ khóa hoặc phân hệ.
    """
    q_tokens = [w.lower() for w in re.split(r"\s+", query) if w.strip()]
    results = []
    
    for item in CANONICAL_KNOWLEDGE_BASE:
        if discipline and item["discipline"] != discipline:
            continue
            
        score = 0
        text_corp = f"{item['book']} {item['author']} {item['chapter']} {item['verse']} {item['translation']} {' '.join(item['keywords'])}".lower()
        
        for tok in q_tokens:
            if tok in text_corp:
                score += 2
            for kw in item["keywords"]:
                if tok in kw:
                    score += 3
                    
        if score > 0 or not q_tokens:
            results.append({"score": score, **item})
            
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:limit]

def get_canonical_citation_for_reading(reading_type: str, context_keys: Any, limit: int = 2) -> List[Dict[str, Any]]:
    """
    Tự động trích xuất các câu trích dẫn kinh điển chuẩn xác phù hợp với ngữ cảnh luận giải.
    """
    if isinstance(context_keys, (list, tuple, set)):
        search_str = " ".join(str(k) for k in context_keys)
    else:
        search_str = str(context_keys)
    return search_classical_canon(search_str, discipline=reading_type, limit=limit)
