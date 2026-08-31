---
name: iching-deep-research
description: Động cơ Deep Research Toàn Diện Thuật Số Kinh Điển Cổ Thư Á Đông (Kinh Dịch, Tử Bình Bát Tự, Tử Vi Đẩu Số Đa Phái Toàn Diện 110+ Sao, Bát Tự Hà Lạc, Kỳ Môn Độn Giáp, Trạch Cát Tung Shing, Dự Báo Lưu Niên 12 Tháng, Đan Đạo Dưỡng Sinh, Huyền Không Phi Tinh Vận 9, Ma Trận Giao Thoa Chéo, Pipeline Kiểm Thử Tải Cao Đa Thế Kỷ & Đối Chứng Zero-Diff CanonicalAstrolabe). 100% Offline, <2ms, Zero Context Bloat, đồng bộ NTP Atomic Clock, Master Synthesis Report, Agent-First JSON API & Interactive Visual Dashboard.
---

# HƯỚNG DẪN VẬN HÀNH CHUẨN (STANDARD OPERATING PROCEDURE - SOP)
# ĐỘNG CƠ THUẬT SỐ Á ĐÔNG ALL-IN-ONE & KIẾN TRÚC BỘ NHỚ ĐẠO TẦNG NHỚ (v4.5.0)

> **DÀNH CHO TẤT CẢ CÁC AI AGENT (MÔI TRƯỜNG MỚI / NGỮ CẢNH SẠCH / KHỞI ĐỘNG LẠNH - COLD START):**  
> Bản tài liệu này là **Quy trình Vận hành Bất Biến (Deterministic SOP)**. Khi nhận được bất kỳ yêu cầu nào liên quan đến Kinh Dịch, Tử Vi, Bát Tự, Kỳ Môn, Phong Thủy, Đan Đạo, Đông Y, hoặc Xem Vận Mệnh, AI BẮT BUỘC tuân thủ tuần tự 5 Bước dưới đây.

---

## I. QUY TRÌNH 5 BƯỚC THỰC THI CHUẨN XÁC (5-STEP AI WORKFLOW)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: BÓC TÁCH THÔNG TIN & XÁC ĐỊNH MỤC TIÊU                              │
│ • Họ tên, Ngày giờ sinh (DD/MM/YYYY HH:MM), Giới tính (1=Nam, 0=Nữ), Nơi sinh│
│ • Vấn sự cần hỏi & Phân loại phương pháp (Gieo đồng xu / Mai Hoa / Tử Vi...) │
├─────────────────────────────────────────────────────────────────────────────┤
│ BƯỚC 2: TRA CỨU HỒ SƠ L5 & BỘ NHỚ ĐA TẦNG (MEMORY PRE-CHECK)                │
│ • Lệnh: python -m engine.cli --find-person "<Tên>"                          │
│ • Lấy vân tay Bát Tự/Tử Vi và trường phái ưa thích (preferred_school)       │
├─────────────────────────────────────────────────────────────────────────────┤
│ BƯỚC 3: CHẠY LỆNH CLI ĐỘNG CƠ PHÙ HỢP (DETERMINISTIC DISPATCH)              │
│ • Tra bảng Ma Trận Lệnh ở Mục II bên dưới để gọi đúng cờ lệnh CLI           │
├─────────────────────────────────────────────────────────────────────────────┤
│ BƯỚC 4: XUẤT BÁO CÁO 100% METADATA + LUẬN GIẢI CHUYÊN SÂU (29 RULES)        │
│ • Đặt BẢNG METADATA KỸ THUẬT của Engine lên ĐẦU TIÊN (100% nguyên văn)      │
│ • Luận giải đa tầng: Dụng Thần, Manh Phái, Sát Tinh, Tứ Hóa, Y Dịch         │
│ • Nếu có dị biệt trường phái: Chạy Quy trình Hiệu chuẩn Đối chứng (Rule 28) │
│ • Bắt buộc dùng mũi tên Unicode `→` (Rule 29)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ BƯỚC 5: TỰ ĐỘNG GHI NHỚ & TIẾN HÓA BỘ NHỚ L4/L5 (CONSOLIDATION)             │
│ • Tự động ghi nhận ca quẻ/dự đoán vào case_tracker.db                        │
│ • Trích xuất mẫu hình công thức (Patterns) nuôi dưỡng Tam Cấp Ngưỡng        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## II. BẢNG MA TRẬN LỆNH DÒNG LỆNH (DETERMINISTIC CLI DISPATCH TABLE)

AI chỉ cần xác định nhu cầu của người dùng và copy chạy chính xác lệnh tương ứng:

| Nhu Cầu Người Dùng | Lệnh CLI Chuẩn (Chạy tại thư mục dự án) | Ghi Chú Kỹ Thuật |
|:---|:---|:---|
| **1. Gieo Quẻ Đồng Xu (Roll Coins)** | `python -m engine.cli --roll-coins --question "<Câu hỏi>"` | Tự động tung 3 đồng xu 6 lần theo chuẩn Dã Hạc |
| **2. Gieo Quẻ Nhập Số Xu Cụ Thể** | `python -m engine.cli --coins "<6 số, vd: 789678>" --question "<Câu hỏi>"` | 6=Lão Âm, 7=Thiếu Dương, 8=Thiếu Âm, 9=Lão Dương |
| **3. Gieo Quẻ Mai Hoa Thời Gian Hiện Tại** | `python -m engine.cli --now --question "<Câu hỏi>"` | Khởi quẻ theo NTP Atomic Clock chính xác từng giây |
| **4. Xem Tử Vi Đẩu Số Toàn Diện (110+ Sao)** | `python -m engine.cli --tu-vi "DD/MM/YYYY HH:MM" --gender 1 --birth-place "Hà Nội" --school standard` | `--school`: `standard`, `kham_thien`, `nam_phai`, `trung_chau` |
| **5. Xem Tử Bình Bát Tự (Four Pillars)** | `python -m engine.cli --bazi "DD/MM/YYYY HH:MM" --gender 1` | Xuất Tứ Trụ, Thập Thần, Nạp Âm, Thần Sát, Đại Vận |
| **6. Xem Bát Tự Hà Lạc (Tiên/Hậu Thiên)** | `python -m engine.cli --ha-lac "DD/MM/YYYY HH:MM" --gender 1` | Quẻ Tiên Thiên, Hậu Thiên, Hóa Công, 100 năm |
| **7. Xem Kỳ Môn Độn Giáp Chiến Lược** | `python -m engine.cli --ky-mon-now` hoặc `--ky-mon "DD/MM/YYYY HH:MM"` | Bát Môn, Cửu Tinh, Bát Thần, Tam Kỳ Lục Nghi |
| **8. Xem Phong Thủy Huyền Không Vận 9** | `python -m engine.cli --feng-shui "<Sơn Hướng, vd: Tý, Ngọ>" --birth-year 1990` | 24 Sơn Hướng, Thành Môn, Sơn/Hướng Tinh, Hóa Giải |
| **9. Xem Đan Đạo Dưỡng Sinh & Ngũ Tạng** | `python -m engine.cli --health "DD/MM/YYYY HH:MM" --gender 1` | Chẩn đoán Ngũ Tạng thừa/thiếu, Lục Tự Quyết, Khí công |
| **10. Giao Thoa Y Dịch (Đông Y ✕ Lục Hào)** | `python -m engine.cli --cross-health "DD/MM/YYYY HH:MM" --question "<Bệnh lý/Sức khỏe>"` | Kết nối quẻ Dịch với kinh lạc ngũ tạng Đông Y |
| **11. Dự Báo Lưu Niên 12 Tháng Cả Năm** | `python -m engine.cli --yearly 2026 --question "<Định hướng năm>"` | Dự báo chi tiết 12 tháng qua 4 bộ môn |
| **12. Đại Tổng Hợp Đa Môn (Master Synthesis)** | `python -m engine.cli --synthesis --time "DD/MM/YYYY HH:MM" --question "<Câu hỏi>" --gender 1` | Tổng hợp đồng thời cả 6 môn vào 1 bản JSON/Report |
| **13. Tra cứu Kho Sách Cổ (FTS5 200+ Sách)** | `python -m engine.cli --canon-fts "<Từ khóa, vd: Hỏa Không tương kích>"` | Quét toàn văn 418 PDF sách cổ kinh điển |
| **14. Tra cứu Quy Tắc Tử Vi (6.285 Rules)** | `python -m engine.cli --tuvi-rules "<Tên sao/cung vị, vd: Vũ Khúc Hóa Kỵ>"` | Tìm kiếm quy tắc kinh điển danh gia |
| **15. Tra cứu / Quản lý Bộ Nhớ (L0 - L5)** | `python -m engine.cli --memory-stats` / `--find-person "<Tên>"` / `--person-journey <ID>` | Xem hồ sơ cá nhân, thống kê mẫu hình tiến hóa |

---

## III. BẢNG 29 QUY TẮC BẤT BIẾN KHI LUẬN GIẢI (29 GOLDEN RULES)

Khi sinh nội dung phản hồi cho người dùng, AI bắt buộc áp dụng các quy tắc sau:

1. **Rule 24 & Rule 25 (Tiêu chuẩn Bảng Metadata 100%)**:  
   BẮT BUỘC in nguyên văn Bảng Metadata Kỹ Thuật do CLI Engine xuất ra ở **đầu phản hồi**. Bảng này chứa đầy đủ: Thời gian kép (Dương/Âm), Tứ Trụ, Tiết Khí, Tuần Không kép, Bảng Thần Sát (10 thần sát), Quải Thân, Phục Thần, Bảng 6 Hào (Thế/Ứng, Lục Thân, Can Chi, Vượng/Suy, Không Vong, Thần Sát, Lục Thú, Trạng thái Động/Tĩnh). Tuyệt đối không tự bịa Can Chi hay sửa đổi bảng này.
2. **Rule 26 (Manh Phái Bát Tự & Sát Tinh Tứ Hóa)**:  
   - Bát Tự: Phải xét **Điều Hầu Dụng Thần** (Hàn/Nhiệt mùa sinh theo *Cùng Thông Bảo Giám*). Phân tích tương tác chi Manh Phái (Thìn-Sửu phá, Hợi-Mão hợp...).  
   - Tử Vi: Phải xét đủ **Lục Sát Tinh** (Không, Kiếp, Kình, Đà, Hỏa, Linh) và **4 Tứ Hóa Năm Sinh** (Lộc A, Quyền B, Khoa C, Kỵ D).
3. **Rule 27 (Dụng Thần Khí Tượng - Dự Báo Thời Tiết)**:  
   Nếu câu hỏi về thời tiết: Phụ Mẫu = Mưa/Mây tuyết; Thê Tài = Trời nắng; Tử Tôn = Trời quang tạnh ráo; Quan Quỷ = Giông bão sấm sét; Huynh Đệ = Gió bão.
4. **Rule 28 (Quy Chuẩn Đối Chiếu Đa Phái & Trọng Tài Phản Hồi Đương Số)**:  
   - Tôn trọng cả phái **Toàn Thư / Trung Châu / Đài Loan** (phân định sâu Âm Dương Thuận Nghịch, Tứ Hóa Phi Tinh) và **Nam Phái Việt Nam** (Cụ Thái Thứ Lang / Cụ Thiên Lương, chuyên sâu Miếu Hãm, Thần Sát).  
   - Khi có điểm dị biệt an sao (Hỏa/Linh, Vòng Trường Sinh, Tứ Hóa Canh/Nhâm, Tuần/Triệt): Trình bày 2 góc nhìn $ightarrow$ Chuyển hóa thành câu hỏi thực chứng đời sống $ightarrow$ Hỏi đương số xác nhận $ightarrow$ Lưu `preferred_school` vào hồ sơ L5.
5. **Rule 29 (Chuẩn Hóa Ký Tự Mũi Tên & Chống Lỗi KaTeX)**:  
   BẮT BUỘC dùng ký tự Unicode `→` (U+2192) hoặc ASCII `->` cho mọi tuyến luân chuyển phi tinh. Tuyệt đối KHÔNG dùng LaTeX `$\rightarrow$` để tránh lỗi nuốt `\r` thành `ightarrow`. Luôn dùng Raw String `r"""..."""` khi sinh mã Python tạo file.

---

## IV. CẤU TRÚC BÀI LUẬN MẪU HOÀN HẢO (STANDARD OUTPUT TEMPLATE)

Một bài luận đạt chuẩn đẳng cấp Master của hệ thống luôn tuân theo cấu trúc 4 phần:

```markdown
```
[In nguyên văn BẢNG METADATA KỸ THUẬT 100% từ CLI Engine]
```

---

### I. TỔNG QUAN TƯƠNG QUAN KHÍ CƠ & DỤNG THẦN
- Phân tích tương tác Ngũ Hành, Dụng Thần (Điều Hầu / Ứng Dụng), thế trận Thể - Dụng.

### II. LUẬN GIẢI CHI TIẾT THEO CÁC BỘ MÔN (ĐỐI CHIẾU SONG SONG)
- Nếu là Kinh Dịch: Luận giải Quẻ Chủ, Hào Động, Quẻ Biến, Lục Thân, Lục Thú, Ứng Kỳ.
- Nếu là Tử Vi / Bát Tự: Phân tích Tứ Trụ, Đại Vận, 12 Cung, Tứ Hóa Khí Đạo, Lục Sát Tinh.
- Nếu có dị biệt trường phái: Lập bảng đối chiếu (Nam Phái vs Toàn Thư) kèm câu hỏi thực chứng.

### III. Y DỊCH ĐỒNG NGUYÊN & PHƯƠNG PHÁP HÓA GIẢI / DƯỠNG SINH
- Lời khuyên Đan Đạo / Phong Thủy / Tâm Pháp cụ thể để chuyển hung thành cát, đạt Thủy Hỏa Ký Tế.

### IV. GHI NHẬN HỒ SƠ & BỘ NHỚ TIẾN HÓA
- Tóm tắt công thức mẫu hình (Pattern) đã được lưu vào hệ thống để theo dõi kiểm chứng.
```

---

## V. ĐỒNG BỘ HÓA MÔI TRƯỜNG & LIÊN KẾT MÃ NGUỒN

Tất cả mã nguồn cốt lõi nằm tại: `C:\Users\Administrator\.gemini\antigravity\scratch\iching-all-in-one`.  
Đồng bộ sang kho lưu trữ: `D:\Book-20251020T041506Z-1-001\AIAgent`.  
GitHub Repository: `https://github.com/SUGirlBae/Universal-Eastern-Metaphysics-Suite`.
