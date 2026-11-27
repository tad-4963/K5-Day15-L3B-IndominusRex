# Tổng hợp bằng chứng pain

> Người phụ trách: **Hoàng Thế Phong (2A202603832) & Đỗ Lý Hoàng Nam — Cặp 2**  
> Dùng cho: Mốc CP3 (10:00 Thứ Bảy 28/11) · Chấm tại Rubric R1.  
> Đối chiếu hai nguồn độc lập: **Nguồn 1 (Đào data log 436 học viên)** và **Nguồn 2 (Phỏng vấn sâu 3 Giảng viên & Lab Coach)**.

---

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| **Đào data** (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ ĐẠT | `evidence/data-mining.md` & `data/lesson_signals_agg.json` |
| **Phỏng vấn** (≥3 người ngoài nhóm, đúng người dùng) | ☑ ĐẠT | `evidence/interviews/P1.md`, `P2.md`, `P3.md` |
| **Khảo sát** (Mẫu form chuẩn bị mở rộng) | ☐ Dự phòng | `evidence/survey/questions.md` & `.docx` |

---

## 2. Số chính

- **Đào data:** **382 / 436 (87.6%)** học viên active toàn khoá từng gặp ít nhất một bài Knowledge Check sai $\ge 50\%$ hoặc bỏ dở bài tập Mini Lab. Cụ thể: Day05 có 63.5% học viên sai State Machine (198/312), Day07 có 54.1% sai Retrieval Context (145/268), Day12 có 62.7% học viên kẹt Mini Lab SDLC (89/142).
- **Phỏng vấn:** **3 / 3** người được phỏng vấn (100%) đều gặp pain nghiêm trọng trong 1 tháng qua:
  - P1 (Key Coach / Day Lead): gặp **6 – 8 lần/tháng**, lần gần nhất mất **30 phút** chữa cháy.
  - P2 (Giảng viên chính): gặp **4 lần/tháng** (mọi buổi lý thuyết), lần gần nhất mất **35 – 40 phút** giảng lại kiến thức nền.
  - P3 (Lab Coach trực bàn): gặp **7 – 8 lần/tháng**, lần gần nhất mất **25 phút** rà soát từng bàn.

### Bảng chi tiết từng người được phỏng vấn:

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| **P1** | Key Coach / Day Lead điều phối ca lab | Có | 6 – 8 lần | 30 phút (Day05 / Day12) | Lướt nhóm Zalo, hỏi miệng vài bạn đầu giờ |
| **P2** | Giảng viên đứng lớp chính (lý thuyết) | Có | 4 lần | 35 – 40 phút (Day07) | Chuẩn bị slide theo giáo án cố định, hỏi miệng đầu giờ |
| **P3** | Lab Coach hướng dẫn thực hành từng bàn | Có | 7 – 8 lần | 20 – 25 phút (Day02 / Day09) | Đi từng bàn kiểm tra xem ai chưa chạy được lab |

---

## 3. Năm trích dẫn nguyên văn minh chứng nỗi đau

1. *"Nhiều hôm vào ca lab mới thấy phần lớn các bạn kẹt đúng một lỗi state transition từ bài pre-class tối qua, cả buổi coach phải đi giải thích lại cùng một lỗi cho từng bàn, cháy sạch giáo án lab."* — **P1 (Key Coach L3B)**
2. *"Nếu trước buổi học 30 phút tôi biết cả lớp đang hiểu sai ở khái niệm nào với tỷ lệ bao nhiêu %, tôi chỉ cần 5 phút đầu giờ chiếu 1 ví dụ phản trực giác là gỡ xong, thay vì để học viên loay hoay cả buổi."* — **P2 (Giảng viên chính)**
3. *"Ở bài Day02, hơn nửa lớp bỏ dở mini lab vì kẹt logic gate. Nếu đầu giờ GV hoặc Coach dẫn nhập nói trước lỗi này thì các bạn đã không bị tắc đồng loạt và gọi coach liên tục."* — **P3 (Lab Coach trực bàn L3A)**
4. *"Đừng đưa mã số hay tên học viên yếu lên báo cáo. Việc đó làm các bạn tự ti. Coach chỉ cần biết tỷ lệ chung và loại lỗi phổ biến để tụi mình chủ động nhắc trước cả lớp."* — **P3 (Lab Coach L3A - xác nhận nguyên tắc Guardrail)**
5. *"Dữ liệu log pre-class: Day05 có 198/312 học viên (63.5%) làm sai Knowledge Check về Agent Loop; Day12 có 89/142 học viên (62.7%) không hoàn thành Mini Lab SDLC."* — **Trích xuất từ `data/lesson_signals_agg.json`**

---

## 4. Các nguồn có khớp nhau không

- **Dữ liệu log (Data Mining)** chỉ ra: Học viên vấp rất nặng ở các bài học mang tính trừu tượng hoặc pipeline phức tạp (Day05: State Machine, Day07: Retrieval Vector, Day12: SDLC Workflow) với tỷ lệ sai/kẹt từ 50% đến 65%.
- **Người dùng thực tế (Phỏng vấn)** xác nhận: Giảng viên và Coach đều gặp chính xác các điểm nghẽn tại Day02, Day05, Day07; họ luôn bị động và mất 25–40 phút đầu giờ giải thích lại kiến thức nền, dẫn đến cháy giáo án buổi lab.
- **Mức độ khớp:** **Khớp nhau 100% về bản chất và vị trí điểm nghẽn.** Nguồn phỏng vấn bổ sung thêm bức tranh thực tế mà log không có: cảm xúc áp lực của coach khi bị quá tải câu hỏi, và yêu cầu nghiêm ngặt về quyền riêng tư (không nêu tên/mã học viên cá nhân).

---

## 5. Kết luận

- Giả thuyết tại [`evidence/hypothesis.md`](file:///Users/phong/Desktop/BaiTapVinUni/K5-Day15-L3B-IndominusRex/evidence/hypothesis.md): **HOÀN TOÀN ĐÚNG.**
- Giảng viên và Lab Coach thực sự gặp nỗi đau lớn khi chuẩn bị dẫn nhập và điều phối ca lab do thiếu công cụ tổng hợp tự động các điểm nghẽn từ log pre-class.
- **Ranh giới bài toán được củng cố:** Báo cáo phải ngắn gọn (đọc $\le 2$ phút), số liệu chính xác $x/N (\%)$, có cảnh báo mẫu nhỏ khi $n < 150$, tuyệt đối không lộ danh tính học viên, và luôn đi kèm 1 hoạt động dẫn nhập 5–10 phút đầu giờ.

---

## 6. Lịch hẹn kiểm thử người dùng (Dùng cho phần Bonus +5 điểm)

| Khách thể | Vai trò | Giờ hẹn kiểm thử | Trạng thái |
|---|---|---|---|
| **P1** | Key Coach / Day Lead | 11:00 Thứ Bảy 28/11/2026 | Đã xác nhận |
| **P2** | Giảng viên đứng lớp chính | 11:30 Thứ Bảy 28/11/2026 | Đã xác nhận |
| **P3** | Lab Coach trực bàn | 12:00 Thứ Bảy 28/11/2026 | Đã xác nhận |
