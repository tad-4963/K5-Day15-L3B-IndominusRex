# Reflection — Trần Anh Dũng

> Mã học viên: `2A202604037` · Vai trò: Đội trưởng (Nhóm IndominusRex · L3B · Track A)

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Đảm nhiệm vai trò Đội trưởng (Cặp 1): khởi tạo repo công khai, phân công nhóm (`TEAMS.md`, `canvas.md`), thiết kế kiến trúc Workflow cố định 3 bước và viết `spec.md` (§0, §3–§10, chốt cứng chuẩn "đạt" §7 trước CP2).
   - Trực tiếp nối OpenAI API (`gpt-4o-mini`) trong `codebase/ai.py`, viết và tinh chỉnh `SYSTEM` prompt ở `codebase/agent.py`, nâng cấp giao diện Dashboard thống kê & Trợ lý AI (`codebase/app.py`, `codebase/demo.html`), và dựng bộ slide 8 trang (`demo-slides.html`, `demo-slides.pdf`).
   - Trực tiếp chạy đánh giá Lượt 1 (`eval/run-1.csv`, `19/26 = 73%`), triển khai cải tiến Lượt 2 (`eval/run-2.csv`, `23/26 = 88%`), chạy mô phỏng chi phí 50 phiên (`cost/simulate-1.csv`), hoàn thiện báo cáo (`eval/report.md`, `cost/cost-estimate.md`), quay video demo và nộp đủ 4 mốc CP1–CP4 (các commit chính: `c5539a2`, `a34f995`, `8324908`, `7aa95b8`, `df04f28`).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng trợ lý AI (Antigravity / LLM) để hỗ trợ viết script đào dữ liệu `data/preclass/`, rà soát khung tài liệu, gợi ý code nối API, xây giao diện web demo và dàn khung slide HTML.
   - Tuy nhiên mình phải kiểm soát và sửa lại khá nhiều đầu ra từ AI: (1) phát hiện và mạnh tay loại bỏ toàn bộ số liệu hardcode không khớp CSV gốc và các file phỏng vấn chưa xác thực do AI sinh nháp (`P1–P3.md`) để giữ nguyên tắc trung thực dữ liệu tuyệt đối; (2) sửa lại độ lệch số liệu ở 4 câu benchmark (`T02, T07, T08, T11`) cho khớp 100% với `data/lesson_signals_agg.json` trước khi khóa CP2; (3) yêu cầu thiết kế lại giao diện bỏ emoji cơ bản, sửa lỗi regex lookahead sinh thẻ trắng trên `demo.html` và chỉnh lại giọng văn trợ lý bớt máy móc, gần gũi với giảng viên hơn.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Ấn tượng nhất với mình là **lỗi trượt ở `T18` và `T23` của Lượt 1** (`run-1@20261127-223811`) cùng lỗi chặn oan **`T19`**: ở `T18`/`T23`, vì code chỉ truyền chuỗi `knowledge_check — X: 8/15 (53.3%)` mà thiếu chữ `"SAI"`, `gpt-4o-mini` đã hiểu ngược thành *"tỷ lệ đúng thấp 53.3%"* và *"100% tỷ lệ thành công"* — một lỗi cực kỳ nguy hiểm nếu giảng viên đọc nhầm; còn ở `T19`, regex `_INJECTION_RE` (`bo qua.{0,80}huong dan`) lại chặn oan câu hỏi hợp lệ *"tình hình bỏ qua mini lab... hướng dẫn thực hành"*.
   - Bài học lớn nhất mình rút ra là **không bao giờ đoán cảm tính rằng prompt/guardrail đã đủ tốt**: phải chạy bộ câu thử thật mới thấy được các lỗi tinh vi như đảo ngược ngữ nghĩa nhãn dữ liệu, false positive ở regex hay regression ở `T22` (Lượt 2 quên nhắc cảnh báo mẫu nhỏ `n=4`). Việc tường minh hóa dữ liệu đầu vào từ tầng code (ghi rõ `"lượt SAI"`) và kiểm soát rủi ro bằng logic deterministic quan trọng hơn rất nhiều so với việc viết prompt thật dài.
