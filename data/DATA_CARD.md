# Data card — Pre-Class Bottleneck Brief (bản CP2)

## Dataset dự kiến: log hành vi pre-class đã tổng hợp

| Thuộc tính | Mô tả |
|---|---|
| Dùng để làm gì | Cung cấp số liệu cấp bài học cho `get_lesson_signals` và bộ câu thử của bản chạy thử. |
| Nguồn | BTC cấp: `data/preclass/answers.csv`, `events.csv`, `chat.csv`; đối chiếu schema bằng `column_dictionary.csv`, loại sự kiện bằng `event_types.csv` và quy tắc bằng `README.md`. |
| Xử lý | `scripts/build_lesson_signals.py` gom theo Day01–Day13. KC chỉ tính câu có `was_correct=True/False`, `lan_thu=1` và nguồn `video_quiz` hoặc `pre_post_post`. Lab tính theo người có sự kiện mở/hoàn tất từng `lab_key`; `skip` lấy từ `lab_completed.data.skipped`, `incomplete` là đã vào nhưng chưa hoàn tất/bỏ qua. Video hỏi nhiều lấy từ `chat.transcript`; missing context lấy từ `agent_replied.data.missing_context`. |
| Quy mô | Nguồn ghi 721 tài khoản, 436 người có hoạt động; `answers.csv` 3.776 dòng, `events.csv` 107.709 dòng, `chat.csv` 1.260 dòng. Bản tổng hợp có 13 ngày. Số active theo ngày được đếm distinct từ sự kiện/answers/chat thuộc ngày đó (ví dụ Day01: 417; Day05: 134; Day12: 26). |
| Phiên bản / ngày lấy | Data pack ghi khoảng thời gian 05/11/2026–25/11/2026; file tổng hợp được tạo bằng `python scripts/build_lesson_signals.py`. |
| Nhãn | Dữ liệu hành vi thật đã được BTC thay mã và loại thông tin nhận dạng trực tiếp; mã giả danh chỉ dùng tạm trong bộ nhớ để đếm distinct, không xuất ra JSON. |
| Giới hạn | Mẫu số KC là số câu trả lời hợp lệ lần đầu cho từng KC; mẫu số lab là số người có event lab đó, không phải toàn bộ active trong ngày. Người mở lab nhưng chưa có event kết thúc được tính incomplete. Không phân tích nguyên nhân hay nội dung chữ chat (nguồn chỉ có độ dài). Dữ liệu ngày bắt đầu ghi khác nhau; active theo ngày không đồng nghĩa số người có tài khoản/hoạt động toàn khóa. |

## Ranh giới riêng tư

Không đưa CSV gốc lên repo. Chỉ chia sẻ JSON tổng hợp sau khi kiểm tra không chứa mã học viên hay nội dung chat. Việc xóa mã khỏi output không thay thế bước kiểm tra nguồn hoặc rà soát kết quả trước khi công bố.
