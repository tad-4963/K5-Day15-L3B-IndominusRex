"""Script khai phá dữ liệu (Data Mining) từ file tổng hợp ẩn danh `data/lesson_signals_agg.json`.

File `data/lesson_signals_agg.json` được sinh trực tiếp từ `data/preclass/*.csv`
bằng `scripts/build_lesson_signals.py` (không chứa mã học viên `hv`).
Chạy lệnh: python scripts/mine_evidence.py
"""
import json
import os
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGG_PATH = os.path.join(ROOT, "data", "lesson_signals_agg.json")
TOTAL_ENROLLED = 721
TOTAL_ACTIVE = 436


def analyze():
    with open(AGG_PATH, encoding="utf-8") as f:
        payload = json.load(f)
    days = payload["days"]

    print("=" * 96)
    print("BÁO CÁO KHAI PHÁ DỮ LIỆU PRE-CLASS (TỪ data/lesson_signals_agg.json — 05/11–25/11/2026)")
    print(f"Tổng tài khoản: {TOTAL_ENROLLED} | Học viên có hoạt động: {TOTAL_ACTIVE}/{TOTAL_ENROLLED} ({TOTAL_ACTIVE/TOTAL_ENROLLED*100:.1f}%)")
    print("=" * 96)
    print(f"{'Ngày':<6} | {'Active':>6} | {'KC sai (lần 1)':<16} | {'KC khó nhất (n>=5)':<44} | {'Lab skip/inc cao nhất'}")
    print("-" * 120)

    total_kc_wrong = 0
    total_kc_ans = 0
    days_with_heavy_kc = []
    days_with_heavy_lab = []
    low_sample_days = []

    for day in sorted(days.keys()):
        d = days[day]
        active = d["active_learners"]
        if active < 50:
            low_sample_days.append((day, active))

        kcs = d.get("kc_stats") or {}
        w_sum = sum(v["wrong"] for v in kcs.values())
        t_sum = sum(v["total"] for v in kcs.values())
        total_kc_wrong += w_sum
        total_kc_ans += t_sum
        kc_rate = (w_sum / t_sum * 100) if t_sum else 0.0

        hard_kcs = sorted(
            [(v["wrong"] / v["total"] * 100, v["wrong"], v["total"], k) for k, v in kcs.items() if v["total"] >= 5],
            reverse=True,
        )
        top_kc_str = f"{hard_kcs[0][3]} ({hard_kcs[0][1]}/{hard_kcs[0][2]}={hard_kcs[0][0]:.1f}%)" if hard_kcs else "không có KC n>=5"
        if hard_kcs and hard_kcs[0][0] >= 35.0:
            days_with_heavy_kc.append((day, hard_kcs[0]))

        labs = d.get("lab_stats") or {}
        lab_issues = []
        for lk, lv in labs.items():
            op = lv["open"]["count"]
            sk = lv["skip"]["count"]
            inc = lv["incomplete"]["count"]
            if op > 0:
                unfin = sk + inc
                lab_issues.append((unfin / op * 100, sk, inc, op, lk))
        lab_issues.sort(reverse=True)
        top_lab_str = (
            f"{lab_issues[0][4]} (skip {lab_issues[0][1]} + inc {lab_issues[0][2]}/{lab_issues[0][3]}={lab_issues[0][0]:.1f}%)"
            if lab_issues
            else "—"
        )
        if lab_issues and lab_issues[0][3] >= 10 and lab_issues[0][0] >= 40.0:
            days_with_heavy_lab.append((day, lab_issues[0]))

        print(f"{day:<6} | {active:>6} | {w_sum:>3}/{t_sum:<4} ({kc_rate:>5.1f}%) | {top_kc_str:<44} | {top_lab_str}")

    d01 = days["Day01"]["active_learners"]
    d12 = days["Day12"]["active_learners"]
    d13 = days["Day13"]["active_learners"]
    print("=" * 96)
    print(f"Tổng câu trả lời KC lần đầu (Day01–Day13): sai {total_kc_wrong}/{total_kc_ans} ({total_kc_wrong/total_kc_ans*100:.1f}%)")
    print(f"Số ngày có KC (n>=5) sai >= 35%: {len(days_with_heavy_kc)}/13 ngày")
    print(f"Số ngày có Mini Lab (open>=10) skip+incomplete >= 40%: {len(days_with_heavy_lab)}/13 ngày")
    print(f"Drop-off active: Day01 ({d01}) -> Day12 ({d12}, giảm {(d01-d12)/d01*100:.1f}%) | Day13 ({d13}, giảm {(d01-d13)/d01*100:.1f}%)")
    print(f"Các ngày mẫu nhỏ (active < 50): {', '.join(f'{d} ({a})' for d, a in low_sample_days)}")
    print("=" * 96)


if __name__ == "__main__":
    analyze()
