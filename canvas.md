# Canvas — IndominusRex · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".
> Track F: chép thêm thẻ đề của nhóm (khung trong file track F) xuống dưới bảng này.

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A (EdTech) — A1 mở rộng: Báo cáo "Bản đồ điểm nghẽn lớp học trước buổi dạy" cho Giảng viên / Lab Coach từ nhật ký pre-class |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Giảng viên và Lab Coach / Key Coach chuẩn bị nội dung ôn tập và dẫn nhập trước mỗi buổi học/lab lớp L3 (khoá AI20K) |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Giảng viên và Lab Coach trước buổi học không biết trong hơn 700 học viên, lớp đang sai nặng nhất ở khái niệm nào hay bỏ dở bước mini lab nào trên trang pre-class (dữ liệu nằm rời rạc trong hàng chục nghìn dòng log), khiến phần mở đầu dễ giảng dàn trải nội dung lớp đã hiểu và bỏ sót đúng chỗ 40–80% học viên đang vướng. |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | **Nguồn chính (đào `data/preclass/` — đã bắt đầu):** 436/721 học viên hoạt động, bài ôn tập cuối ngày sai tới 80% ở một số KC cốt lõi (`ai_product_canvas` 12/15, `feedback_signal_types` 8/15 = 53,3%, `react_reasoning_acting_pattern` 9/18 = 50%), 22,5% lượt mini lab bị bấm Skip (102/453), 37,1% phiên xem video phải hỏi lặp ≥3 lần. **Nguồn kiểm chéo (sẽ làm trước CP3):** Phỏng vấn ≥3 Lab Coach / Key Coach / Giảng viên tại lớp chiều T6 để xác nhận mức độ cần thiết và thời gian chuẩn bị thực tế. |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một giảng viên hoặc lab coach · chuẩn bị trước buổi học Day X · công cụ code tổng hợp tỷ lệ sai KC, mini lab bị bỏ qua và video bị hỏi nhiều từ log pre-class để AI quyết định xếp hạng Top 3 điểm nghẽn (kèm mức tin cậy) và đề xuất 1 hoạt động gỡ vướng 5–10 phút · giảng viên duyệt và đưa đúng trọng tâm vào đầu buổi học. |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | **AI gợi ý, người quyết (Giảng viên / Lab Coach duyệt)** — vì giảng viên quyết định nội dung giảng dạy, và log hành vi không chứa nội dung chữ học viên gõ nên AI chỉ tổng hợp tín hiệu & đề xuất giả thuyết để người kiểm chứng. |
| 7 | Phân công có tên | Cặp 1 (Trần Anh Dũng, Vũ Huy Hiệu): kiến trúc workflow, script tổng hợp data ẩn danh (`lesson_signals_agg.json`), tools & bản chạy thử nối model thật. Cặp 2 (Đỗ Lý Hoàng Nam, Hoàng Thế Phong): đào data chi tiết, phỏng vấn ≥3 Lab Coach/GV, bộ câu thử 20–30 câu, chấm eval, mô phỏng chi phí & slide. (Cả 4 người cùng tham gia phỏng vấn/đọc lỗi lượt 1 và review chéo.) |
| — | *(CP2)* Đã đổi gì so với CP1 | Giữ nguyên Track A & lát cắt Pre-Class Bottleneck Brief; chốt kiến trúc Workflow cố định 3 bước (xóa hoàn toàn mã `hv` ở tầng dữ liệu tổng hợp `data/lesson_signals_agg.json`, tính % bằng code, chặn soi cá nhân & gắn cờ mẫu nhỏ G10), chốt chuẩn "đạt" tại `spec.md` §7 và bổ sung trích dẫn phỏng vấn Lab Coach/GV đầu tiên. |
