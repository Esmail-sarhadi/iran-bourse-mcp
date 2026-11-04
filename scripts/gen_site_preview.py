"""Screenshot the website for the README (desktop hero and a Persian phone view).

    uv run python scripts/gen_site_preview.py       (needs Microsoft Edge or Chrome)
"""

from __future__ import annotations

import http.server
import shutil
import socketserver
import subprocess
import threading
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium", "chrome",
]


def browser() -> str:
    for candidate in BROWSERS:
        path = shutil.which(candidate) or (candidate if Path(candidate).exists() else None)
        if path:
            return path
    raise SystemExit("Edge or Chrome is required")


def shot(port: int, name: str, width: int, height: int, query: str, scale: float = 1.0) -> None:
    cmd = [browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={width},{height}",
           f"--force-device-scale-factor={scale}", "--virtual-time-budget=4000", f"--screenshot={DOCS / 'assets' / name}",
           f"http://localhost:{port}/index.html{query}"]
    subprocess.run(cmd, check=True, capture_output=True)
    print("wrote", name)


def main() -> None:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
    handler.log_message = lambda *a, **k: None  # type: ignore[method-assign]
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        shot(port, "site-preview.png", 1280, 800, "", 1.0)
        server.shutdown()


if __name__ == "__main__":
    main()
