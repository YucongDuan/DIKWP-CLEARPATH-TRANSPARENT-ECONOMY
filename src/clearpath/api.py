from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .models import OpportunitySpec, PersonProfile
from .portfolio import analyze_portfolio
from .viability import analyze_opportunity


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "external_action_authority": 0})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in {"/analyze", "/portfolio"}:
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                raise ValueError("request too large")
            data = json.loads(self.rfile.read(length))
            person = PersonProfile.from_dict(data["person"])
            if self.path == "/analyze":
                result = analyze_opportunity(person, OpportunitySpec.from_dict(data["opportunity"]))
            else:
                result = analyze_portfolio(person, [OpportunitySpec.from_dict(item) for item in data["opportunities"]])
            self._send(200, result)
        except Exception as exc:
            self._send(400, {"error": str(exc)})

    def log_message(self, format: str, *args) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765, allow_nonloopback: bool = False) -> int:
    if host not in {"127.0.0.1", "localhost", "::1"} and not allow_nonloopback:
        raise ValueError("Reference server refuses non-loopback binding")
    server = ThreadingHTTPServer((host, port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0
