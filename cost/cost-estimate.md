# Chi phí khi dùng thật

> Chạy thật bằng lệnh `python run.py simulate --rate-from eval/run-2.csv` (50 phiên, seed 42, 0 phiên lỗi).  
> Mọi con số trích trực tiếp từ `cost/simulate-1-summary.md` và `cost/simulate-1.csv`, tính theo **giá gói trả phí** chuẩn BTC (`further-reading/model-prices.md`, xem ngày 25/11/2026).

## 1. Đầu vào

- **Persona** (`cost/personas.yaml` — 3 kiểu người dùng, tổng `share = 1.0`):
  - `giang_vien_chinh` (25% · 4 phiên/tháng · 1 lượt/phiên) — *(tự ước tính theo lịch học GĐ1)*
  - `lab_coach_truc_lop` (55% · 8 phiên/tháng · 1 lượt/phiên) — *(tự ước tính theo lịch trực 2 buổi lab/tuần)*
  - `key_coach_lead` (20% · 15 phiên/tháng · 2 lượt/phiên) — *(tự ước tính theo vai trò điều phối nhiều lớp)*
- **Số người dùng thật** (3 kịch bản): thấp **40 người** *(tự ước tính — nhóm trực lab chính)* · cơ sở **84 người** *(22 giảng viên + 62 lab coach, nguồn: `data/training-ops/README.md`)* · cao **120 người** *(tự ước tính — mở rộng trợ giảng/khoá tiếp theo)*.
- **Giá 3 mức model** (USD / 1M token, từ `further-reading/model-prices.md`, xem ngày **25/11/2026**):
  - `gpt-4o-mini` (Nhỏ): vào **$0.15** · ra **$0.60** ([developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing))
  - `gemini-3.1-flash-lite` (Nhỏ): vào **$0.25** · ra **$1.50** ([ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing))
  - `gpt-6.2-sol` (Lớn): vào **$2.00** · ra **$10.00** ([developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing))
- **Tỉ lệ đạt dùng để tính:** **23/26 (88%)** — lượt `run-2@20261127-224608` (`eval/run-2.csv`, cùng model `gpt-4o-mini`).
- **Ghi chú đo token:** Đo token thật trên model **`gpt-4o-mini`** (trung bình 840–1.414 token vào, 274–471 token ra tùy persona), tính giá đối chiếu trên `gpt-4o-mini`, `gemini-3.1-flash-lite` và `gpt-6.2-sol` *(model khác bộ tách token có thể lệch nhẹ)*. Tỷ giá tham khảo: `1 USD = 25.400 ₫`.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · tóm tắt `cost/simulate-1-summary.md` · **50 phiên** (`0/50` lỗi) · **seed 42**.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| `giang_vien_chinh` | 17 | 1 | 863 | 304 | 0.9 | 3.2 |
| `lab_coach_truc_lop` | 24 | 1 | 840 | 274 | 0.9 | 3.2 |
| `key_coach_lead` | 9 | 2 | 1.414 | 471 | 1.6 | 5.6 |

| Model (giá $/1M token) | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (40 người) | / tháng — cơ sở (84 người) | / tháng — cao (120 người) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| **gpt-4o-mini** (`0.15 / 0.60`) | `$0.00033` (~8 ₫) | **`$0.00038`** (~10 ₫) | `$0.1230` (~3.123 ₫) | **`$0.2582`** (~6.558 ₫) | `$0.3689` (~9.369 ₫) | **`$0.0031`** (~78 ₫) |
| **gemini-3.1-flash-lite** (`0.25 / 1.50`) | `$0.00072` (~18 ₫) | **`$0.00081`** (~21 ₫) | `$0.2634` (~6.690 ₫) | **`$0.5531`** (~14.048 ₫) | `$0.7901` (~20.069 ₫) | **`$0.0066`** (~167 ₫) |
| **gpt-6.2-sol** (`2.00 / 10.00`) | `$0.0051` (~130 ₫) | **`$0.0058`** (~146 ₫) | `$1.87` (~47.578 ₫) | **`$3.93`** (~99.914 ₫) | `$5.62` (~142.734 ₫) | **`$0.0468`** (~1.189 ₫) |

*Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt (23/26 = 88%) — không coi như đạt 100%.*

## 3. So với impact

- **Impact / người / tháng (`spec.md` §2):** 12 buổi × 45 phút *(tự ước tính)* = **540 phút (~9 giờ/người/tháng)** chuẩn bị & tối ưu phần dẫn nhập đầu giờ cho giảng viên/lab coach (gián tiếp cải thiện trải nghiệm học của >700 học viên lớp L3).
- **Chi phí / người / tháng (cơ sở, model `gpt-4o-mini`):** **`$0.0031` (~78 ₫/người/tháng)** — cả khoá 84 giảng viên & lab coach tốn **`$0.26/tháng` (~6.558 ₫/tháng)**; ngay cả khi nâng lên model lớn `gpt-6.2-sol` cũng chỉ tốn **`$3.93/tháng` (~99.914 ₫/tháng)**.
- **Kết luận một dòng — đáng làm không:** **Rất đáng làm (GO)** — chi phí API gần như bằng 0 (`< $0.30/tháng` với `gpt-4o-mini`) nhờ kiến trúc Workflow cố định tổng hợp số bằng code trước khi gọi LLM đúng 1 lần, trong khi giá trị tiết kiệm thời gian giảng dạy là rất lớn.

## 4. Phân tích thêm (chi phí ngoài model & đòn bẩy tối ưu)

- **Chi phí ngoài model:** Script tổng hợp `build_lesson_signals.py` chạy định kỳ trước buổi học tốn < 2 giây CPU (gần như 0$); giờ công giảng viên duyệt bản tóm tắt ≤ 2 phút/buổi.
- **Đòn bẩy giảm chi phí khi mở rộng quy mô lớn:** Caching câu trả lời theo cặp `(lesson_id, focus)` giữa nhiều lab coach cùng hỏi về cùng 1 ngày học (ví dụ 15 coach cùng hỏi `Day05` trước buổi lab) có thể giảm tiếp **70–85%** tổng số lượt gọi API.
