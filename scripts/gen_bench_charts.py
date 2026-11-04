"""Export the website's benchmark charts as standalone, theme-aware SVGs for the README.

    uv run python scripts/gen_bench_charts.py          (needs Microsoft Edge or Chrome; serves docs/ itself)

The charts are drawn once, by docs/app.js. We load the site in headless Edge, take the rendered chart
markup and wrap each chart in a card with title, legend and light/dark colours.
"""

from __future__ import annotations

import http.server
import re
import shutil
import socketserver
import subprocess
import threading
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "assets"
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium", "chrome",
]
CHARTS = {
    "tokens": ("ch-tok", "lg-tok", "Tokens the model must read", "Log scale. Raw JSON payload vs the MCP response."),
    "time": ("ch-time", "lg-time", "Wall-clock time to the data", "Seconds. Sequential raw requests vs one tool call."),
    "requests": ("ch-req", "lg-req", "HTTP requests the agent must make", "Log scale. MCP always needs one call."),
    "accuracy": ("ch-acc", "lg-acc", "Agent trials: accuracy", "Share of fields correct against independent ground truth."),
}
COLOURS = {"--s1": ("#2a78d6", "#3987e5"), "--s2": ("#eb6834", "#d95926"), "--s3": ("#1baf7a", "#199e70")}


def find_browser() -> str:
    for candidate in BROWSERS:
        path = shutil.which(candidate) or (candidate if Path(candidate).exists() else None)
        if path:
            return path
    raise SystemExit("Edge or Chrome is required to export the charts")


def dump_dom(port: int) -> str:
    cmd = [find_browser(), "--headless=new", "--disable-gpu", "--window-size=1280,2400", "--virtual-time-budget=4000",
           "--lang=en-US", "--dump-dom", f"http://localhost:{port}/index.html"]
    return subprocess.run(cmd, capture_output=True, check=True).stdout.decode("utf-8", "replace")


def card(title: str, sub: str, legend: list[tuple[str, str]], chart_svg: str) -> str:
    height = float(re.search(r'viewBox="0 0 [\d.]+ ([\d.]+)"', chart_svg).group(1))  # type: ignore[union-attr]
    width = float(re.search(r'viewBox="0 0 ([\d.]+) ', chart_svg).group(1))  # type: ignore[union-attr]
    inner = re.sub(r"^<svg[^>]*>", "", chart_svg, count=1).removesuffix("</svg>")
    swatches, x = [], 24.0
    for var, label in legend:
        swatches.append(f'<rect x="{x}" y="66" width="12" height="12" rx="3" fill="var({var})"/><text class="lg" x="{x + 18}" y="76.5">{label}</text>')
        x += 40 + len(label) * 6.6
    total_h = 96 + height + 20
    light = "".join(f"{k}:{v[0]};" for k, v in COLOURS.items())
    dark = "".join(f"{k}:{v[1]};" for k, v in COLOURS.items())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width + 48:.0f} {total_h:.0f}" width="{width + 48:.0f}" role="img" aria-label="{title}">
<title>{title}</title>
<style>
svg{{{light}--ink:#0b1530;--ink2:#34426b;--muted:#5f6e95;--grid:#d9dfee;--card:#ffffff;--edge:#d5ddee;font-family:'Segoe UI','Inter',Helvetica,Arial,sans-serif}}
@media (prefers-color-scheme: dark){{svg{{{dark}--ink:#e8eef9;--ink2:#b6c3e0;--muted:#8fa1c7;--grid:#22305a;--card:#0e1730;--edge:#22305a}}}}
.t{{font-size:17px;font-weight:700;fill:var(--ink)}} .s{{font-size:12.5px;fill:var(--muted)}} .lg{{font-size:12.5px;fill:var(--ink2)}}
text{{fill:var(--ink2);font-size:13px}} .val{{font-family:ui-monospace,Consolas,monospace;font-size:11.5px;fill:var(--ink)}}
.tick{{font-family:ui-monospace,Consolas,monospace;font-size:10.5px;fill:var(--muted)}} .gridline{{stroke:var(--grid);stroke-width:1}}
</style>
<rect x=".5" y=".5" width="{width + 47:.0f}" height="{total_h - 1:.0f}" rx="14" fill="var(--card)" stroke="var(--edge)"/>
<text class="t" x="24" y="34">{title}</text><text class="s" x="24" y="54">{sub}</text>
{"".join(swatches)}
<g transform="translate(24 96)">{inner}</g>
</svg>'''


def main() -> None:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
    handler.log_message = lambda *a, **k: None  # type: ignore[method-assign]
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        dom = dump_dom(port)
        server.shutdown()
    for name, (chart_id, legend_id, title, sub) in CHARTS.items():
        match = re.search(rf'id="{chart_id}">(<svg.*?</svg>)', dom, re.S)
        legend_html = re.search(rf'id="{legend_id}">(.*?)</div>', dom, re.S)
        if not match or not legend_html:
            print(f"skip {name}: chart not rendered (no data yet?)")
            continue
        legend = re.findall(r'background:\s*var\((--s\d)\)"></i>([^<]+)</span>', legend_html.group(1))
        svg = card(title, sub, legend, match.group(1))
        (OUT / f"bench-{name}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote bench-{name}.svg")


if __name__ == "__main__":
    main()
