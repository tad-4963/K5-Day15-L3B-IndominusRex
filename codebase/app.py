"""Local web demo & statistics dashboard for Pre-Class Bottleneck Brief.

Run with ``python run.py`` and open http://127.0.0.1:8765.
The old terminal interface remains available with ``python codebase/app.py --cli``.
Only the Python standard library is used.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CODEBASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CODEBASE)
HTML_PATH = os.path.join(CODEBASE, "demo.html")
SIGNALS_PATH = os.path.join(ROOT, "data", "lesson_signals_agg.json")
RAW_PRECLASS_DIR = os.path.join(ROOT, "data-btc", "preclass")
sys.path.insert(0, CODEBASE)

# Official BTC price reference (25/11/2026) for live per-query estimate (USD / 1M tokens)
_MODEL_PRICES = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-5-nano": (0.05, 0.40),
    "gpt-5-mini": (0.25, 2.00),
    "gpt-6.2-sol": (2.00, 10.00),
    "gemini-3.1-flash-lite": (0.25, 1.50),
}
_USD_TO_VND = 25400


def _status():
    from ai import API_KEY, MODEL_NAME, MODEL_PROVIDER

    ready = MODEL_PROVIDER == "openai" and bool(API_KEY and MODEL_NAME)
    has_raw = os.path.isdir(RAW_PRECLASS_DIR) and os.path.isfile(os.path.join(RAW_PRECLASS_DIR, "answers.csv"))
    return {
        "provider": MODEL_PROVIDER,
        "model": MODEL_NAME if ready else ("fake" if MODEL_PROVIDER == "fake" else "chưa cấu hình"),
        "ready": ready,
        "has_raw_data": has_raw,
        "data_source": "data-btc/preclass → data/lesson_signals_agg.json" if has_raw else "data/lesson_signals_agg.json",
    }


def _load_signals_payload():
    if not os.path.isfile(SIGNALS_PATH):
        return {"days": {}, "overview": {"total_enrolled": 721, "total_active": 436}}
    with open(SIGNALS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    days = raw.get("days", {}) if isinstance(raw, dict) else {}
    total_kc_wrong = 0
    total_kc_ans = 0
    days_out = {}
    for day in sorted(days.keys()):
        d = days[day]
        kcs = d.get("kc_stats") or {}
        kc_list = []
        w_sum, t_sum = 0, 0
        for name, v in kcs.items():
            w, t = int(v.get("wrong", 0)), int(v.get("total", 0))
            if t > 0:
                w_sum += w
                t_sum += t
                kc_list.append({"name": name, "wrong": w, "total": t, "rate": round(100.0 * w / t, 1)})
        kc_list.sort(key=lambda x: (-x["rate"], -x["total"], x["name"]))
        total_kc_wrong += w_sum
        total_kc_ans += t_sum

        labs = d.get("lab_stats") or {}
        lab_list = []
        for lk, lv in labs.items():
            op = int((lv.get("open") or {}).get("count", 0))
            sk = int((lv.get("skip") or {}).get("count", 0))
            inc = int((lv.get("incomplete") or {}).get("count", 0))
            if op > 0:
                done = max(0, op - sk - inc)
                lab_list.append({
                    "name": lk,
                    "open": op,
                    "skip": sk,
                    "skip_rate": round(100.0 * sk / op, 1),
                    "incomplete": inc,
                    "incomplete_rate": round(100.0 * inc / op, 1),
                    "done": done,
                    "done_rate": round(100.0 * done / op, 1),
                    "unfin_rate": round(100.0 * (sk + inc) / op, 1),
                })
        lab_list.sort(key=lambda x: (-x["unfin_rate"], -x["open"], x["name"]))

        active = int(d.get("active_learners", 0))
        low_sample = active < 30 or (len(kc_list) > 0 and all(x["total"] < 10 for x in kc_list[:3]))
        days_out[day] = {
            "day": day,
            "active_learners": active,
            "low_sample": low_sample,
            "kc_wrong_total": w_sum,
            "kc_ans_total": t_sum,
            "kc_wrong_rate": round(100.0 * w_sum / t_sum, 1) if t_sum else 0.0,
            "kc_list": kc_list,
            "lab_list": lab_list,
            "top_asked_videos": (d.get("top_asked_videos") or [])[:5],
            "missing_context_count": d.get("missing_context_count", 0),
        }

    return {
        "overview": {
            "total_enrolled": 721,
            "total_active": 436,
            "active_rate": 60.5,
            "total_days": len(days_out),
            "total_kc_wrong": total_kc_wrong,
            "total_kc_ans": total_kc_ans,
            "total_kc_wrong_rate": round(100.0 * total_kc_wrong / total_kc_ans, 1) if total_kc_ans else 0.0,
            "has_raw_data": _status()["has_raw_data"],
        },
        "days": days_out,
    }


def _estimate_cost(model_name, tokens_in, tokens_out):
    p_in, p_out = _MODEL_PRICES.get(model_name, (0.15, 0.60))
    usd = (tokens_in * p_in + tokens_out * p_out) / 1_000_000.0
    return round(usd, 6), round(usd * _USD_TO_VND, 1)


class DemoHandler(BaseHTTPRequestHandler):
    server_version = "PreClassDemo/2.0"

    def _send(self, status, value, content_type="application/json; charset=utf-8"):
        if isinstance(value, str):
            body = value.encode("utf-8")
        else:
            body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            try:
                with open(HTML_PATH, encoding="utf-8") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except OSError as exc:
                self._send(500, {"error": "Không đọc được giao diện demo: %s" % exc})
            return
        if path == "/api/status":
            try:
                self._send(200, _status())
            except Exception as exc:
                self._send(500, {"error": "%s: %s" % (type(exc).__name__, exc)})
            return
        if path == "/api/signals":
            try:
                self._send(200, _load_signals_payload())
            except Exception as exc:
                self._send(500, {"error": "%s: %s" % (type(exc).__name__, exc)})
            return
        self._send(404, {"error": "Không tìm thấy đường dẫn."})

    def do_POST(self):
        if urlparse(self.path).path != "/api/ask":
            self._send(404, {"error": "Không tìm thấy đường dẫn."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 12000:
                self._send(400, {"error": "Yêu cầu phải có nội dung và không vượt quá 12 KB."})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            query = str(payload.get("query", "") if isinstance(payload, dict) else "").strip()
            if not query:
                self._send(400, {"error": "Hãy nhập câu hỏi trước khi gửi."})
                return
            if len(query) > 2000:
                self._send(400, {"error": "Câu hỏi tối đa 2.000 ký tự."})
                return

            import tracing
            from agent import answer
            from tools import parse_and_guard_request

            # Preview parsed days / guardrail status for UI sync
            parsed = parse_and_guard_request(query)

            tracing.begin("web-demo")
            try:
                result = answer(query)
            except Exception:
                tracing.end()
                raise
            summary, events = tracing.end()
            state = _status()
            used_model = ", ".join(summary["models"]) or ("code-guardrail" if summary["model_calls"] == 0 else state["model"])
            cost_usd, cost_vnd = _estimate_cost(state["model"], summary["tokens_in"], summary["tokens_out"])
            trace_steps = [
                {
                    "kind": ev.get("kind", ev.get("type", "step")),
                    "name": ev.get("name", ev.get("model", "")),
                    "latency_ms": round(float(ev.get("latency_s", 0)) * 1000, 1),
                }
                for ev in events
            ]
            self._send(200, {
                "output": result.get("output", "") if isinstance(result, dict) else str(result),
                "model": used_model,
                "provider": state["provider"],
                "model_calls": summary["model_calls"],
                "tool_calls": summary["tool_calls"],
                "tokens_in": summary["tokens_in"],
                "tokens_out": summary["tokens_out"],
                "latency_s": round(sum(event.get("latency_s", 0) for event in events), 2),
                "cost_usd": cost_usd,
                "cost_vnd": cost_vnd,
                "blocked": bool(parsed.get("blocked")),
                "need_clarify": bool(parsed.get("need_clarify")),
                "detected_days": parsed.get("lesson_ids", []),
                "focus": parsed.get("focus", "all"),
                "trace_steps": trace_steps,
                "ready": state["ready"],
            })
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send(400, {"error": "Không đọc được yêu cầu JSON: %s" % exc})
        except Exception as exc:
            self._send(502, {"error": "%s: %s" % (type(exc).__name__, exc)})

    def log_message(self, fmt, *args):
        sys.stdout.write("[web-demo] %s\n" % (fmt % args))


def _cli_main():
    try:
        import tracing
        from agent import answer
    except Exception as exc:
        import traceback as tb
        path = getattr(exc, "filename", None) or (tb.extract_tb(exc.__traceback__)[-1].filename if exc.__traceback__ else "")
        if path:
            path = os.path.relpath(os.path.abspath(path), ROOT).replace(os.sep, "/")
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (path or "codebase/", type(exc).__name__, exc))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print("Pre-Class Bottleneck Brief — hỏi điểm nghẽn theo ngày (vd: Day05 lớp kẹt gì?).")
    print("Chỉ dùng số liệu tổng hợp; không hỗ trợ truy vấn cá nhân. Thoát: Ctrl+C hoặc Enter 2 lần.")
    blank = 0
    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not query:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        tracing.begin("app-cli")
        try:
            result = answer(query)
        except NotImplementedError as exc:
            tracing.end()
            print("Chưa nối model: %s" % exc)
            return 1
        except Exception as exc:
            tracing.end()
            print("[lỗi] %s: %s" % (type(exc).__name__, exc))
            continue
        summary, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(summary["models"]) or "—", summary["model_calls"], summary["tool_calls"],
                 summary["tokens_in"], summary["tokens_out"]))


def main() -> int:
    if "--cli" in sys.argv[1:]:
        return _cli_main()
    try:
        from ai import MODEL_PROVIDER, MODEL_NAME
        from agent import answer  # noqa: F401
    except Exception as exc:
        print("Không nạp được codebase/ — %s: %s" % (type(exc).__name__, exc))
        print("Kiểm tra codebase/agent.py và docs/connect-model.md")
        return 1

    host = os.environ.get("DEMO_HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("DEMO_PORT", "8765"))
    except ValueError:
        print("DEMO_PORT phải là số nguyên.")
        return 2
    try:
        server = HTTPServer((host, port), DemoHandler)
    except OSError as exc:
        print("Không mở được giao diện tại %s:%d — %s" % (host, port, exc))
        return 1
    print("Pre-Class Bottleneck Brief — Dashboard & AI Demo")
    print("Mở trình duyệt: http://%s:%d" % (host, port))
    print("Model: %s%s · Dừng server: Ctrl+C"
          % (MODEL_PROVIDER, (" / " + MODEL_NAME) if MODEL_NAME else ""))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng giao diện demo.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
