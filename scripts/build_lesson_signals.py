"""Build anonymous lesson aggregates from the BTC CSVs in data/preclass/.

The source schemas vary by cohort export. Column names are matched using common
aliases; if required fields cannot be found, the script stops instead of making
up counts. Raw identifiers are used only in memory to count distinct learners
and are never written to the aggregate.
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SOURCE = os.path.join(ROOT, "data", "preclass")
DEFAULT_OUTPUT = os.path.join(ROOT, "data", "lesson_signals_agg.json")

ALIASES = {
    "day": ("day", "day_id", "lesson", "lesson_id", "day_code", "transcript"),
    "learner": ("hv", "learner_id", "student_id", "user_id", "participant_id"),
    "kc": ("kc", "kc_id", "kc_code", "question_id", "item_id"),
    "correct": ("was_correct", "is_correct", "correct", "result", "score"),
    "lab": ("lab", "lab_id", "lab_key", "activity_id", "mini_lab_id"),
    "event": ("event_type", "event", "action", "status", "type"),
    "video": ("video_id", "video", "video_key", "content_id"),
    "context": ("missing_context", "context_missing", "has_context", "context_status"),
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def column(rows, role, required=False):
    if not rows:
        return None
    lookup = {norm(k): k for k in rows[0]}
    for candidate in ALIASES[role]:
        if norm(candidate) in lookup:
            return lookup[norm(candidate)]
    if required:
        raise ValueError("Không tìm thấy cột %s (thử một trong: %s)" % (role, ", ".join(ALIASES[role])))
    return None


def day_key(value):
    m = re.search(r"(?:day|ngày)[^0-9]*0*(\d{1,2})", str(value or ""), re.I)
    if not m:
        return None
    n = int(m.group(1))
    return "Day%02d" % n if 1 <= n <= 13 else None


def truth(value):
    return str(value or "").strip().lower() in ("1", "true", "yes", "y", "correct", "đúng", "dung", "success")


def build(source):
    paths = {name: os.path.join(source, name + ".csv") for name in ("answers", "events", "chat")}
    absent = [p for p in paths.values() if not os.path.isfile(p)]
    if absent:
        raise FileNotFoundError("Thiếu file nguồn: " + ", ".join(os.path.relpath(p, ROOT) for p in absent))
    tables = {name: read_csv(path) for name, path in paths.items()}
    chat_day_by_id = {}
    chat_learner_by_id = {}
    for row in tables["chat"]:
        chat_day = day_key(row.get("transcript")) or day_key(row.get("lesson_id"))
        if chat_day:
            chat_day_by_id[row.get("id")] = chat_day
            chat_learner_by_id[row.get("id")] = row.get("hv")
    days = {"Day%02d" % i: {"active_learners": 0, "kc_stats": {}, "lab_stats": {},
                             "top_asked_videos": [], "missing_context_count": 0} for i in range(1, 14)}
    active = defaultdict(set)
    kc_counts = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    lab_counts = defaultdict(lambda: defaultdict(Counter))
    lab_participants = defaultdict(set)
    video_counts = defaultdict(Counter)
    missing = Counter()

    ans = tables["answers"]
    if ans:
        dc, uc = column(ans, "day", True), column(ans, "learner", True)
        kc, cc = column(ans, "kc", True), column(ans, "correct", True)
        attempt_col = "lan_thu" if "lan_thu" in ans[0] else None
        source_col = "nguon" if "nguon" in ans[0] else None
        for row in ans:
            d = day_key(row.get(dc)); learner = row.get(uc)
            if not (d and learner):
                continue
            active[d].add(learner)
            # Include scored quiz/pre-post answers only; exclude unscored practice/chat.
            if (attempt_col and str(row.get(attempt_col)).strip() != "1") or (source_col and row.get(source_col) not in ("video_quiz", "pre_post_post")):
                continue
            correct = str(row.get(cc) or "").strip().lower()
            if correct not in ("true", "false"):
                continue
            key = (d, str(row.get(kc) or "knowledge_check"))
            kc_counts[key]["total"][0] += 1
            if correct == "false":
                kc_counts[key]["wrong"][0] += 1

    ev = tables["events"]
    if ev:
        dc, uc = column(ev, "day", True), column(ev, "learner", True)
        lc, ec = column(ev, "lab"), column(ev, "event", True)
        for row in ev:
            d = day_key(row.get(dc)); learner = row.get(uc)
            if not d and row.get("type") in ("chat_sent", "agent_replied"):
                d = chat_day_by_id.get(row.get("ref_id"))
            if d and learner:
                active[d].add(learner)
                event = str(row.get(ec) or "")
                try:
                    payload = json.loads(row.get("data") or "{}")
                except (TypeError, json.JSONDecodeError):
                    payload = {}
                if event in ("lab_opened", "lab_completed"):
                    lab_name = str(payload.get("lab_key") or row.get(lc) or "mini_lab")
                    lab_participants[(d, lab_name)].add(learner)
                    if event == "lab_opened":
                        lab_counts[(d, lab_name)]["open"][learner] = 1
                    elif truth(payload.get("skipped")):
                        lab_counts[(d, lab_name)]["skip"][learner] = 1
                    else:
                        lab_counts[(d, lab_name)]["completed"][learner] = 1
                if event == "agent_replied" and truth(payload.get("missing_context")):
                    missing[d] += 1

    chat = tables["chat"]
    if chat:
        for row in chat:
            d = day_key(row.get("transcript")) or day_key(row.get("lesson_id"))
            if d and row.get("hv"):
                active[d].add(row["hv"])
            if d and row.get("channel") == "video_question" and row.get("transcript"):
                video_counts[d][str(row["transcript"])] += 1

    for d, data in days.items():
        data["active_learners"] = len(active[d])
    for (d, name), counts in kc_counts.items():
        wrong, total = counts["wrong"][0], counts["total"][0]
        days[d]["kc_stats"][name] = {"wrong": wrong, "total": total, "rate": round(wrong / total, 4) if total else 0}
    for (d, name), kinds in lab_counts.items():
        total = len(lab_participants[(d, name)])
        completed = len(kinds.get("completed", {}))
        # Incomplete means a learner opened a lab but did not complete it.
        incomplete = max(0, total - completed - len(kinds.get("skip", {})))
        days[d]["lab_stats"][name] = {
            "open": {"count": total, "total": total, "rate": 1.0 if total else 0},
            "skip": {"count": len(kinds.get("skip", {})), "total": total, "rate": round(len(kinds.get("skip", {})) / total, 4) if total else 0},
            "incomplete": {"count": incomplete, "total": total, "rate": round(incomplete / total, 4) if total else 0},
        }
    for d, counts in video_counts.items():
        days[d]["top_asked_videos"] = [{"video_id": k, "count": v} for k, v in counts.most_common(5)]
    for d in days:
        days[d]["missing_context_count"] = missing[d]
    return {"schema_version": 1, "source": "data/preclass/*.csv", "days": days}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Thư mục CSV đầu vào (mặc định data/preclass)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Đường dẫn JSON tổng hợp")
    args = parser.parse_args()
    try:
        result = build(args.source)
    except (OSError, ValueError, csv.Error) as exc:
        print("Không tạo được aggregate: %s" % exc, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Đã ghi %s (13 ngày; không xuất mã học viên)." % args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
