"""Fixed workflow: guard request, read aggregates, rank with code, explain."""
import json

from ai import call_model
from tools import check_guardrails_and_rank, get_lesson_signals, parse_and_guard_request

SYSTEM = """Bạn là trợ lý giảng dạy đồng hành cùng Giảng viên và Lab Coach trước giờ lên lớp (Pre-Class Bottleneck Brief).
Giọng văn: tự nhiên, ngắn gọn, tinh tế, nói chuyện trực tiếp với giảng viên/coach (xưng "mình", gọi "thầy/cô"), tránh văn phong máy móc hay lặp từ.

Quy tắc bắt buộc về độ chính xác và an toàn:
1. Chỉ dùng duy nhất số liệu trong JSON từ công cụ; giữ nguyên 100% mọi con số x/N (%), số học viên active, số lượt hỏi video và tên mã gốc (`kc_code`, `lab_key`, `video_id`). Khi nhắc tên mã, hãy diễn đạt tự nhiên bằng tiếng Việt kèm mã gốc trong ngoặc (vd: "phần Khung sản phẩm AI (`ai_product_canvas`): 12/15 lượt sai — 80.0%").
2. Mọi chỉ số `KC sai lần đầu` là TỶ LỆ TRẢ LỜI SAI (tuyệt đối không viết nhầm thành tỷ lệ đúng hay thành công).
3. Dữ liệu đã ẩn danh chỉ ghi nhận hành vi, KHÔNG có nội dung câu chữ chat. Nếu thầy/cô hỏi học viên nhắn gì hoặc video nào bị hỏi nhiều nhất, hãy nêu rõ tên video & số lượt hỏi từ `top_asked_videos` và nói nhẹ nhàng rằng hệ thống không lưu nội dung chữ chat.
4. Khi JSON có cảnh báo `small_sample` (mẫu nhỏ `n < 10` hoặc `active < 30`), nhắc rõ "độ tin cậy thấp do mẫu nhỏ" kèm số `n` cụ thể để thầy/cô cân nhắc, không kết luận thay cho cả lớp (không gọi mẫu >= 10 như n=21 là mẫu nhỏ). Nếu thầy/cô hỏi có nên dành 30 phút giảng lại khi mẫu quá nhỏ (n=1–2), khuyên thẳng là chưa nên, chỉ cần kiểm tra nhanh 5 phút đầu giờ.
5. Với bài thực hành (mini lab) bị bỏ qua/chưa hoàn thành cao, nêu đủ cả hai số skip và incomplete nếu có trong JSON; nhắc rằng nguyên nhân có thể do thiếu thời gian hoặc vướng môi trường kỹ thuật chứ chưa chắc do không hiểu bài.
6. Tuyệt đối không nêu mã cá nhân học viên (`Lxxxx`), không xếp hạng học viên và không đánh giá giảng viên.
7. Độ dài gọn (≤ 280 từ, đọc trong ≤ 2 phút), chia rõ đúng 3 mục để thầy/cô dễ lướt và duyệt:
   - (1) Điểm lớp đang vướng nhất (tối đa 3 điểm kèm mã gốc & số x/N (%))
   - (2) Lưu ý khi đọc số liệu (giả thuyết ngắn gọn + nhắc rõ chỉ có dữ liệu hành vi, không có chữ chat; kèm cảnh báo mẫu nhỏ nếu có)
   - (3) Gợi ý 5–10 phút mở đầu buổi học (đưa 1 câu hỏi cụ thể hoặc 1 ví dụ thực tế dùng được ngay — bản nháp để thầy/cô duyệt)"""


def _percent(item):
    return "%d/%d (%.1f%%)" % (item["numerator"], item["denominator"], item["rate"])


def _format_item(item):
    cat = item["category"]
    if cat == "knowledge_check":
        return "KC sai lần đầu — %s: %s lượt SAI" % (item["name"], _percent(item))
    if cat == "mini_lab_skip":
        return "Mini lab bị bỏ qua (skip) — %s: %s học viên SKIP" % (item["name"], _percent(item))
    if cat == "mini_lab_incomplete":
        return "Mini lab chưa hoàn thành (incomplete) — %s: %s học viên INCOMPLETE" % (item["name"], _percent(item))
    return "%s — %s: %s" % (cat, item["name"], _percent(item))


def _mentioned_lab_details(text, signals):
    lower = text.lower()
    details = {}
    for lab_key, stats in (signals.get("lab_stats") or {}).items():
        if lab_key.lower() in lower and isinstance(stats, dict):
            row = {}
            for kind in ("skip", "incomplete"):
                info = stats.get(kind)
                if isinstance(info, dict) and info.get("total"):
                    rate = round(100.0 * info["count"] / info["total"], 1)
                    row[kind] = "%d/%d (%.1f%%)" % (info["count"], info["total"], rate)
            if row:
                details[lab_key] = row
    return details


def answer(text: str) -> dict:
    request = parse_and_guard_request(text)
    if request["blocked"]:
        return {"output": request["block_reason"]}
    if request["need_clarify"]:
        return {"output": "Bạn muốn xem ngày nào (Day01–Day13)? Nếu muốn xem tổng quan, hãy nói rõ phạm vi ngày."}
    ids = request["lesson_ids"]
    if len(ids) > 2:
        return {"output": "Mỗi lần mình so sánh tối đa hai ngày. Bạn muốn chọn hai ngày nào?"}
    reports = []
    for lesson_id in ids:
        signals = get_lesson_signals(lesson_id)
        if signals is None:
            reports.append({"lesson_id": lesson_id, "missing": True})
            continue
        ranked = check_guardrails_and_rank(signals, request["focus"])
        reports.append({"lesson_id": lesson_id, "signals": signals, "ranked": ranked})
    if all(r.get("missing") for r in reports):
        return {"output": "Không có dữ liệu cho %s. Dữ liệu hiện được thiết kế cho Day01–Day13; hãy kiểm tra ngày cần xem." % ", ".join(ids)}
    context = []
    for report in reports:
        if report.get("missing"):
            context.append("%s: không có dữ liệu." % report["lesson_id"])
            continue
        ranked = report["ranked"]
        items = [_format_item(x) for x in ranked["top_bottlenecks"]]
        videos = report["signals"].get("top_asked_videos") or []
        payload = {
            "lesson": report["lesson_id"],
            "active_learners": ranked["active_learners"],
            "top_bottlenecks": items,
            "small_sample": ranked["sample_notes"],
            "data_gaps": ranked["data_gaps"],
            "top_asked_videos": videos[:3],
            "missing_context_count": ranked["missing_context_count"],
        }
        mentioned = _mentioned_lab_details(text, report["signals"])
        if mentioned:
            payload["mentioned_lab_detail"] = mentioned
        context.append(json.dumps(payload, ensure_ascii=False))
    user = "Căn cứ từ công cụ (giữ nguyên mọi số liệu):\n%s\n\nYêu cầu: %s" % ("\n".join(context), text)
    reply = call_model(SYSTEM, user)
    return {"output": reply["text"]}
