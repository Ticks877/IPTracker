#!/usr/bin/env python3
"""Consent-based IPTracker link diagnostic server.

Run this on a server you control. The page clearly tells visitors that basic
connection information is recorded for a network diagnostic test.
"""

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class DiagnosticHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown")
        timestamp = datetime.now(timezone.utc).isoformat()

        print("\n=== DIAGNOSTIC REQUEST ===")
        print(f"Time      : {timestamp}")
        print(f"IP        : {client_ip}")
        print(f"User-Agent: {user_agent}")

        body = """<!doctype html>
<html>
<head><meta charset="utf-8"><title>IPTracker Diagnostic</title></head>
<body>
<h1>IPTracker Network Diagnostic</h1>
<p>This is a consent-based network diagnostic test.</p>
<p>Your basic connection information has been recorded for this test.</p>
</body>
</html>"""
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        return


def main():
    host = input("Listen address [127.0.0.1]: ").strip() or "127.0.0.1"
    port_text = input("Port [8080]: ").strip() or "8080"
    port = int(port_text)

    print(f"\nIPTracker diagnostic server listening on http://{host}:{port}")
    print("Use only on infrastructure you control and with visitors' knowledge.")
    print("Press Ctrl+C to stop.\n")
    HTTPServer((host, port), DiagnosticHandler).serve_forever()


if __name__ == "__main__":
    main()
