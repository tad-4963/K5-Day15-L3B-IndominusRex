# Đào data — cách đếm và kết quả

> Dùng cho: Bằng chứng **Nguồn 1** chứng minh điểm nghẽn pre-class phân bố lệch mạnh theo từng bài học (`Day01`–`Day13`) và sụt giảm mẫu số mạnh về cuối khoá.  
> Script tái lập: `python scripts/mine_evidence.py` (đọc trực tiếp từ `data/lesson_signals_agg.json`, được tổng hợp từ `data/preclass/*.csv` bằng `scripts/build_lesson_signals.py`).

---

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Bộ dữ liệu hành vi pre-class thật đã ẩn danh do BTC cấp (`data/preclass/`: `answers.csv`, `events.csv`, `chat.csv`, giai đoạn 05/11–25/11/2026, 13 ngày học `Day01`–`Day13`), tổng hợp không chứa mã `hv` tại `data/lesson_signals_agg.json` (chi tiết xử lý: `data/DATA_CARD.md`).
- **Đếm gì:**
  1. Số học viên có hoạt động theo từng ngày (`active_learners`).
  2. Tỷ lệ trả lời sai ở lần thử đầu (`lan_thu = 1`, `was_correct = True/False`, nguồn `video_quiz` và `pre_post_post`) cho từng `kc_code`.
  3. Tỷ lệ học viên bấm bỏ qua (`skip`) hoặc mở nhưng chưa hoàn thành (`incomplete`) theo từng `lab_key` (mẫu số = số học viên distinct có sự kiện mở/tham gia lab đó).
- **Mẫu số (N):**
  - Tổng tài khoản: **721** · Học viên có hoạt động toàn khoá: **436/721 (60,5%)**.
  - Với từng `kc_code`: mẫu số là tổng lượt trả lời hợp lệ lần đầu của KC đó (chỉ xếp hạng các KC có `n ≥ 5` để tránh nhiễu mẫu quá nhỏ).
  - Với từng `lab_key`: mẫu số là số học viên distinct đã mở lab đó.

---

## 2. Đọc trước, đếm sau

Sau khi đọc từ điển cột (`column_dictionary.csv`, `event_types.csv`) và 30 dòng đầu của từng bảng, phát hiện 3 kiểu hành vi rõ rệt:
- **Kiểu 1 (Điểm nghẽn tập trung cục bộ vào từng KC lõi):** Tỷ lệ sai chung toàn bộ KC lần đầu chỉ khoảng 20,3%, nhưng một số khái niệm cụ thể bị sai rất nặng (40–85%), không phân bố đều giữa các ngày.
- **Kiểu 2 (Mini lab bị bỏ qua / bỏ dở cao):** Ở nhiều bài thực hành, 40–58% học viên đã mở lab nhưng bấm `skip` hoặc thoát giữa chừng (`incomplete`).
- **Kiểu 3 (Sụt giảm tương tác mạnh về các ngày cuối):** Số học viên active giảm từ 417 (Day01) xuống 26 (Day12), khiến các ngày `Day09`–`Day13` không có KC nào đủ `n ≥ 5` → bắt buộc phải gắn cờ cảnh báo mẫu nhỏ (HAX G10).

---

## 3. Kết quả khai phá (Data Mining)

Tái lập bằng lệnh: `python scripts/mine_evidence.py`

| Ngày | Active | Tổng KC sai lần 1 (`x/N`) | KC khó nhất (`n ≥ 5`) | Mini Lab có tỷ lệ `skip + incomplete` cao nhất |
|---|---:|---|---|---|
| **Day01** | 417 | 71/439 (16,2%) | `chatbot_is_app_around_model` (**16/41 = 39,0%**) | `d01-lab-ban-la-llm` (skip 15 + inc 16 / 72 = **43,1%**) |
| **Day02** | 180 | 43/263 (16,3%) | `select_rule_workflow_agent_level` (8/23 = 34,8%) | `d02-lab-cham-gate` (skip 2 + inc 1 / 4 = 75,0% — *mẫu nhỏ*) |
| **Day03** | 154 | 52/230 (22,6%) | `agentic_fit_scoring_decision` (**12/20 = 60,0%**) | `d03-lab-can-agentic-fit` (skip 6 + inc 7 / 38 = 34,2%) |
| **Day04** | 145 | 50/316 (15,8%) | `cot_task_fit` (**11/27 = 40,7%**) | `d04-lab-soi-system-prompt` (skip 3 + inc 0 / 8 = 37,5% — *mẫu nhỏ*) |
| **Day05** | 134 | 55/180 (30,6%) | `ai_product_canvas` (**12/15 = 80,0%**) | `d05-lab-eval-spec` (skip 1 + inc 4 / 20 = 25,0%) |
| **Day06** | 103 | 41/93 (44,1%) | `label_agreement_beyond_raw_percent` (**6/7 = 85,7%**) | `d06-lab-tram-gate` (skip 3 + inc 6 / 16 = **56,2%**) |
| **Day07** | 86 | 26/123 (21,1%) | `tool_definition_context_cost` (**6/10 = 60,0%**) | `d07-lab-ngan-sach-context` (skip 5 + inc 2 / 12 = **58,3%**) |
| **Day08** | 109 | 20/137 (14,6%) | `multi_agent_token_cost` (**4/10 = 40,0%**) | `d08-lab-crash-test` (skip 8 + inc 3 / 21 = **52,4%**) |
| **Day09** | 75 | 9/36 (25,0%) | *không có KC n ≥ 5* | `d09-lab-soi-giam-khao` (skip 3 + inc 3 / 11 = **54,5%**) |
| **Day10** | 44 | 5/48 (10,4%) | *không có KC n ≥ 5* | `d10-lab-van-hanh-pilot` (skip 1 + inc 1 / 4 = 50,0% — *mẫu nhỏ*) |
| **Day11** | 43 | 11/48 (22,9%) | *không có KC n ≥ 5* | `d11-lab-bo-ba-nguy-hiem` (skip 3 + inc 1 / 10 = **40,0%**) |
| **Day12** | 26 | 6/36 (16,7%) | *không có KC n ≥ 5* | `d12-lab-loi-dan-o-khoa` (skip 2 + inc 0 / 3 = 66,7% — *mẫu nhỏ*) |
| **Day13** | 50 | 12/26 (46,2%) | *không có KC n ≥ 5* | `d13-lab-pilot-trung-thuc` (skip 1 + inc 2 / 3 = 100,0% — *mẫu nhỏ*) |

### Chỉ số tổng hợp chính
1. **Tổng tỷ lệ sai KC lần đầu (Day01–Day13):** **401/1.975 (20,3%)**, nhưng có tới **7/13 ngày** xuất hiện KC (`n ≥ 5`) sai **≥ 35%** (đỉnh điểm 80,0% ở Day05 và 85,7% ở Day06).
2. **Tỷ lệ bỏ qua / bỏ dở Mini Lab:** **6/13 ngày** có bài mini lab (`open ≥ 10` học viên) bị `skip + incomplete` **≥ 40%** (đỉnh điểm 58,3% ở Day07 và 56,2% ở Day06).
3. **Sụt giảm mẫu số mạnh (Drop-off):** Từ **417** học viên active (Day01) giảm xuống **26** (Day12, giảm **93,8%**) và **50** (Day13, giảm **88,0%**). 3 ngày có `active < 50` (`Day10: 44`, `Day11: 43`, `Day12: 26`) → minh chứng trực tiếp cho nhu cầu cảnh báo mẫu nhỏ (HAX G10).

---

## 4. Năm ví dụ cụ thể từ dữ liệu thật (`data/lesson_signals_agg.json`)

1. **Ví dụ 1 (`Day05` — `ai_product_canvas`):** **12/15 lượt trả lời lần đầu bị sai (80,0%)**, góp phần đẩy tỷ lệ sai chung Day05 lên **55/180 (30,6%)** trên 134 học viên active.
2. **Ví dụ 2 (`Day06` — `label_agreement_beyond_raw_percent` & `d06-lab-tram-gate`):** Tỷ lệ sai KC chung cao nhất các ngày có mẫu khá (**41/93 = 44,1%**), riêng `label_agreement_beyond_raw_percent` sai **6/7 (85,7%)**; đồng thời mini lab `d06-lab-tram-gate` có **9/16 học viên (56,2%)** bấm skip hoặc chưa hoàn thành.
3. **Ví dụ 3 (`Day07` — `d07-lab-ngan-sach-context` & `tool_definition_context_cost`):** **7/12 học viên (58,3%)** mở mini lab `d07-lab-ngan-sach-context` bấm skip (5) hoặc bỏ dở (2); đồng thời KC `tool_definition_context_cost` sai **6/10 (60,0%)**.
4. **Ví dụ 4 (`Day01` — `chatbot_is_app_around_model` & video `d01-r1-v02.txt`):** Trên 417 học viên active, **16/41 lượt (39,0%)** sai `chatbot_is_app_around_model`, **31/72 học viên (43,1%)** chưa hoàn thành/skip `d01-lab-ban-la-llm`, và riêng video `Day01/d01-r1-v02.txt` phát sinh **115 lượt** câu hỏi `video_question`.
5. **Ví dụ 5 (`Day12` — Trường hợp mẫu rất nhỏ):** Chỉ có **26 học viên active**, **0 KC có `n ≥ 5`**, mini lab chỉ có **3 người mở** — là ví dụ điển hình buộc hệ thống phải gắn cảnh báo độ tin cậy thấp thay vì kết luận cho cả lớp.

---

## 5. Giới hạn của dữ liệu

- **Chỉ ghi nhận hành vi, không có nội dung chữ chat:** Log đã được BTC ẩn danh, không lưu văn bản câu hỏi hay câu trả lời tự do của học viên (chỉ có độ dài ký tự và số lượt hỏi theo video). Do đó nguyên nhân sâu xa (không hiểu bài vs thiếu thời gian vs lỗi kỹ thuật) chỉ là giả thuyết để Giảng viên/Lab Coach kiểm chứng đầu giờ.
- **Khác biệt định nghĩa mẫu số:** Mẫu số KC tính theo lượt trả lời hợp lệ lần đầu (`video_quiz`, `pre_post_post`); mẫu số Mini Lab tính theo số học viên distinct mở từng `lab_key` (khác với tổng `active_learners` trong ngày).
- **Trạng thái nguồn bổ trợ:** Tại mốc CP3, nhóm tạm dùng Nguồn 1 (`data/preclass/`) làm nguồn bằng chứng đạt ngưỡng chính và không đưa log phỏng vấn chưa xác thực vào repo (chi tiết: `evidence/summary.md`).
