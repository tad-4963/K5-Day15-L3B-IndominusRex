# Đào data — cách đếm và kết quả

> Người phụ trách: **Hoàng Thế Phong (2A202603832) — Cặp 2**  
> Dùng cho: Bằng chứng Nguồn 1 chứng minh nỗi đau của Giảng viên & Lab Coach khi không nắm được điểm nghẽn của lớp trước giờ lên lớp.  
> Script tái lập: `python3 scripts/mine_evidence.py` (chạy độc lập, cho ra kết quả đồng nhất).

---

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Log tương tác pre-class khoá học AI20K (Cohort V) từ Day01 đến Day13. Bao gồm các sự kiện trả lời câu hỏi trắc nghiệm kiến thức (Knowledge Check - KC) và trạng thái thực hành Mini Lab.
- **Đếm gì:**
  1. Số học viên tham gia làm bài pre-class theo từng ngày (`active`).
  2. Số lượt và tỷ lệ học viên trả lời sai ngay lần đầu ở các câu trắc nghiệm cốt lõi (`kc_errors`).
  3. Số lượt và tỷ lệ học viên bỏ dở hoặc không hoàn thành bài tập thực hành Mini Lab (`lab_incomplete`).
- **Mẫu số là gì (N):**
  - **Mẫu số tổng (Enrolled):** 721 học viên đăng ký khoá học.
  - **Mẫu số active toàn khoá:** 436 học viên (có phát sinh ít nhất 1 tương tác pre-class từ Day01 đến Day13). Tỷ lệ active toàn khoá: 436/721 (60.5%).
  - **Mẫu số từng ngày ($N_{day}$):** Số học viên thực sự làm bài pre-class của ngày đó (từ 412 ở Day01 giảm dần xuống 84 ở Day13). *Lưu ý: Không dùng mẫu số cố định 721 cho từng ngày để tránh làm méo mó tỷ lệ sai của những người thực học.*
- **Script tái lập:** `scripts/mine_evidence.py`

---

## 2. Đọc trước, đếm sau

Đã đọc cấu trúc dữ liệu và log 100 dòng đầu của các bảng tương tác. Các *kiểu hành vi* phát hiện được trước khi đếm:
- **Kiểu 1 (Vấp ở khái niệm trừu tượng):** Ở các bài học lý thuyết thuần túy (như State Machine, ReAct loop, Retrieval Context), học viên hay chọn sai ở câu hỏi phân biệt ranh giới khái niệm trong lần thử đầu tiên.
- **Kiểu 2 (Bỏ dở Mini Lab khi gặp lỗi môi trường / code phức tạp):** Học viên bắt đầu bài lab nhưng dừng lại ở bước 2 hoặc 3 (chưa ra kết quả cuối), log ghi nhận trạng thái `incomplete` hoặc `abandoned`.
- **Kiểu 3 (Sụt giảm tương tác - Drop-off):** Càng về các ngày cuối (Day10–Day13), số lượng học viên hoàn thành pre-class trước giờ học giảm mạnh (dưới 150 người), khiến mẫu dữ liệu bị nhỏ (`n < 150`), dễ gây ngộ nhận nếu không có cơ chế cảnh báo độ tin cậy.

---

## 3. Kết quả khai phá (Data Mining)

Tái lập bằng lệnh: `python3 scripts/mine_evidence.py`

| Ngày | Số học viên làm bài ($N_{day}$) | Số học viên sai KC ($x$) | % Sai KC | Số học viên kẹt Mini Lab ($x$) | % Kẹt Lab | Chủ đề điểm nghẽn chính |
|---|---|---|---|---|---|---|
| **Day01** | 412 | 75 | 18.2% | 35 | 8.5% | Cài đặt môi trường & Python cơ bản |
| **Day02** | 388 | 95 | 24.5% | 54 | 13.9% | Prompt Engineering căn bản |
| **Day03** | 354 | 112 | 31.6% | 73 | 20.6% | Tool use & function calling |
| **Day04** | 335 | 100 | 29.9% | 73 | 21.8% | ReAct pattern loop |
| **Day05** | **312** | **198** | **63.5%** | **184** | **59.0%** | **Agent Loop & State Machine (ĐIỂM NGHẼN NẶNG)** |
| **Day06** | 289 | 99 | 34.3% | 75 | 26.0% | Data Ingestion & Embedding |
| **Day07** | **268** | **145** | **54.1%** | **129** | **48.1%** | **Retrieval Context & Vector Search (NGHẼN KC)** |
| **Day08** | 245 | 95 | 38.8% | 75 | 30.6% | Workflow to Autonomous Agent |
| **Day09** | **215** | 91 | 42.3% | **112** | **52.1%** | **Evaluation & Failure Analysis (NGHẼN LAB)** |
| **Day10** | **168** | 78 | 46.4% | **96** | **57.1%** | **PoC to Pilot Gate (MẪU NHỎ, NGHẼN LAB)** |
| **Day11** | 152 | 62 | 40.8% | 58 | 38.2% | Guardrails & Human-in-the-loop |
| **Day12** | **142** | **73** | **51.4%** | **89** | **62.7%** | **AI-SDLC & Multi-step Workflow (NGHẼN LAB CAO)** |
| **Day13** | **84** | **45** | **53.6%** | **55** | **65.5%** | **Launch Economics & Cost (MẪU RẤT NHỎ)** |

### Các chỉ số tổng hợp chính:
1. **Tỷ lệ học viên gặp ít nhất một điểm nghẽn:** **382 / 436 học viên active (87.6%)** từng gặp ít nhất 1 bài KC có tỷ lệ sai toàn lớp $\ge 50\%$ hoặc không hoàn thành Mini Lab.
2. **Các "ổ điểm nghẽn" lớn nhất:** Day05 (63.5% sai State Machine), Day07 (54.1% sai Retrieval Context), Day12 (62.7% kẹt Mini Lab SDLC).
3. **Mức độ sụt giảm mẫu số (Drop-off):** Từ 412 học viên (Day01) giảm xuống 84 học viên (Day13), tức tỷ lệ nộp bài trước giờ giảm **79.6%**. Bắt buộc AI phải kích hoạt nguyên tắc HAX G10: cảnh báo mẫu số nhỏ khi $N < 150$.

---

## 4. Năm ví dụ cụ thể minh chứng điểm nghẽn

1. **Ví dụ 1 (Day05 — Khái niệm State Machine & Vòng lặp dừng):**
   - 198 / 312 học viên (63.5%) trả lời sai câu hỏi về điều kiện dừng của vòng lặp ReAct khi agent bị kẹt loop vô tận. 184 / 312 học viên (59.0%) không chạy ra được output cuối cùng của mini lab do lỗi state transition.
2. **Ví dụ 2 (Day07 — Cơ chế Retrieval Context & Chunking):**
   - 145 / 268 học viên (54.1%) chọn sai phương án về kích thước chunk size và overlap khi retrieval tài liệu dài, dẫn đến mất ngữ cảnh quan trọng.
3. **Ví dụ 3 (Day09 — Đánh giá & Phân tích lỗi):**
   - 112 / 215 học viên (52.1%) bỏ dở mini lab khi phải tự viết hàm đo lường metric F1 / Recall cho LLM judge, gây dồn ứ câu hỏi kỹ thuật khi vào buổi lab.
4. **Ví dụ 4 (Day10 — PoC to Pilot Gate & Ngưỡng chấp nhận):**
   - 96 / 168 học viên (57.1%) không đạt điều kiện pass ở bước xác định ngưỡng latency và cost budget cho kịch bản triển khai pilot thực tế.
5. **Ví dụ 5 (Day12 — AI-SDLC Multi-step Workflow):**
   - 89 / 142 học viên (62.7%) bị fail ở khâu nối pipeline 3 bước tự động. Do số lượng học viên làm bài chỉ còn 142 ($< 150$), đây là điển hình của trường hợp vừa có tỷ lệ lỗi cao vừa thuộc diện dữ liệu mẫu nhỏ cần chú thích thận trọng.

---

## 5. Giới hạn của dữ liệu

- **Chỉ ghi nhận hành vi, không có nội dung chữ chat:** Dữ liệu log chỉ phản ánh *sự kiện* (trả lời đúng/sai, bắt đầu/kết thúc lab, click timestamp). Log hoàn toàn **không lưu văn bản câu hỏi chi tiết hay tin nhắn trao đổi của học viên** trong file `chat.csv` (nhằm đảm bảo quyền riêng tư).
- **Hệ quả đối với AI:** AI không được suy diễn bừa bãi nguyên nhân chi tiết nếu không có căn cứ từ dữ liệu số; khi báo cáo cho Giảng viên, AI phải nêu rõ giới hạn này để Giảng viên chủ động hỏi nhanh lớp vào đầu giờ.
- **Kiểm chứng chéo:** Bằng chứng số liệu này được kiểm chứng và bổ sung bởi **Nguồn 2 (Phỏng vấn thực tế ≥3 Giảng viên & Lab Coach)** tại `evidence/summary.md` và `evidence/interviews/`.
