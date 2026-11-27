# KẾ HOẠCH THỰC HIỆN CHI TIẾT — NHÓM INDOMINUSREX (L3B · TRACK A)

> **Đề tài đã chốt:** Track A (EdTech) · A1 mở rộng — **Pre-Class Bottleneck Brief: Bản đồ điểm nghẽn lớp học trước buổi dạy cho Giảng viên / Lab Coach**  
> **Repo nhóm:** https://github.com/tad-4963/K5-Day15-L3B-IndominusRex  
> **Nguyên tắc phối hợp (theo `02-guide.md`):** *Cả nhóm cùng đi qua mạch câu chuyện Pain → Impact → Giải pháp → Đánh giá → Chi phí; chia cặp trong từng chặng; trước mỗi checkpoint dành 15 phút rà chung cả nhóm để ai cũng trả lời được Q&A.*

---

## 1. Phân vai & Cấu trúc 2 cặp (4 thành viên)

| STT | Thành viên | Mã học viên | Vai trò & Cặp | Hạng mục chịu trách nhiệm chính (trùng khớp `TEAMS.md` & `reflection/`) |
|---|---|---|---|---|
| 1 | **Trần Anh Dũng** | `2A202604037` | **Đội trưởng · Cặp 1** (Kiến trúc & Model) | Điều phối tiến độ & nộp 4 checkpoint · Viết `spec.md` (§0, §3, §4, §5, §6, §9, §10) · Kết nối model thật (`codebase/ai.py`) · Cài đặt luồng chính & prompt (`codebase/agent.py`) · Quản trị an toàn / guardrails |
| 2 | **Vũ Huy Hiệu** | `2A202603979` | **Thành viên · Cặp 1** (Dữ liệu & Prototype) | Viết script tổng hợp `data/preclass/` → `data/lesson_signals_agg.json` (đã xóa toàn bộ mã `hv`) · Viết `data/DATA_CARD.md` · Viết công cụ code (`codebase/tools.py`: đọc tín hiệu, kiểm mẫu nhỏ, chặn soi cá nhân, xếp hạng điểm nghẽn) · Nâng cấp giao diện/CLI (`codebase/app.py`) · Code cải tiến Lượt 2 & quay video demo |
| 3 | **Đỗ Lý Hoàng Nam** | `2A202603777` | **Thành viên · Cặp 2** (Phỏng vấn & Eval) | Tổ chức phỏng vấn ≥3 Lab Coach / Key Coach / Giảng viên (`evidence/interviews/P1.md`–`P3.md`, `evidence/summary.md`) · Thiết kế `eval/metric_spec.yaml` & `eval/benchmark.csv` (24–28 câu) · Tổ chức chấm chéo 5 output (khớp ≥4/5) · Chấm `run-1.csv`, `run-2.csv` · Viết `eval/report.md` & `eval/README.md` |
| 4 | **Hoàng Thế Phong** | `2A202603832` | **Thành viên · Cặp 2** (Data Mining, Cost & Slide) | Hoàn thiện `evidence/data-mining.md` (script đếm chuẩn xác, x/N, %, giới hạn data) · Viết `spec.md` §1–§2 (Bảng impact ≥3 hướng có nguồn) · Xây `cost/personas.yaml`, chạy `run.py simulate` (≥50 phiên, ≥2 model), viết `cost/cost-estimate.md` & `spec.md` §8 · Tổ chức test Bonus (`validation/log.md`) · Thiết kế Slide 8 trang |

> **Quy tắc kiểm chéo bắt buộc:**
> - **Trước CP2:** Cặp 1 (Dũng, Hiệu) review `benchmark.csv` + `metric_spec.yaml` của Cặp 2 (chấm độc lập 5 output); Cặp 2 (Nam, Phong) review sơ đồ `spec.md` §4 + `DATA_CARD.md` của Cặp 1.
> - **Mỗi người phỏng vấn ≥1 người** (nếu phỏng vấn 4 Lab Coach/GV thì mỗi bạn hỏi 1 người hoặc chia cặp 1 hỏi + 1 ghi chép).
> - **Mỗi người chạy thử ít nhất 1 lần** `python run.py`, `python run.py eval`, `python run.py simulate` để hiểu luồng khi giám khảo hỏi.

---

## 2. Lộ trình chi tiết theo 5 chặng (16:30 T6 27/11 → 23:59 T7 28/11)

### CHẶNG 1 · KHỞI ĐỘNG & NỘP CP1 *(16:30 → 17:00 Thứ Sáu 27/11 — 3 điểm)*
**Mục tiêu:** Chốt CP1 sạch sẽ, đúng giờ, 0 lỗi format `TEAMS.md`.

- **Trần Anh Dũng (Cặp 1):**
  - Rà lại `TEAMS.md`, `canvas.md`, `evidence/hypothesis.md`, `README.md`.
  - Chạy `python run.py check` xác nhận `TEAMS.md` không lỗi.
  - Commit & push lên GitHub, mở link repo bằng **cửa sổ ẩn danh** kiểm tra Public.
  - Mời 3 thành viên vào GitHub Collaborators.
  - **Nộp form CP1 trước 16:55** trên https://ai20k-hackathon.pages.dev/#submit.
- **Vũ Huy Hiệu (Cặp 1):**
  - Mở đọc cấu trúc `data/preclass/` (`column_dictionary.csv`, `event_types.csv`, `answers.csv`, `events.csv`, `chat.csv`) để chuẩn bị viết script tạo `data/lesson_signals_agg.json`.
  - Chạy thử `python run.py` chế độ giả để đảm bảo môi trường Python 3.10+ chạy ổn.
- **Đỗ Lý Hoàng Nam (Cặp 2):**
  - **Đi tìm và hẹn ngay 3–4 Lab Coach / Key Coach / Giảng viên** đang có mặt tại lớp (C401, hoặc các phòng L3A) cho các buổi phỏng vấn ngắn 10 phút trong khung 17:00–18:00.
  - Chuẩn bị mẫu ghi chép `evidence/interviews/P1.md`..`P3.md` theo kịch bản Mom Test (ở Mục 3 bên dưới).
- **Hoàng Thế Phong (Cặp 2):**
  - Đọc kỹ số liệu `data/preclass/` và phác thảo bảng so sánh **4 hướng Track A** cho `spec.md` §2 (1. Bản đồ điểm nghẽn GV/LC · 2. Trợ giảng trích dẫn mốc video · 3. Bộ điều phối Bạn học AI · 4. Trợ lý gỡ kẹt Mini Lab).

---

### CHẶNG 2 · THIẾT KẾ, KHUNG PROTOTYPE & CHỐT CHUẨN "ĐẠT" → NỘP CP2 *(17:00 → 19:30 Thứ Sáu 27/11 — 4 điểm)*
> **CỰC KỲ QUAN TRỌNG:** Chuẩn "đạt" trong `spec.md` §7 **CHỐT TẠI MỐC NÀY (19:30)** và **KHÔNG ĐƯỢC SỬA** về sau!

- **17:00–17:45 (Cả nhóm thu bằng chứng đầu & tổng hợp chung):**
  - **Đỗ Lý Hoàng Nam + Hoàng Thế Phong** (cùng sự hỗ trợ của Dũng/Hiệu nếu cần): hoàn thành phỏng vấn **≥2–3 Lab Coach / Key Coach / Giảng viên** (mỗi người 10 phút), ghi nguyên văn trích dẫn vào `evidence/interviews/P1.md`..`P3.md` (ẩn danh `P1, P2, P3`, không ghi tên thật!). **Nhớ hẹn luôn 2–3 anh/chị này sáng/đầu giờ chiều mai test 5 phút cho phần Bonus +5đ!**
  - **17:45–18:00 (Cả nhóm họp 15 phút):** Tổng hợp insight từ phỏng vấn + data → chốt chính thức lát cắt, sơ đồ kiến trúc, 4 lớp chỗ khó và chuẩn "đạt".
- **18:00–19:15 (Chia 2 cặp làm song song):**
  - **Cặp 1 — Trần Anh Dũng:**
    - Viết `spec.md` §0, §3, §4 (sơ đồ Mermaid Workflow 3 bước + lý do không chọn multi-agent + bảng công cụ + mức tự động "AI gợi ý, người quyết" + 4 nguyên tắc HAX có **G10 bắt buộc**), §5 (≥6 kịch bản 4 lớp + **2 câu tấn công đòi xếp hạng/lộ mã học viên `Lxxxx`**), §6.
    - Cập nhật `canvas.md` bản CP2 (số bằng chứng đầu + 1 trích dẫn + dòng "Đã đổi gì so với CP1").
    - Lấy sẵn **API key** (OpenAI / Gemini / Anthropic / DeepSeek), tạo `.env` (không commit!) và thử nối trước khi rời lớp.
  - **Cặp 1 — Vũ Huy Hiệu:**
    - Viết script tổng hợp `scripts/build_lesson_signals.py` → sinh `data/lesson_signals_agg.json` (tổng hợp 13 ngày học Day01–Day13: `active_learners`, `kc_stats` gồm `wrong/total/rate`, `lab_stats` gồm `skip/incomplete/open`, `top_asked_videos`, `missing_context_count`; **tuyệt đối không có mã `hv`**).
    - Viết `data/DATA_CARD.md` bản đầu (nguồn `data/preclass/`, bước ẩn danh/tổng hợp, quy mô, giới hạn không có chữ chat).
    - Dựng khung `codebase/tools.py` (`get_lesson_signals`, `check_guardrails_and_rank`) và `codebase/agent.py` chạy thông hết luồng với `MODEL_PROVIDER=fake` (`python run.py` chạy ra output khung không lỗi).
  - **Cặp 2 — Đỗ Lý Hoàng Nam:**
    - Viết `eval/metric_spec.yaml` (**4 metric** rõ ràng, đo được: `number_fidelity`, `uncertainty_and_boundary`, `privacy_guardrail`, `actionable_brief`).
    - Viết `eval/benchmark.csv` **≥12 câu thử bản đầu** (đủ 6 cột, xóa 3 dòng ví dụ B01–B03; gồm câu thường từ Day01–Day08, câu khó mẫu nhỏ Day10/Day12/Day13, 2 câu `tu_choi` tấn công đòi mã `Lxxxx` / prompt injection; ≥1/3 từ `data_that` & `nguoi_dung`).
    - Cùng **Dũng** chốt **Chuẩn "đạt" bằng số** ghi vào `spec.md` §7 (ví dụ: *"Đạt khi ≥ 80% tổng số câu thử qua, VÀ điều kiện cứng: 100% câu `tu_choi`/tấn công qua (0% rò rỉ/xếp hạng cá nhân), 100% con số x/N khớp tool"*).
  - **Cặp 2 — Hoàng Thế Phong:**
    - Viết `evidence/data-mining.md` kèm script đếm tái lập được (`scripts/mine_evidence.py`), ghi rõ mẫu số (436 active / 721 tổng), `x/N (%)`, ≥5 ví dụ cụ thể từng bài và giới hạn dữ liệu.
    - Viết nháp bảng Impact ở `spec.md` §1–§2 (≥3 hướng, giữ hướng bị loại có lý do, công thức Impact/tháng có nguồn).
- **19:15–19:30 (Tự soát & Nộp CP2):**
  - Chạy `python run.py check` + `python run.py`.
  - **Trần Anh Dũng** rà đủ 5 mục tự soát CP2, nhóm thống nhất commit/push và **nộp form CP2 trước 19:30**.

---

### CHẶNG 3 · BUILD AI THẬT, MỞ RỘNG BENCHMARK & CHẠY LƯỢT 1 → NỘP CP3 *(Tối T6 27/11 → 10:00 T7 28/11 — 4 điểm)*
> **Lưu ý:** Sáng Thứ Bảy không có lớp. **Phải nối xong model thật & chạy `eval --try` ngay tối Thứ Sáu trước khi ngủ!**

- **Tối T6 (20:30–23:30):**
  - **Cặp 1 — Trần Anh Dũng:**
    - Nối model thật trong `codebase/ai.py` theo `docs/connect-model.md`, chạy `python run.py eval --try` kiểm tra `tokens_in > 0`, `tokens_out > 0`.
    - Viết `SYSTEM` prompt bản V1 trong `codebase/agent.py`: ép trích đúng `x/N (%)` từ JSON tool, bắt buộc cảnh báo mẫu nhỏ (`n < 10`), nêu rõ giới hạn không có nội dung chữ chat, chặn soi cá nhân, giữ độ dài đọc trong ≤2 phút.
  - **Cặp 1 — Vũ Huy Hiệu:**
    - Hoàn thiện `codebase/tools.py`: xử lý truy vấn linh hoạt (nhận diện `"Day 5"`, `"ngày 5"`, `"day05"`, `"ai-product-thinking"`, so sánh 2 ngày, lọc riêng mini lab vs lý thuyết, trả lỗi rõ khi ngày không tồn tại như `Day14`, chặn cứng regex/từ khóa truy vấn mã `L\d{4}` hoặc xếp hạng học viên).
    - Chạy thử `python run.py simulate --try` (10 phiên) để kiểm tra khung mô phỏng chi phí không bị lỗi trước CP3.
  - **Cặp 2 — Đỗ Lý Hoàng Nam:**
    - Mở rộng `eval/benchmark.csv` lên **24–28 câu thử** (phủ lưới input: ≥6 `kho` gồm Day10/Day12/Day13 mẫu nhỏ, so sánh 2 ngày, hỏi chữ chat không có trong log, câu mơ hồ không nói ngày; ≥4 `tu_choi` gồm 2 câu tấn công + Day14 không có data + yêu cầu ngoài phạm vi; ≥50% câu có `source` là `data_that:` hoặc `nguoi_dung:`).
    - Chạy `python run.py check` đảm bảo **0 cảnh báo**!
    - Chấm chéo độc lập **5 output mẫu** giữa **Nam** và **Phong** (đạt khớp ≥4/5, nếu lệch ≥2/5 sửa định nghĩa trong `metric_spec.yaml`), ghi kết quả vào `eval/README.md`.
  - **Cặp 2 — Hoàng Thế Phong:**
    - Hoàn thiện `evidence/summary.md` (tổng hợp đối chiếu Nguồn 1 đào data + Nguồn 2 phỏng vấn ≥3 Lab Coach/GV + ≥5 trích dẫn nguyên văn bỏ tên + kết luận giả thuyết).
    - Hoàn thiện `spec.md` §1–§2 (công thức impact/tháng hoàn chỉnh có nguồn từng thừa số).
    - Viết nháp `cost/personas.yaml` (3 persona thật: GV giảng chính 4 lần/tháng, Lab Coach trực lab 8 lần/tháng, Key Coach / Ban đào tạo rà tổng hợp 15 lần/tháng; điền bảng giá chuẩn từ `further-reading/model-prices.md` ngày 25/11/2026 cho ≥2 tầng model).
- **Sáng T7 (08:30–10:00 — Cả nhóm họp online chạy Lượt 1 & Nộp CP3):**
  - **Cả nhóm (08:30–09:15):** Chạy `python run.py eval` → ra `eval/run-1.csv` + `traces/run-1.jsonl` (nếu gói miễn phí dính 429 thì thêm `--wait 4`). **Nam** chủ trì chấm cột `pass` (1/0) theo đúng `metric_spec.yaml` → chạy `python run.py score eval/run-1.csv`.
  - **Vũ Huy Hiệu (09:15–09:35):** Quay **video 30 giây** chạy thật gọi AI thật (1 case Day05 + 1 case tấn công/Day12), đăng YouTube Unlisted hoặc Google Drive công khai (kiểm mở bằng cửa sổ ẩn danh).
  - **Trần Anh Dũng (09:35–09:55):** Rà `spec.md` đủ §0–§7, rà 5 mục CP3, commit/push (sau khi nhóm chốt) và **nộp form CP3 trước 10:00**.

---

### CHẶNG 4 · PHÂN TÍCH LỖI, CẢI TIẾN LƯỢT 2, CHI PHÍ & BONUS → NỘP CP4 *(10:00 → 14:30 Thứ Bảy 28/11 — 4 điểm)*

- **10:00–10:45 (Cả nhóm đọc toàn bộ câu trượt của Lượt 1):**
  - Cả 4 bạn mở `eval/run-1.csv` và `traces/run-1.jsonl`, liệt kê mọi câu trượt (`pass = 0`), gom thành các nhóm lỗi có tên (vd: *bịa/lệch số so với tool*, *quên cảnh báo mẫu nhỏ G10*, *suy diễn nguyên nhân quá chắc dù không có chữ chat*, *báo cáo quá dài*).
  - Chọn **1 nhóm lỗi đau nhất với giảng viên/lab coach** để thiết kế **1 lần cải tiến tập trung** (ghi rõ vào `spec.md` §10 changelog).
- **10:45–12:30 (Chia 2 cặp chạy nước rút):**
  - **Cặp 1 — Trần Anh Dũng & Vũ Huy Hiệu:**
    - Thực hiện cải tiến đã chốt (siết prompt + bổ sung bước hậu kiểm số bằng code trong `agent.py`/`tools.py`, không sửa `benchmark.csv` hay chuẩn "đạt"!).
    - Chạy lại trọn bộ: `python run.py eval` → `eval/run-2.csv` → **Nam** chấm lại `pass` → `python run.py score eval/run-2.csv`.
    - Hoàn thiện `README.md` (bảng Phần nào thật/giả, lệnh chạy, mục Dùng AI vào việc gì) và `docs/ai-usage.md`.
  - **Cặp 2 — Đỗ Lý Hoàng Nam:**
    - Viết `eval/report.md` (% Lượt 1 → Lượt 2 vs chuẩn "đạt", phân tích chi tiết ≥3 lỗi có input/output/nguyên nhân, mô tả cải tiến & lỗi còn lại).
    - Hoàn thiện `eval/README.md` (Hồ sơ đánh giá 1 trang: dataset → benchmark → metric + kết quả chấm chéo ≥4/5 → bảng các lượt chạy kèm run ID & model → lỗi chính).
  - **Cặp 2 — Hoàng Thế Phong:**
    - Chạy mô phỏng chi phí thật: `python run.py simulate --rate-from eval/run-2.csv` (**≥50 phiên**, seed cố định) → `cost/simulate-1.csv` + summary.
    - Viết `cost/cost-estimate.md` & `spec.md` §8: chi phí / task thành công (dùng % đạt thật của Lượt 2!), 3 kịch bản (thấp / cơ sở / cao) ở quy mô thật (~84 GV + Lab Coach khóa AI20K), **≥2 tầng model** (vd `gpt-5-nano` / `gemini-3.1-flash-lite` vs `gpt-6.2-sol` / `gemini-4-hydrogen`, ghi rõ giá + link + ngày xem 25/11/2026), và **1 dòng so sánh chi phí/người/tháng vs impact/người/tháng**.
  - **Bonus (+5 điểm) — Đỗ Lý Hoàng Nam & Hoàng Thế Phong (11:30–13:30):**
    - Mời **2–3 Lab Coach / Key Coach** (đã hẹn từ chiều T6) dùng thử trực tiếp bản chạy thử theo **kịch bản 5 nhịp** (để người thử tự gõ, quan sát im lặng, hỏi 4 câu cuối) → ghi đủ cột vào `validation/log.md` + rút ra ≥1 thay đổi (ghi vào `spec.md` §10).
- **13:00–14:20 (Chuẩn bị Slide, Video dự phòng & Tập Demo):**
  - **Hoàng Thế Phong + Đỗ Lý Hoàng Nam:** Hoàn thiện **Slide 8 trang** theo đúng khung `02-guide.md` 5.1 (xuất `demo-slides.pdf`, mỗi trang có ≥1 con số / trích dẫn có nguồn / kết quả đo).
  - **Vũ Huy Hiệu:** Quay **video demo dự phòng** (2 phút: 1 case thường `Day05` + 1 case khó `Day12` mẫu nhỏ + 1 case tấn công `Lxxxx`) mở được ẩn danh.
  - **Cả nhóm (13:50–14:15):** Chạy tập demo 1 lượt, phân phần nói cho cả 4 bạn, kiểm tra cả 4 người trả lời trôi chảy 4 câu hỏi tủ của giám khảo:
    1. *Vì sao chọn Workflow cố định mà không chọn Multi-agent?*
    2. *Lỗi nguy hiểm nhất là gì và nhóm chặn ở đâu?*
    3. *Chi phí / task thành công tính thế nào?*
    4. *Phần việc cụ thể của bạn là gì?*
  - **Trần Anh Dũng (trước 14:25):** Kiểm tra không có `.env` / API key / file CSV gốc `data/preclass/` trong repo → **Nộp form CP4 trước 14:30**!

---

### CHẶNG 5 · DEMO & HOÀN THIỆN HẠN CHÓT *(14:30 → 23:59 Thứ Bảy 28/11)*
- **14:30–16:00:** Demo Zone (mọi người đều nói ≥1 phần; sẵn sàng chạy 1 câu thử lạ giám khảo đưa tại chỗ).
- **16:00–18:00:** Demo Phòng (nếu lọt top zone).
- **18:00–23:30 (Sau Demo → Hạn chót 23:59):**
  - Ghi mọi chỉnh sửa sau góp ý của giám khảo vào `spec.md` §10 (tuyệt đối **không sửa** chuẩn "đạt", câu thử trong `benchmark.csv`, số liệu bằng chứng hay kết quả `run-1.csv`/`run-2.csv`; nếu chạy thêm thì lưu thành `run-3.csv`).
  - **Cả 4 thành viên** tự viết file reflection cá nhân trong `reflection/` (bắt buộc để ghép điểm lab!):
    - `reflection/tran-anh-dung.md`
    - `reflection/vu-huy-hieu.md`
    - `reflection/do-ly-hoang-nam.md`
    - `reflection/hoang-the-phong.md`
    *(Mỗi file gồm: vai trò & phần mình làm · AI hỗ trợ thế nào · 1 bài học rút ra từ 1 câu thử trượt của chính nhóm.)*

---

## 3. Kịch bản phỏng vấn 10 phút cho Lab Coach / Giảng viên *(dùng ngay 17:00 chiều nay)*

> **Luật Mom Test:** KHÔNG giới thiệu ý tưởng app AI trước; chỉ hỏi chuyện **đã xảy ra trong 1 tháng qua**; ghi `P1, P2, P3` + vai trò, **tuyệt đối không ghi tên thật**.

1. *"Trước buổi dạy / buổi lab gần nhất anh/chị phụ trách (ví dụ tuần này), anh/chị chuẩn bị nội dung dẫn nhập đầu giờ như thế nào và mất khoảng bao lâu?"*
2. *"Trước khi vào lớp, anh/chị có cách nào xem học viên đã làm bài pre-class ra sao, sai câu nào hay bỏ qua mini lab nào nhiều không?"*
3. *"Trong 1 tháng qua, có lần nào vào buổi học/buổi lab rồi anh/chị mới phát hiện đa số học viên đang vướng nặng cùng một khái niệm pre-class nên phải dừng lại giảng lại từ đầu không? Lần đó mất bao lâu và ảnh hưởng gì tới tiến độ buổi học?"*
4. *"Nếu trước buổi học 1 tiếng anh/chị có 1 trang tóm tắt điểm nghẽn của lớp, 3 thông tin nào anh/chị muốn thấy nhất — và điều gì sẽ khiến anh/chị **không tin** hoặc **không dùng** bảng tóm tắt đó?"*
5. **Chốt hẹn Bonus:** *"Tối nay tụi em build bản chạy thử từ log ẩn danh của khoá, sáng/trưa mai em nhờ anh/chị dùng thử 5 phút góp ý giúp tụi em được không ạ?"*

---

## 4. Checklist "Cấm tuyệt đối" để không bị 0 điểm / trừ điểm
- [ ] **Không commit `.env` hay API key** (lộ = trừ 10 điểm).
- [ ] **Không commit nguyên file `data/preclass/*.csv`** vào repo Public — chỉ commit file tổng hợp `data/lesson_signals_agg.json` (đã xóa hết mã `hv`).
- [ ] **Không sửa chuẩn "đạt" ở `spec.md` §7 sau CP2 (19:30 T6)**.
- [ ] **Không xóa câu thử bị trượt, không sửa `expected` cho khớp output, không sửa tay `run-N.csv`**.
- [ ] **Mọi con số trên Slide phải truy ngược được về file trong repo** (`evidence/`, `eval/`, `cost/`).
- [ ] **Đủ 4 file `reflection/<ten-khong-dau>.md`** trước 23:59 Thứ Bảy 28/11.
