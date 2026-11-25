import json, runpy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
class H(BaseHTTPRequestHandler):
    def handle_any(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        try: body = json.loads(raw) if raw else {}
        except Exception: body = {"_raw": raw.decode(errors="replace")}
        try:
            ns = runpy.run_path("resp.py")
            code, resp = ns["respond"](self.command, self.path, dict(self.headers), body)
        except Exception as e:
            code, resp = 500, {"err": repr(e)}
        out = json.dumps(resp).encode()
        print(f"\n=== {self.command} {self.path} seq={self.headers.get('x-ads-sequence')}\nBODY {raw.decode(errors='replace')}\nRESP {code} {out.decode()}", flush=True)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
    do_GET = do_POST = do_PUT = handle_any
    def log_message(self, *a): pass
ThreadingHTTPServer(("127.0.0.1", 8088), H).serve_forever()
