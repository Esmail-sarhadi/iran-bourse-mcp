"""Render docs/promo.html into docs/assets/promo.mp4 (and a small GIF) with headless Edge/Chrome and ffmpeg.

    uv run python scripts/render_promo.py [--fps 20] [--keep-frames]

Every frame is a screenshot of promo.html?t=<seconds>, so the video is fully deterministic and reproducible.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import http.server
import shutil
import socketserver
import subprocess
import tempfile
import threading
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TOTAL = 15.5
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "msedge", "google-chrome", "chromium", "chrome",
]


def find(candidates: list[str], what: str) -> str:
    for c in candidates:
        path = shutil.which(c) or (c if Path(c).exists() else None)
        if path:
            return path
    raise SystemExit(f"{what} not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--keep-frames", action="store_true")
    args = parser.parse_args()
    browser = find(BROWSERS, "Edge or Chrome")
    ffmpeg = find(["ffmpeg"], "ffmpeg")
    frames_dir = Path(tempfile.mkdtemp(prefix="promo_frames_"))
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
    handler.log_message = lambda *a, **k: None  # type: ignore[method-assign]
    total_frames = int(TOTAL * args.fps)

    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()

        def frame(i: int) -> None:
            t = i / args.fps
            out = frames_dir / f"f{i:04d}.png"
            subprocess.run(
                [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                 "--virtual-time-budget=2500", f"--screenshot={out}", f"http://localhost:{port}/promo.html?t={t:.3f}"],
                check=True, capture_output=True,
            )

        with cf.ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(frame, range(total_frames)))
        server.shutdown()

    assets = DOCS / "assets"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(args.fps), "-i", str(frames_dir / "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(assets / "promo.mp4")], check=True)
    palette = frames_dir / "palette.png"
    scale = "fps=10,scale=560:-1:flags=lanczos"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(args.fps), "-i", str(frames_dir / "f%04d.png"),
                    "-vf", f"{scale},palettegen=max_colors=64", str(palette)], check=True)
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(args.fps), "-i", str(frames_dir / "f%04d.png"), "-i", str(palette),
                    "-lavfi", f"{scale}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4", str(assets / "promo.gif")], check=True)
    if not args.keep_frames:
        shutil.rmtree(frames_dir, ignore_errors=True)
    for name in ("promo.mp4", "promo.gif"):
        print(name, round((assets / name).stat().st_size / 1024), "KB")


if __name__ == "__main__":
    main()
