"""Local web demo for Pre-Class Bottleneck Brief.

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
sys.path.insert(0, CODEBASE)


def _status():
    from ai import API_KEY, MODEL_NAME, MODEL_PROVIDER

    ready = MODEL_PROVIDER == "openai" and bool(API_KEY and MODEL_NAME)
    return {
        "provider": MODEL_PROVIDER,
        "model": MODEL_NAME if ready else ("fake" if MODEL_PROVIDER == "fake" else "chưa cấu hình"),
        "ready": ready,
    }


class DemoHandler(BaseHTTPRequestHandler):
    server_version = "PreClassDemo/1.0"

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

            tracing.begin("web-demo")
            try:
                result = answer(query)
            except Exception:
                summary, events = tracing.end()
                raise
            summary, events = tracing.end()
            state = _status()
            self._send(200, {
                "output": result.get("output", "") if isinstance(result, dict) else str(result),
                "model": ", ".join(summary["models"]) or state["model"],
                "provider": state["provider"],
                "model_calls": summary["model_calls"],
                "tool_calls": summary["tool_calls"],
                "tokens_in": summary["tokens_in"],
                "tokens_out": summary["tokens_out"],
                "latency_s": round(sum(event.get("latency_s", 0) for event in events), 2),
                "ready": state["ready"],
            })
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send(400, {"error": "Không đọc được yêu cầu JSON: %s" % exc})
        except Exception as exc:
            self._send(502, {"error": "%s: %s" % (type(exc).__name__, exc)})

    def log_message(self, fmt, *args):
        # Avoid echoing user input or API errors into the terminal log.
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
        from agent import answer  # noqa: F401 — fail early if the app flow cannot load
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
    print("Pre-Class Bottleneck Brief — giao diện demo")
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
