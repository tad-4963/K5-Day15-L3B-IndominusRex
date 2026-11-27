"""Read and rank anonymized lesson level pre-class signals."""
import json
import os
import re
import unicodedata

from tracing import tool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNALS_PATH = os.path.join(ROOT, "data", "lesson_signals_agg.json")

# The public alias is grounded in spec.md: the AI Product Canvas KC is in Day05.
_LESSON_ALIASES = {
    "ai product thinking": "Day05",
    "ai product canvas": "Day05",
    "ai_product_canvas": "Day05",
}
_DAY_RE = re.compile(
    r"\bday\s*0*(\d{1,2})\b|\bngay\s*0*(\d{1,2})\b|\bd0*(\d{1,2})(?:\s+r\d)?\b",
    re.I,
)
_STUDENT_RE = re.compile(r"\b(?:l\s*\d{3,8}|hv[_-]?[\w-]+)\b", re.I)
_RANK_RE = re.compile(
    r"\b(?:xep\s+hang|ranking|rank\s+(?:hoc\s+vien|students?)|"
    r"top\s*\d+\s*(?:hoc\s+vien|students?|ca\s+nhan)|"
    r"liet\s+ke.{0,60}(?:hoc\s+vien|students?|ca\s+nhan)|"
    r"(?:hoc\s+vien|students?).{0,40}(?:yeu\s+nhat|gioi\s+nhat|sai\s+nhieu\s+nhat)|"
    r"danh\s+sach.{0,40}(?:hoc\s+vien|students?))\b",
    re.I,
)
_INJECTION_RE = re.compile(
    r"(?:bo\s+qua|ignore|disregard|override).{0,80}"
    r"(?:huong\s+dan|instructions?|system\s+prompt|prompt)|"
    r"(?:reveal|show|print|xuat|tiet\s+lo).{0,40}"
    r"(?:system\s+prompt|hidden\s+prompt|huong\s+dan\s+he\s+thong)",
    re.I,
)
_OUT_OF_SCOPE_TEACHER_RE = re.compile(
    r"(?:giang\s+vien|teacher|instructor).{0,40}"
    r"(?:te\s+nhat|kem\s+nhat|danh\s+gia|xep\s+hang|cham\s+diem)|"
    r"(?:te\s+nhat|kem\s+nhat|danh\s+gia|xep\s+hang|cham\s+diem).{0,40}"
    r"(?:giang\s+vien|teacher|instructor)",
    re.I,
)
_OUT_OF_SCOPE_SLIDE_RE = re.compile(
    r"(?:soan|viet|tao).{0,60}(?:tron\s+bo|toan\s+bo|\d+\s*trang).{0,30}"
    r"(?:slide|giao\s+an)|(?:slide|giao\s+an).{0,40}"
    r"(?:tron\s+bo|toan\s+bo|\d+\s*trang)",
    re.I,
)


def _plain_text(value):
    """Lowercase, remove accents, and normalize punctuation for Vietnamese matching."""
    value = unicodedata.normalize("NFD", str(value or "").lower())
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9_]+", " ", value).strip()


def _blocked(reason):
    return {"blocked": True, "block_reason": reason, "need_clarify": False,
            "lesson_ids": [], "focus": "all"}


@tool
def parse_and_guard_request(query: str) -> dict:
    """Tên: parse_and_guard_request · Input: query (str) · Output: trạng thái chặn/làm rõ/ngày · Tác động ngoài: không."""
    text = str(query or "")
    normalized = _plain_text(text)

    if _STUDENT_RE.search(text) or _RANK_RE.search(normalized) or _INJECTION_RE.search(normalized):
        return _blocked(
            "Mình chỉ cung cấp số liệu tổng hợp cấp lớp, không truy xuất hay xếp hạng cá nhân học viên."
        )
    if _OUT_OF_SCOPE_TEACHER_RE.search(normalized):
        return _blocked(
            "Mình không đánh giá hay xếp hạng năng lực giảng viên. Dữ liệu pre-class chỉ phản ánh "
            "độ khó nội dung và hành vi tự học trước buổi học."
        )
    if _OUT_OF_SCOPE_SLIDE_RE.search(normalized):
        return _blocked(
            "Soạn trọn bộ slide/giáo án nằm ngoài phạm vi. Mình chỉ hỗ trợ tóm tắt Top 3 điểm nghẽn "
            "pre-class (Day01–Day13) và gợi ý 1 hoạt động gỡ vướng 5–10 phút đầu giờ."
        )

    ids = []
    for match in _DAY_RE.finditer(normalized):
        number = next((group for group in match.groups() if group), None)
        if number:
            lesson = "Day%02d" % int(number)
            if lesson not in ids:
                ids.append(lesson)

    alias_ids = [lesson for alias, lesson in _LESSON_ALIASES.items() if alias in normalized]
    # An explicit day always wins. Use the documented Day05 alias only when no day was given.
    if not ids and alias_ids:
        ids = list(dict.fromkeys(alias_ids))

    if not ids:
        return {"blocked": False, "block_reason": "", "need_clarify": True,
                "lesson_ids": [], "focus": "all"}

    lab_terms = ("mini lab", "lab", "thuc hanh", "bo qua", "skip")
    kc_terms = ("quiz", "kc", "trac nghiem", "ly thuyet", "khai niem", "sai nhieu")
    wants_lab = any(term in normalized for term in lab_terms)
    wants_kc = any(term in normalized for term in kc_terms) or bool(alias_ids)
    focus = "all" if wants_lab and wants_kc else "lab" if wants_lab else "kc" if wants_kc else "all"
    return {"blocked": False, "block_reason": "", "need_clarify": False,
            "lesson_ids": ids, "focus": focus}


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
    text = str(lesson_id or "").strip()
    alias = _plain_text(text)
    if alias in _LESSON_ALIASES:
        text = _LESSON_ALIASES[alias]
    match = re.fullmatch(r"\s*(?:day\s*|ngay\s*)?0*(\d{1,2})\s*", _plain_text(text), re.I)
    if not match:
        return None
    number = int(match.group(1))
    if not 1 <= number <= 13:
        return None
    return _load_data().get("Day%02d" % number)


def _metric(item):
    if not isinstance(item, dict):
        return None
    try:
        numerator = int(item.get("wrong", item.get("skip", item.get("incomplete", item.get("count", 0)))))
        denominator = int(item.get("total", item.get("active_learners", 0)))
    except (TypeError, ValueError):
        return None
    if numerator < 0 or denominator <= 0:
        return None
    return {"numerator": numerator, "denominator": denominator,
            "rate": round(100.0 * numerator / denominator, 1)}


@tool
def check_guardrails_and_rank(signals: dict, focus: str = "all") -> dict:
    """Tên: check_guardrails_and_rank · Input: signals và focus · Output: top điểm nghẽn, cảnh báo mẫu nhỏ · Tác động ngoài: không."""
    if not isinstance(signals, dict):
        return {"top_bottlenecks": [], "low_sample_warning": True,
                "sample_notes": ["Không có dữ liệu hợp lệ."], "data_gaps": []}

    if focus not in ("all", "kc", "lab"):
        focus = "all"
    try:
        active = max(0, int(signals.get("active_learners", signals.get("active", 0)) or 0))
    except (TypeError, ValueError):
        active = 0

    items = []
    if focus in ("all", "kc"):
        kc_stats = signals.get("kc_stats")
        if isinstance(kc_stats, dict):
            for name, values in kc_stats.items():
                metric = _metric(values)
                if metric:
                    items.append(dict(metric, category="knowledge_check", name=name,
                                      severity=metric["rate"]))
    if focus in ("all", "lab"):
        lab_stats = signals.get("lab_stats")
        if isinstance(lab_stats, dict):
            for name, values in lab_stats.items():
                if not isinstance(values, dict):
                    continue
                for kind in ("skip", "incomplete"):
                    count = values.get(kind)
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
                        items.append(dict(metric, category="mini_lab_" + kind, name=name,
                                          severity=metric["rate"]))

    items.sort(key=lambda item: (-item["severity"], item["category"], item["name"]))
    notes = []
    if active < 30:
        notes.append("Chỉ có %d người active; mẫu lớp nhỏ." % active)
    small_items = [item for item in items if item["denominator"] < 10]
    if small_items:
        names = ", ".join("%s (n=%d)" % (item["name"], item["denominator"])
                          for item in small_items[:5])
        notes.append("Có tín hiệu với mẫu số dưới 10: %s." % names)

    gaps = []
    if not signals.get("top_asked_videos"):
        gaps.append("Không có tín hiệu video được hỏi nhiều.")
    if signals.get("missing_context_count") is None:
        gaps.append("Không có số liệu missing context.")

    return {"top_bottlenecks": items[:3], "low_sample_warning": bool(notes),
            "sample_notes": notes, "data_gaps": gaps, "active_learners": active,
            "top_asked_videos": signals.get("top_asked_videos", []),
            "missing_context_count": signals.get("missing_context_count")}


# Names retained to match the CP2 architecture and existing documentation.
rank_bottlenecks = check_guardrails_and_rank
