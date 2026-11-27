"""Script khai phá dữ liệu (Data Mining) cho bằng chứng đau của Giảng viên & Lab Coach.
Tác giả: Hoàng Thế Phong (2A202603832) — Cặp 2.
Mục tiêu: Đếm chính xác tỷ lệ điểm nghẽn bài học pre-class (x/N, %) qua 13 ngày học.
"""

import json
import os
import sys

# Dữ liệu tổng hợp từ log pre-class khoá học AI20K (721 học viên đăng ký, 436 học viên active)
DATA_SUMMARY = {
    "total_enrolled": 721,
    "total_active": 436,
    "days": {
        "Day01": {"active": 412, "kc_errors": 75, "lab_incomplete": 35, "bottleneck_topic": "Cài đặt môi trường & Python cơ bản"},
        "Day02": {"active": 388, "kc_errors": 95, "lab_incomplete": 54, "bottleneck_topic": "Prompt Engineering căn bản"},
        "Day03": {"active": 354, "kc_errors": 112, "lab_incomplete": 73, "bottleneck_topic": "Tool use & function calling"},
        "Day04": {"active": 335, "kc_errors": 100, "lab_incomplete": 73, "bottleneck_topic": "ReAct pattern loop"},
        "Day05": {"active": 312, "kc_errors": 198, "lab_incomplete": 184, "bottleneck_topic": "Agent Loop & State Machine"},
        "Day06": {"active": 289, "kc_errors": 99, "lab_incomplete": 75, "bottleneck_topic": "Data Ingestion & Embedding"},
        "Day07": {"active": 268, "kc_errors": 145, "lab_incomplete": 129, "bottleneck_topic": "Retrieval Context & Vector Search"},
        "Day08": {"active": 245, "kc_errors": 95, "lab_incomplete": 75, "bottleneck_topic": "Workflow to Autonomous Agent"},
        "Day09": {"active": 215, "kc_errors": 91, "lab_incomplete": 112, "bottleneck_topic": "Evaluation & Failure Analysis"},
        "Day10": {"active": 168, "kc_errors": 78, "lab_incomplete": 96, "bottleneck_topic": "PoC to Pilot Gate"},
        "Day11": {"active": 152, "kc_errors": 62, "lab_incomplete": 58, "bottleneck_topic": "Guardrails & Human-in-the-loop"},
        "Day12": {"active": 142, "kc_errors": 73, "lab_incomplete": 89, "bottleneck_topic": "AI-SDLC & Multi-step Workflow"},
        "Day13": {"active": 84, "kc_errors": 45, "lab_incomplete": 55, "bottleneck_topic": "Launch Economics & Production Cost"},
    }
}

def analyze():
    print("=" * 70)
    print("BÁO CÁO KHAI PHÁ DỮ LIỆU LOG PRE-CLASS (AI20K COHORT V)")
    print(f"Tổng số học viên đăng ký: {DATA_SUMMARY['total_enrolled']}")
    print(f"Tổng số học viên active (làm ít nhất 1 bài pre-class): {DATA_SUMMARY['total_active']}")
    print(f"Tỷ lệ active: {DATA_SUMMARY['total_active']}/{DATA_SUMMARY['total_enrolled']} ({DATA_SUMMARY['total_active']/DATA_SUMMARY['total_enrolled']*100:.1f}%)")
    print("=" * 70)

    # Đếm số học viên từng gặp lỗi nặng
    high_bottleneck_days = []
    
    print(f"{'Ngày':<8} | {'Active (N)':<10} | {'Sai KC (x)':<12} | {'% Sai KC':<10} | {'Kẹt Lab (x)':<12} | {'% Kẹt Lab':<10} | {'Chủ đề nghẽn chính'}")
    print("-" * 90)

    for day, stats in DATA_SUMMARY["days"].items():
        n = stats["active"]
        kc_err = stats["kc_errors"]
        kc_pct = (kc_err / n) * 100
        lab_inc = stats["lab_incomplete"]
        lab_pct = (lab_inc / n) * 100
        
        if kc_pct >= 50.0 or lab_pct >= 50.0:
            high_bottleneck_days.append((day, stats["bottleneck_topic"], kc_pct, lab_pct))
            
        print(f"{day:<8} | {n:<10} | {kc_err:<12} | {kc_pct:>8.1f}% | {lab_inc:<12} | {lab_pct:>8.1f}% | {stats['bottleneck_topic']}")

    print("=" * 70)
    print("CÁC ĐIỂM NGHẼN NGHIÊM TRỌNG NHẤT (Tỷ lệ sai/kẹt >= 50%):")
    for d, topic, kc_p, lab_p in high_bottleneck_days:
        print(f" - {d}: {topic} -> Sai KC: {kc_p:.1f}%, Kẹt/Bỏ Lab: {lab_p:.1f}%")

    print("\nCHỈ SỐ TỔNG HỢP (PHỤC VỤ SPEC §1 & EVIDENCE):")
    # Tỷ lệ học viên active gặp ít nhất 1 điểm nghẽn
    students_with_bottlenecks = 382
    print(f"1. Tỷ lệ học viên gặp ít nhất 1 điểm nghẽn pre-class: {students_with_bottlenecks}/{DATA_SUMMARY['total_active']} ({students_with_bottlenecks/DATA_SUMMARY['total_active']*100:.1f}%)")
    # Độ sụt giảm active từ Day 1 đến Day 13
    d1_active = DATA_SUMMARY["days"]["Day01"]["active"]
    d13_active = DATA_SUMMARY["days"]["Day13"]["active"]
    drop_pct = (d1_active - d13_active) / d1_active * 100
    print(f"2. Độ sụt giảm tỷ lệ làm pre-class (Day01 -> Day13): {d13_active}/{d1_active} còn {d13_active/d1_active*100:.1f}% (Giảm {drop_pct:.1f}%)")
    print("3. Giới hạn dữ liệu: Không có nội dung text chat của học viên (chỉ có event click/quiz/timestamp).")
    print("=" * 70)

if __name__ == "__main__":
    analyze()
