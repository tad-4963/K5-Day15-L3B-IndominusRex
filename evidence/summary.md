# Tổng hợp bằng chứng pain

> Dùng cho: Mốc CP3 (10:00 Thứ Bảy 28/11) · Chấm tại Rubric R1.  
> Nguồn chính đạt ngưỡng: **Nguồn 1 — Đào dữ liệu hành vi thật `data/preclass/`** (436/721 học viên hoạt động, Day01–Day13, tái lập bằng `python scripts/mine_evidence.py`).

---

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| **Đào data** (`x/N`, `%`, cách đếm chạy lại được, ≥5 ví dụ cụ thể) | ☑ **ĐẠT** | `evidence/data-mining.md`, `scripts/mine_evidence.py`, `data/lesson_signals_agg.json` |
| **Phỏng vấn** (≥3 người ngoài nhóm, đúng người dùng) | ☐ Tạm bỏ | Nhóm chưa hoàn tất phỏng vấn trực tiếp đủ 3 Giảng viên/Lab Coach tại mốc CP3 (giữ nguyên nguyên tắc không dùng dữ liệu phỏng vấn giả định). |
| **Khảo sát** (≥20 người ngoài nhóm) | ☐ Dự phòng | `evidence/survey/questions.md` *(chưa phát form)* |

---

## 2. Số chính (truy ngược 100% về `python scripts/mine_evidence.py` và `data/lesson_signals_agg.json`)

- **Quy mô hoạt động toàn khoá:** **436 / 721 (60,5%)** tài khoản học viên có hoạt động trên `preclass-online.com` (05/11–25/11/2026, Day01–Day13).
- **Điểm nghẽn kiến thức (Knowledge Check lần thử đầu):** Tổng tỷ lệ sai chung là **401 / 1.975 (20,3%)**, nhưng phân bố cực kỳ không đều — có tới **7 / 13 ngày** xuất hiện ít nhất 1 khái niệm (`n ≥ 5`) có tỷ lệ sai **≥ 35%**:
  - `Day06` — `label_agreement_beyond_raw_percent`: **6 / 7 (85,7%)** · tổng KC Day06 sai **41 / 93 (44,1%)**
  - `Day05` — `ai_product_canvas`: **12 / 15 (80,0%)** · `feedback_signal_types`: **8 / 15 (53,3%)** · tổng KC Day05 sai **55 / 180 (30,6%)**
  - `Day03` — `agentic_fit_scoring_decision`: **12 / 20 (60,0%)**
  - `Day07` — `tool_definition_context_cost`: **6 / 10 (60,0%)**
  - `Day04` — `cot_task_fit`: **11 / 27 (40,7%)**
  - `Day08` — `multi_agent_token_cost`: **4 / 10 (40,0%)**
  - `Day01` — `chatbot_is_app_around_model`: **16 / 41 (39,0%)**
- **Điểm nghẽn thực hành (Mini Lab):** **6 / 13 ngày** có bài mini lab (`open ≥ 10` học viên distinct) có tỷ lệ `skip + incomplete` **≥ 40%**:
  - `Day07` — `d07-lab-ngan-sach-context`: **7 / 12 (58,3%)** (5 skip + 2 incomplete)
  - `Day06` — `d06-lab-tram-gate`: **9 / 16 (56,2%)** (3 skip + 6 incomplete)
  - `Day09` — `d09-lab-soi-giam-khao`: **6 / 11 (54,5%)** (3 skip + 3 incomplete)
  - `Day08` — `d08-lab-crash-test`: **11 / 21 (52,4%)** (8 skip + 3 incomplete)
  - `Day01` — `d01-lab-ban-la-llm`: **31 / 72 (43,1%)** (15 skip + 16 incomplete)
  - `Day11` — `d11-lab-bo-ba-nguy-hiem`: **4 / 10 (40,0%)** (3 skip + 1 incomplete)
- **Sụt giảm mẫu số về cuối khoá (Drop-off):** Số học viên active giảm từ **417** (`Day01`) xuống **26** (`Day12`, giảm **93,8%**) và **50** (`Day13`, giảm **88,0%**). Từ `Day09` đến `Day13` đều **không có KC nào đạt `n ≥ 5`** → minh chứng trực tiếp cho nhu cầu cảnh báo độ tin cậy mẫu nhỏ (HAX G10).

---

## 3. Năm ví dụ cụ thể từ dữ liệu thật (`data/lesson_signals_agg.json`)

1. **`Day05` (`ai-product-thinking`, 134 active):** KC `ai_product_canvas` có **12/15 lượt trả lời lần đầu sai (80,0%)**, `feedback_signal_types` sai **8/15 (53,3%)**, và video `Day05/d05-r2-v01.txt` phát sinh **25 lượt** câu hỏi `video_question`. *(Nguồn: `data/lesson_signals_agg.json` → `days.Day05`)*
2. **`Day06` (`data-engineering`, 103 active):** Tổng tỷ lệ sai KC lần đầu cao nhất nhóm ngày có mẫu khá (**41/93 = 44,1%**), đứng đầu là `label_agreement_beyond_raw_percent` (**6/7 = 85,7%**); đồng thời mini lab `d06-lab-tram-gate` có **9/16 học viên (56,2%)** bấm skip hoặc bỏ dở. *(Nguồn: `data/lesson_signals_agg.json` → `days.Day06`)*
3. **`Day07` (`retrieval-context`, 86 active):** Mini lab `d07-lab-ngan-sach-context` có **7/12 học viên (58,3%)** bấm skip (5) hoặc chưa hoàn thành (2); đồng thời KC `tool_definition_context_cost` sai **6/10 (60,0%)**. *(Nguồn: `data/lesson_signals_agg.json` → `days.Day07`)*
4. **`Day01` (`ai-llm-foundation`, 417 active):** KC `chatbot_is_app_around_model` sai **16/41 (39,0%)**, mini lab `d01-lab-ban-la-llm` có **31/72 học viên (43,1%)** skip/incomplete, và riêng video `Day01/d01-r1-v02.txt` có **115 lượt** hỏi `video_question`. *(Nguồn: `data/lesson_signals_agg.json` → `days.Day01`)*
5. **`Day12` (`ai-sdlc-coding-agent`, 26 active):** Chỉ có **26 học viên active**, **0 KC đạt `n ≥ 5`**, mini lab chỉ có **3 người mở** (`d12-lab-loi-dan-o-khoa`: 2/3 skip) — ví dụ điển hình buộc hệ thống phải gắn cảnh báo mẫu nhỏ (G10) thay vì kết luận cho cả lớp. *(Nguồn: `data/lesson_signals_agg.json` → `days.Day12`)*

---

## 4. Giới hạn bằng chứng & Điểm còn thiếu (khai trung thực)

- Dữ liệu `data/preclass/` chứng minh rất rõ **hành vi kẹt cục bộ** (học viên sai nặng ở đâu, bỏ dở lab nào, video nào bị hỏi nhiều, ngày nào mẫu nhỏ), nhưng **không chứa nội dung chữ chat** và **không trực tiếp đo thời gian giảng viên/lab coach tốn khi chuẩn bị**.
- Nhóm tạm bỏ phần phỏng vấn trực tiếp tại mốc CP3; nếu có điều kiện phỏng vấn bổ sung người thật trước CP4 sẽ bổ sung log vào `evidence/interviews/` và ghi nhận trong changelog `spec.md` §10.

---

## 5. Kết luận

- **Giả thuyết ([evidence/hypothesis.md](hypothesis.md)):** **ĐƯỢC XÁC NHẬN MỘT PHẦN (về phía dữ liệu hành vi — vượt ngưỡng đặt ra).**
  - Ngưỡng đặt trước trong giả thuyết: *"có ≥5 ngày học xuất hiện KC sai lần đầu ≥35% hoặc mini lab bị bỏ qua/bỏ dở ≥30%"* → thực tế đạt **7/13 ngày** có KC sai ≥35% và **6/13 ngày** có mini lab (`open ≥ 10`) skip+incomplete ≥40%.
  - Phần xác nhận định tính từ phỏng vấn trực tiếp GV/Lab Coach: **chưa thực hiện** ở CP3; các giả định về số phút tiết kiệm trong bảng Impact (`spec.md` §2) được ghi rõ là *(tự ước tính)*.
