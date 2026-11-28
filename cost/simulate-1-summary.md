# Tóm tắt mô phỏng simulate-1@20261127-224811

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_chinh | 17 | 1 | 863 | 304 | 0.9 | 3.2 |
| lab_coach_truc_lop | 24 | 1 | 840 | 274 | 0.9 | 3.2 |
| key_coach_lead | 9 | 2 | 1414 | 471 | 1.6 | 5.6 |

Tỉ lệ đạt dùng để tính: 23/26 (88%) — lượt run-2@20261127-224608

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (40 người) | Chi phí / tháng — cơ sở (84 người) | Chi phí / tháng — cao (120 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00033 (≈ 8 ₫) | $0.00038 (≈ 10 ₫) | $0.00032 (≈ 8 ₫) | $0.1230 (≈ 3.123 ₫) | $0.2582 (≈ 6.558 ₫) | $0.3689 (≈ 9.369 ₫) | $0.0031 (≈ 78 ₫) |
| gpt-6.2-sol (vào 2.0 · ra 10.0 $/1M) | $0.0051 (≈ 130 ₫) | $0.0058 (≈ 146 ₫) | $0.0049 (≈ 124 ₫) | $1.87 (≈ 47.578 ₫) | $3.93 (≈ 99.914 ₫) | $5.62 (≈ 142.734 ₫) | $0.0468 (≈ 1.189 ₫) |
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00072 (≈ 18 ₫) | $0.00081 (≈ 21 ₫) | $0.00069 (≈ 17 ₫) | $0.2634 (≈ 6.690 ₫) | $0.5531 (≈ 14.048 ₫) | $0.7901 (≈ 20.069 ₫) | $0.0066 (≈ 167 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.2) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-4o-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ (Tỷ giá tham khảo (tự ghi theo quy ước bảng giá BTC)).
