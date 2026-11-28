# Dàn slide 8 trang — Nhóm IndominusRex (Track A · Pre-Class Bottleneck Brief)

> Luật: **không có bằng chứng thì không có slide** — mỗi trang đều có số liệu / kết quả đo truy ngược được về file trong repo.  
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo (hoặc nộp link Canva/Google Slides ở form CP4 trước 14:30 Thứ Bảy 28/11).

| # | Trang | Nội dung chính & Con số đã kiểm chứng | File nguồn | Xong |
|---|---|---|---|---|
| 1 | **Người dùng & Pain** | GV & Lab Coach (84 nhân sự, >700 HV L3) không thấy điểm nghẽn trước giờ học. **Data thật (`data/preclass/`):** 436/721 (60,5%) active · **7/13 ngày** có KC `n≥5` sai ≥35% (Day05 `ai_product_canvas` **12/15 = 80%**, Day06 **6/7 = 85,7%**) · **6/13 ngày** mini lab (`open≥10`) skip+inc ≥40% (Day07 **58,3%**) · drop-off 417→26 (**-93,8%**). | `evidence/summary.md`, `evidence/data-mining.md` | ☑ |
| 2 | **Vì sao chọn bài này** | Bảng so sánh **4 hướng Track A** (giữ lại 3 hướng bị loại kèm lý do). Impact ước tính: `84 người × 12 buổi × 45 phút (ước tính) = 756 giờ/tháng` · Làm gọn trong 10h, dùng data thật BTC, rủi ro thấp hơn chatbot tự do. | `spec.md` §2 | ☑ |
| 3 | **Giải pháp AI** | **Lát cắt 1 câu** · Sơ đồ **Workflow cố định 3 bước** (lý do không chọn multi-agent) · Mức tự động **AI gợi ý, người duyệt (HITL)** · Chặn rủi ro 2 tầng (xóa 100% `hv` trong `lesson_signals_agg.json` + code guardrail) · HAX **G10** (cảnh báo mẫu nhỏ). | `spec.md` §4 | ☑ |
| 4 | **Demo live** | Chạy trực tiếp 1 case thường (`Day05` — 3 phần ≤2p đọc) + 1 case khó (`Day13` mẫu cực nhỏ `n=1–2` hoặc `T25/T26` tấn công chặn `0 token`) + sẵn sàng chạy câu lạ giám khảo đưa tại chỗ. *(Kèm link video dự phòng mở ẩn danh.)* | `codebase/`, `eval/benchmark.csv` | ☐ |
| 5 | **Đánh giá thế nào** | Bộ **26 câu** (`18/26` từ `data_that`, 4 metric, chấm chéo 5/5 khớp). **Lượt 1** (`run-1@20261127-223811`): **19/26 (73%)** — chưa đạt (3 nhóm lỗi: regex chặn oan `T19` & sót `T25/T26`, đảo nghĩa tỷ lệ sai `T18/T23`, sót video/lab `T07/T12`). **1 lần cải tiến → Lượt 2** (`run-2@20261127-224608`): **23/26 (88% — ĐẠT CHUẨN!)**, `tu_choi` **7/7 (100%)**, khai thật 1 regression ở `T22`. | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Chi phí khi dùng thật** | Mô phỏng **50 phiên** thật (`simulate-1.csv`, seed 42, `0/50` lỗi, dùng tỷ lệ đạt 88% của Lượt 2). **`gpt-4o-mini`:** `$0.00038`/task thành công (~10₫) · Thấp `$0.12` / Cơ sở (84 người) **`$0.26/tháng` (~6.558₫)** / Cao `$0.37` · **`$0.0031`/người/tháng (~78₫)**. Đối chiếu `gemini-3.1-flash-lite` (`$0.55/tháng`) & `gpt-6.2-sol` (`$3.93/tháng`). | `cost/cost-estimate.md`, `cost/simulate-1-summary.md` | ☑ |
| 7 | **Kết luận** | **GO (kèm 1 vòng iterate nhỏ cho 3 câu sót):** Bài toán thật (7/13 ngày KC sai ≥35%), vượt chuẩn đánh giá (88% tổng, 100% an toàn `tu_choi`), chi phí siêu rẻ (`$0.26/tháng` cho cả khoá 84 GV/Lab Coach). | Trang 1, 5, 6 | ☑ |
| 8 | **Nếu có thêm 1 tuần** | (1) Ép gắn header cảnh báo mẫu nhỏ `G10` bằng code deterministic (triệt tiêu regression `T22`); (2) Tách slot bắt buộc cho câu hỏi về video/lab cụ thể (`T07, T12`); (3) Phỏng vấn & pilot thực tế với 5–10 Giảng viên/Lab Coach + bật cache theo `(lesson_id, focus)` giảm thêm 70–85% chi phí. | `eval/report.md` mục 4 | ☑ |

## Phân công trình bày Demo (cả 4 thành viên đều nói)

| Trang | Người trình bày | Trọng tâm Q&A phụ trách |
|---|---|---|
| Trang 1–2 | **Hoàng Thế Phong** | Số liệu đào `data/preclass/`, công thức Impact & lý do loại 3 hướng kia |
| Trang 3–4 | **Trần Anh Dũng** & **Vũ Huy Hiệu** | Vì sao chọn Workflow cố định, 2 tầng guardrail, demo live + chạy câu lạ |
| Trang 5 | **Đỗ Lý Hoàng Nam** | Bộ 26 câu thử, 4 metric, phân tích 3 nhóm lỗi Lượt 1 → Lượt 2 & regression `T22` |
| Trang 6–8 | **Trần Anh Dũng** & **Hoàng Thế Phong** | Cách tính chi phí / task thành công, 3 kịch bản, kết luận GO & kế hoạch 1 tuần |
