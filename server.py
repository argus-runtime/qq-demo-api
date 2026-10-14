"""A tiny JSON API on the standard library, for trying qq."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def add(a: int, b: int) -> int:
    return a + b


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body, status = {"status": "ok"}, 200
        elif self.path.startswith("/add/"):
            try:
                a, b = (int(x) for x in self.path.removeprefix("/add/").split("/"))
                body, status = {"result": add(a, b)}, 200
            except ValueError:
                body, status = {"error": "use /add/<int>/<int>"}, 400
        else:
            body, status = {"error": "not found"}, 404
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
