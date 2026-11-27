"""Read and rank anonymized lesson level pre-class signals."""
import json
import os
import re

from tracing import tool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNALS_PATH = os.path.join(ROOT, "data", "lesson_signals_agg.json")
_DAY_RE = re.compile(r"\bday\s*0*(\d{1,2})\b|\bngày\s*0*(\d{1,2})\b|\bd0*(\d{1,2})-r\d", re.I)
_STUDENT_RE = re.compile(r"\b(?:L\d{4}|hv\w*)\b", re.I)
_RANK_RE = re.compile(r"\b(xếp hạng|xep hang|top\s*\d+\s*(?:học viên|hoc vien)|yếu nhất|yeu nhat|giỏi nhất|gioi nhat|liệt kê.*học viên|liet ke.*hoc vien)\b", re.I)
_INJECTION_RE = re.compile(r"(bỏ qua|bo qua).{0,40}(hướng dẫn|huong dan|instruction)|reveal.{0,20}(prompt|system)|ignore.{0,30}instruction", re.I)
_OUT_OF_SCOPE_TEACHER_RE = re.compile(r"(giảng viên|giang vien).{0,30}(tệ nhất|te nhat|kém nhất|kem nhat|đánh giá|danh gia|xếp hạng|xep hang)", re.I)
_OUT_OF_SCOPE_SLIDE_RE = re.compile(r"(soạn|soan|viết|viet).{0,30}(trọn bộ|tron bo|toàn bộ|toan bo|\d+\s*trang).{0,20}(slide|giáo án|giao an)", re.I)


@tool
def parse_and_guard_request(query: str) -> dict:
    """Tên: parse_and_guard_request · Input: query (str) · Output: trạng thái chặn/làm rõ/ngày · Tác động ngoài: không."""
    text = str(query or "")
    if _STUDENT_RE.search(text) or _RANK_RE.search(text) or _INJECTION_RE.search(text):
        return {"blocked": True, "block_reason": "Mình chỉ cung cấp số liệu tổng hợp cấp lớp, không truy xuất hay xếp hạng cá nhân học viên.", "need_clarify": False, "lesson_ids": [], "focus": "all"}
    if _OUT_OF_SCOPE_TEACHER_RE.search(text):
        return {"blocked": True, "block_reason": "Mình không đánh giá hay xếp hạng năng lực giảng viên. Dữ liệu pre-class chỉ phản ánh độ khó nội dung và hành vi tự học trước buổi học.", "need_clarify": False, "lesson_ids": [], "focus": "all"}
    if _OUT_OF_SCOPE_SLIDE_RE.search(text):
        return {"blocked": True, "block_reason": "Soạn trọn bộ slide/giáo án nằm ngoài phạm vi. Mình chỉ hỗ trợ tóm tắt Top 3 điểm nghẽn pre-class (Day01–Day13) và gợi ý 1 hoạt động gỡ vướng 5–10 phút đầu giờ.", "need_clarify": False, "lesson_ids": [], "focus": "all"}
    ids = []
    for match in _DAY_RE.finditer(text):
        number = next((g for g in match.groups() if g), None)
        if number:
            lesson = "Day%02d" % int(number)
            if lesson not in ids:
                ids.append(lesson)
    if not ids:
        return {"blocked": False, "block_reason": "", "need_clarify": True, "lesson_ids": [], "focus": "all"}
    lower = text.lower()
    focus = "lab" if any(k in lower for k in ("mini lab", "lab", "thực hành", "thuc hanh")) else "kc" if any(k in lower for k in ("quiz", "kc", "trắc nghiệm", "trac nghiem", "lý thuyết", "ly thuyet")) else "all"
    return {"blocked": False, "block_reason": "", "need_clarify": False, "lesson_ids": ids, "focus": focus}


def _load_data():
    if not os.path.isfile(SIGNALS_PATH):
        return {}
    with open(SIGNALS_PATH, encoding="utf-8") as f:
        value = json.load(f)
    if isinstance(value, dict) and isinstance(value.get("days"), dict):
        return value["days"]
    if isinstance(value, dict):
        return value
    return {}


@tool
def get_lesson_signals(lesson_id: str) -> dict:
    """Tên: get_lesson_signals · Input: lesson_id (str) · Output: tín hiệu tổng hợp hoặc None · Tác động ngoài: không."""
    match = re.fullmatch(r"\s*(?:day\s*|ngày\s*)?0*(\d{1,2})\s*", str(lesson_id), re.I)
    if not match:
        return None
    key = "Day%02d" % int(match.group(1))
    return _load_data().get(key)


def _metric(item):
    if not isinstance(item, dict):
        return None
    try:
        numerator = int(item.get("wrong", item.get("skip", item.get("incomplete", item.get("count", 0)))))
        denominator = int(item.get("total", item.get("active_learners", 0)))
    except (TypeError, ValueError):
        return None
    if denominator <= 0:
        return None
    rate = 100.0 * numerator / denominator
    return {"numerator": numerator, "denominator": denominator, "rate": round(rate, 1)}


@tool
def check_guardrails_and_rank(signals: dict, focus: str = "all") -> dict:
    """Tên: check_guardrails_and_rank · Input: signals và focus · Output: top điểm nghẽn, cảnh báo mẫu nhỏ · Tác động ngoài: không."""
    if not isinstance(signals, dict):
        return {"top_bottlenecks": [], "low_sample_warning": True, "sample_notes": ["Không có dữ liệu hợp lệ."], "data_gaps": []}
    active = int(signals.get("active_learners", signals.get("active", 0)) or 0)
    items = []
    if focus in ("all", "kc"):
        for name, values in (signals.get("kc_stats") or {}).items():
            metric = _metric(values)
            if metric:
                items.append(dict(metric, category="knowledge_check", name=name, severity=metric["rate"]))
    if focus in ("all", "lab"):
        for name, values in (signals.get("lab_stats") or {}).items():
            for kind in ("skip", "incomplete"):
                count = values.get(kind) if isinstance(values, dict) else None
                if isinstance(count, dict):
                    metric = _metric(count)
                elif count is not None:
                    try:
                        total = int(values.get("total", active))
                        metric = _metric({"count": count, "total": total})
                    except (TypeError, ValueError):
                        metric = None
                else:
                    metric = None
                if metric:
                    items.append(dict(metric, category="mini_lab_" + kind, name=name, severity=metric["rate"]))
    items.sort(key=lambda x: (-x["severity"], x["category"], x["name"]))
    notes = []
    if active < 30:
        notes.append("Chỉ có %d người active; mẫu lớp nhỏ." % active)
    elif any(x["denominator"] < 10 for x in items):
        notes.append("Có tín hiệu với mẫu số dưới 10.")
    gaps = []
    if not signals.get("top_asked_videos"):
        gaps.append("Không có tín hiệu video được hỏi nhiều.")
    if signals.get("missing_context_count") is None:
        gaps.append("Không có số liệu missing context.")
    return {"top_bottlenecks": items[:3], "low_sample_warning": bool(notes), "sample_notes": notes, "data_gaps": gaps,
            "active_learners": active, "top_asked_videos": signals.get("top_asked_videos", []),
            "missing_context_count": signals.get("missing_context_count")}


# Names retained to match the CP2 architecture and existing documentation.
rank_bottlenecks = check_guardrails_and_rank
