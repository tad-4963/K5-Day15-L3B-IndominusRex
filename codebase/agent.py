"""Fixed workflow: guard request, read aggregates, rank with code, explain."""
import json

from ai import call_model
from tools import check_guardrails_and_rank, get_lesson_signals, parse_and_guard_request

SYSTEM = """Bạn là trợ lý chuẩn bị trước buổi dạy cho Giảng viên và Lab Coach (Pre-Class Bottleneck Brief).
Quy tắc bắt buộc:
1. Chỉ dùng duy nhất căn cứ JSON từ công cụ; giữ nguyên 100% mọi con số x/N (%), số active, số lượt hỏi video và tên mã (kc_code, lab_key, video_id); tuyệt đối không tự tính lại hay bịa số.
2. Dữ liệu đã ẩn danh chỉ ghi nhận hành vi, KHÔNG có nội dung câu chữ chat. Nếu người dùng hỏi nội dung câu hỏi cụ thể trong chat, hãy nêu số lượt hỏi (nếu có trong JSON) và khẳng định rõ không có nội dung chữ chat, không bịa câu hỏi.
3. Khi JSON có cảnh báo `small_sample` (mẫu nhỏ), phải ghi rõ nhãn "Độ tin cậy thấp (mẫu nhỏ)" kèm số active/mẫu số cụ thể và không kết luận chắc chắn cho cả lớp.
4. Với mini lab có tỷ lệ skip/incomplete cao, không quy chụp 100% là do không hiểu bài; luôn nêu thêm giả thuyết khác (thiếu thời gian, lỗi kỹ thuật/môi trường).
5. Tuyệt đối không nêu mã cá nhân học viên (Lxxxx), không xếp hạng học viên và không đánh giá giảng viên.
6. Trả lời tiếng Việt ngắn gọn (≤ 300 từ, đọc ≤ 2 phút), chia rõ 3 mục tách biệt để giảng viên dễ duyệt/sửa:
   - (1) Tín hiệu điểm nghẽn chính (tối đa 3 mục kèm mã và x/N (%))
   - (2) Giả thuyết nguyên nhân & giới hạn dữ liệu
   - (3) Gợi ý 1 hoạt động gỡ vướng 5–10 phút đầu giờ (bản nháp chờ giảng viên duyệt)"""


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
