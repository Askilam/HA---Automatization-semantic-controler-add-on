# web.py
# Small web page for the Home Assistant add-on (shown in the HA sidebar via Ingress).
# Uses only the Python standard library.
import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

import analysis

PORT = 8099

# Where Home Assistant's own automations.yaml is mounted inside the add-on.
CANDIDATE_PATHS = [
    os.environ.get("AUTOMATIONS_PATH", ""),
    "/homeassistant/automations.yaml",
    "/config/automations.yaml",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "automatizacia.yaml"),  # fallback: sample file
]

CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--card:#f4f5f7;--bad:#c62828;--rec:#b26a00;--ok:#2e7d32;--line:#d9dbe0}
@media (prefers-color-scheme:dark){:root{--bg:#111318;--fg:#e8e8e8;--card:#1c1f26;--bad:#ef9a9a;--rec:#ffcc80;--ok:#a5d6a7;--line:#2f333c}}
body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--fg);margin:0;padding:16px;max-width:900px}
h1{font-size:1.4rem;margin:0 0 4px} h2{font-size:1.05rem;margin:24px 0 8px}
.muted{opacity:.7;font-size:.9rem}
.item{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0}
.item b{display:block;margin-bottom:4px}
.bad{border-left:4px solid var(--bad)} .rec{border-left:4px solid var(--rec)} .ok{border-left:4px solid var(--ok)}
button{font:inherit;padding:8px 14px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
textarea{width:100%;box-sizing:border-box;min-height:160px;font-family:monospace;background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px}
"""


def find_automations_file():
    for path in CANDIDATE_PATHS:
        if path and os.path.isfile(path):
            return path
    return None


def render_items(items, css_class):
    parts = []
    for item in items:
        alias = html.escape(str(item.get("alias", "no alias")))
        message = html.escape(str(item.get("message", "")))
        parts.append(f'<div class="item {css_class}"><b>{alias}</b>{message}</div>')
    return "\n".join(parts)


def render_result(source_label, result):
    automations_ir, errors, problems, recommendations = result
    body = [f'<p class="muted">Source: {html.escape(source_label)} &middot; '
            f'automations tested: {len(automations_ir)}</p>']
    if not problems and not recommendations:
        body.append('<div class="item ok"><b>Result: OK</b>No problems or recommendations found.</div>')
    body.append(f"<h2>Problems ({len(problems)})</h2>")
    body.append(render_items(problems, "bad") or '<p class="muted">None.</p>')
    body.append(f"<h2>Recommendations ({len(recommendations)})</h2>")
    body.append(render_items(recommendations, "rec") or '<p class="muted">None.</p>')
    return "\n".join(body)


def render_page(content_html):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Automation Robustness Analyzer</title><style>{CSS}</style></head>
<body>
<h1>Automation Robustness Analyzer</h1>
<p class="muted">Semantic checks of Home Assistant automations.</p>
<form method="get" action="./"><button type="submit">Analyse my automations.yaml</button></form>
{content_html}
<h2>Or paste YAML to check</h2>
<form method="post" action="./analyze">
<textarea name="yaml" placeholder="- alias: my automation&#10;  trigger: ..."></textarea><br><br>
<button type="submit">Analyse pasted YAML</button>
</form>
</body></html>"""


def error_box(message):
    return f'<div class="item bad"><b>Could not analyse</b>{html.escape(message)}</div>'


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, status=200):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = find_automations_file()
        if path is None:
            self._send(render_page(error_box("No automations.yaml found. Paste YAML below instead.")))
            return
        try:
            result = analysis.analyze_file(path)
            self._send(render_page(render_result(path, result)))
        except Exception as exc:  # show the problem on the page instead of crashing
            self._send(render_page(error_box(f"{type(exc).__name__}: {exc}")))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        text = (form.get("yaml") or [""])[0]
        if not text.strip():
            self._send(render_page(error_box("The pasted text was empty.")))
            return
        try:
            result = analysis.analyze_text(text)
            self._send(render_page(render_result("pasted YAML", result)))
        except Exception as exc:
            self._send(render_page(error_box(f"{type(exc).__name__}: {exc}")))

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


if __name__ == "__main__":
    print(f"Automation Robustness Analyzer listening on port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
