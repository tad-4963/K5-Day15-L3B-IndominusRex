"""Fixed workflow: guard request, read aggregates, rank with code, explain."""
import json

from ai import call_model
from tools import check_guardrails_and_rank, get_lesson_signals, parse_and_guard_request

SYSTEM = """Bạn là trợ lý chuẩn bị trước lớp cho giảng viên/lab coach. Chỉ dùng căn cứ JSON được cung cấp; không tự tính hoặc thay đổi số x/N (%). Nêu tối đa 3 tín hiệu, tách rõ số liệu với giả thuyết, gợi ý một hoạt động 5–10 phút. Nêu rõ dữ liệu chỉ là hành vi ẩn danh, không có nội dung chữ chat nên không thể biết nguyên nhân chắc chắn. Nếu cảnh báo mẫu nhỏ xuất hiện, phải nêu rõ và tránh kết luận cho cả lớp. Không suy luận về cá nhân. Trả lời tiếng Việt gọn, có thể đọc trong 2 phút."""


def _percent(item):
    return "%d/%d (%.1f%%)" % (item["numerator"], item["denominator"], item["rate"])


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
        items = ["%s — %s: %s" % (x["category"], x["name"], _percent(x)) for x in ranked["top_bottlenecks"]]
        videos = report["signals"].get("top_asked_videos") or []
        context.append(json.dumps({"lesson": report["lesson_id"], "active_learners": ranked["active_learners"],
                                   "top_bottlenecks": items, "small_sample": ranked["sample_notes"],
                                   "data_gaps": ranked["data_gaps"], "top_asked_videos": videos,
                                   "missing_context_count": ranked["missing_context_count"]}, ensure_ascii=False))
    user = "Căn cứ từ công cụ (giữ nguyên mọi số liệu):\n%s\n\nYêu cầu: %s" % ("\n".join(context), text)
    reply = call_model(SYSTEM, user)
    return {"output": reply["text"]}
