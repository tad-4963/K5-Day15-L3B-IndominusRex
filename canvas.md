# Canvas — IndominusRex · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A (EdTech) — A1 mở rộng: Báo cáo "Bản đồ điểm nghẽn lớp học trước buổi dạy" cho Giảng viên / Lab Coach từ nhật ký pre-class |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Giảng viên và Lab Coach / Key Coach chuẩn bị nội dung ôn tập và dẫn nhập trước mỗi buổi học/lab lớp L3 (khoá AI20K) |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Giảng viên và Lab Coach trước buổi học không biết trong hơn 700 học viên, lớp đang sai nặng nhất ở khái niệm nào hay bỏ dở bước mini lab nào trên trang pre-class (dữ liệu nằm rời rạc trong hàng chục nghìn dòng log), khiến phần mở đầu dễ giảng dàn trải nội dung lớp đã hiểu và bỏ sót đúng chỗ 40–80% học viên đang vướng. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | **Nguồn 1 (Đào data `data/preclass/` — tái lập bằng `python scripts/mine_evidence.py`):** 436/721 (60,5%) học viên active; 7/13 ngày có KC (`n≥5`) sai ≥35% (Day05 `ai_product_canvas` 12/15 = 80,0%; Day06 `label_agreement_beyond_raw_percent` 6/7 = 85,7%; Day03 `agentic_fit_scoring_decision` 12/20 = 60,0%); 6/13 ngày có mini lab (`open≥10`) bị skip+incomplete ≥40% (Day07 `d07-lab-ngan-sach-context` 7/12 = 58,3%); drop-off từ 417 (Day01) xuống 26 (Day12).<br>**Nguồn 2 (Đang triển khai trước CP3):** Phỏng vấn ≥3 Lab Coach / Giảng viên tại lớp (ghi log tại `evidence/interviews/P1.md`–`P3.md`) để kiểm chéo và bổ sung trích dẫn nguyên văn thật. |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một giảng viên hoặc lab coach · chuẩn bị trước buổi học Day X · công cụ code tổng hợp tỷ lệ sai KC, mini lab bị bỏ qua và video bị hỏi nhiều từ log pre-class để AI quyết định xếp hạng Top 3 điểm nghẽn (kèm mức tin cậy) và đề xuất 1 hoạt động gỡ vướng 5–10 phút · giảng viên duyệt và đưa đúng trọng tâm vào đầu buổi học. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | **AI gợi ý, người quyết (Giảng viên / Lab Coach duyệt)** — vì giảng viên quyết định nội dung giảng dạy, và log hành vi không chứa nội dung chữ học viên gõ nên AI chỉ tổng hợp tín hiệu & đề xuất giả thuyết để người kiểm chứng. |
| 7 | Phân công có tên | Cặp 1: Trần Anh Dũng (Đội trưởng: Kiến trúc, Model, Spec), Vũ Huy Hiệu (Data pipeline, Tools, App). Cặp 2: Đỗ Lý Hoàng Nam (Phỏng vấn, Metric, Benchmark), Hoàng Thế Phong (Data mining, Impact, Cost, Slide). |
| — | *(CP2)* Đã đổi gì so với CP1 | Giữ nguyên Track A & lát cắt Pre-Class Bottleneck Brief; hoàn thiện script đào data thật (`scripts/mine_evidence.py`, `data/lesson_signals_agg.json`), chốt kiến trúc Workflow cố định 3 bước trong `spec.md` §4, chốt 16 câu thử + 4 metric + chuẩn "đạt" tại `spec.md` §7, và chạy thông khung bản chạy thử `python run.py` chế độ giả. |
