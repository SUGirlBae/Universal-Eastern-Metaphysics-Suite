# 🌌 Antigravity Eastern Metaphysics All-In-One Suite (v2.3.0 Universal Edition)

[![CI Tests](https://img.shields.io/badge/pytest-21%20passed%20(100%25)-brightgreen.svg)]()
[![Benchmark](https://img.shields.io/badge/benchmark-10%2C000%20vectors%20zero--bug-blue.svg)]()
[![Speed](https://img.shields.io/badge/speed-%3C2ms%20per%20cycle-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Antigravity Eastern Metaphysics All-In-One Suite** là siêu hệ sinh thái phần mềm thuật số & kinh điển cổ thư phương Đông toàn diện chuẩn công nghiệp (Production-Grade), 100% Offline, hiệu năng siêu tốc (<2ms), tích hợp Web Dashboard tương tác và tương thích hoàn hảo với mọi nền tảng AI Agent (Antigravity, Claude Code, GitHub Copilot CLI, Cursor, AutoGen, CrewAI).

---

## ⚡ Các Phân Hệ Thuật Số Tích Hợp (9 Trong 1)

1. **Ma Trận Giao Thoa Chéo (Cross-Matrix Synthesis - Rule 13)**:
   - Lấy **Kinh Dịch làm xương sống 1 chiều** nhúng vào Đông Y & Phong Thủy để định vị ổ bệnh, kinh lạc và đồ vật phạm sát.
2. **Kinh Dịch Lục Hào Dã Hạc & Mai Hoa (I Ching)**: 
   - Đồng bộ NTP Máy chủ Nguyên tử (Cloudflare / Google), gieo xu 3 xu (0-6 hào động), nạp giáp đầy đủ 100% metadata.
   - Tự động chú thích Bát Cung Phân Vị (*Bát Thuần, Du Hồn, Quy Hồn, Lục Xung, Lục Hợp, Tứ Đại Nan Quái*).
3. **Tử Vi Đẩu Số (Tu Vi Engine)**:
   - Tính Chân Thái Dương Thời (True Solar Time), 12 Cung Vị, Cục số, 14 Chính Tinh, Tứ Hóa Năm Sinh & Phi Tinh.
4. **Tử Bình Bát Tự (Bazi Engine)**:
   - 4 Trụ (Năm, Tháng, Ngày, Giờ), Thập Thần, Tàng Can, Thần Sát, Đại Vận 10 năm.
5. **Dự Báo Thời Vận 12 Tháng (Annual Forecast)**:
   - Quét 6 hào Lục Hào tương ứng 6 giai đoạn (12 tháng), kết hợp Lưu Thái Tuế & Lưu Tứ Hóa.
6. **Đan Đạo Khí Cơ & Đông Y Tạng Phủ (Dan Dao Health)**:
   - Chẩn đoán ngũ hành 8 chữ, phát hiện tạng phủ Thái Quá/Bất Cập và phép thở Lục Tự Khí Quyết.
7. **Phong Thủy Huyền Không Vận 9 (2024–2043) & Bát Trạch**:
   - Trận đồ 9 Cung cho 24 Sơn Hướng (Tọa - Hướng) và Cung Phi bản mệnh gia chủ.
8. **Bát Tự Hà Lạc (He Luo Li Shu Engine)**:
   - Quẻ Tiên Thiên, Hậu Thiên, Hào Nguyên Khí, Hóa Công và Đại Vận 9 năm / 6 năm.
9. **Kỳ Môn Độn Giáp Thời Gia (Qi Men Dun Jia Engine)**:
   - Thiết lập Bàn Kỳ Môn 4 tầng (Địa, Thiên, Bát Môn, Cửu Tinh, Bát Thần, Trực Phù, Trực Sử).

---

## 🖥️ Giao Diện Web Trực Quan Tương Tác (Visual Dashboard)

Chạy lệnh sau để khởi động Web Dashboard cục bộ (Zero-dependency):
```bash
python engine/cli.py --server
# Mở trình duyệt tại: http://localhost:8888
```

---

## 💻 Sử Dụng Dòng Lệnh Nhanh (CLI Quickstart)

```bash
# 1. Giao thoa Y Dịch (Đông Y ✕ Kinh Dịch Lục Hào)
python engine/cli.py --cross-health "06/12/1999 02:00" --question "Đau mỏi vai gáy"

# 2. Giao thoa Dương Trạch (Huyền Không Vận 9 ✕ Gieo Xu Lục Hào)
python engine/cli.py --cross-feng-shui "Tý" --birth-year 1999 --coins "886788"

# 3. Xem thời vận ngày hôm nay (Tử Vi ✕ Kinh Dịch)
python engine/cli.py --tu-vi "06/12/1999 02:00" && python engine/cli.py --now --question "Thời vận hôm nay"

# 4. Dự báo thời vận 12 tháng cả năm
python engine/cli.py --yearly 2026 --question "Thời vận công danh sự nghiệp"

# 5. Gieo quẻ Lục Hào 3 xu (0-6 hào động)
python engine/cli.py --roll-coins --question "Mưu sự đại sự"
```

---

## 🤖 Dành Cho AI Agent (Agent-First API & MCP Server)

Hệ thống cung cấp sẵn máy chủ chuẩn **Model Context Protocol (MCP Server)** và cờ lệnh trích xuất dữ liệu JSON thuần khiết:

```bash
# Trích xuất payload JSON siêu đậm đặc (Zero Context Bloat) cho AI Agent
python engine/cli.py --agent-json --question "<câu hỏi>"

# Khởi động MCP Server chuẩn JSON-RPC Stdio
python engine/mcp_server.py
```

---

## 🧪 Chạy Kiểm Thử Toàn Diện (Pytest)

```bash
pytest -v tests/
```
