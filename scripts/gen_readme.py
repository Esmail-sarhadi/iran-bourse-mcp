"""Fill the generated blocks of README.md (install recipes, benchmark tables) from the code and results.

    uv run python scripts/gen_readme.py

Blocks live between <!-- NAME:START --> and <!-- NAME:END --> markers so the rest of the README stays hand-written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from iran_bourse_mcp import clients

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
RESULTS = ROOT / "benchmarks" / "results"


def install_block() -> str:
    out = ["<details>\n<summary><b>All agents and IDEs: copy-paste recipes (17)</b></summary>\n"]
    for c in clients.all_clients():
        if c.id == "generic":
            continue
        out.append(f"\n#### {c.label}\n")
        if c.command:
            out.append("```bash\n" + c.command + "\n```\n")
        if c.id == "codex":
            cmd, args = clients.launch()
            out.append(f"or in `{c.paths['all']}`:\n\n```toml\n[mcp_servers.{clients.SERVER_NAME}]\ncommand = \"{cmd}\"\nargs = {json.dumps(args)}\n```\n")
        elif c.id == "goose":
            out.append("```bash\n" + clients.shell_command() + "\n```\n\nPaste that into `goose configure` > Add Extension > Command-line Extension, or open the one-click link on the website.\n")
        elif c.config_key:
            body = {c.config_key: {clients.SERVER_NAME: clients.entry_for(c)}}
            if "all" in c.paths:
                where = f"`{c.paths['all']}`"
            elif c.paths:
                names = {"windows": "Windows", "macos": "macOS", "linux": "Linux"}
                where = "the config file (" + "; ".join(f"{names.get(os_name, os_name)}: `{path}`" for os_name, path in c.paths.items()) + ")"
            else:
                where = ""
            intro = f"Add to {where}:" if where else "Add this entry in the client's MCP settings:"
            out.append(intro + "\n\n```json\n" + json.dumps(body, indent=2) + "\n```\n")
        if c.auto_install:
            out.append(f"Or automatically (makes a backup first): `iran-bourse-mcp install {c.id}`\n")
        if c.note:
            out.append(f"> {c.note}\n")
    out.append("\n#### Python agent frameworks and plain shell\n")
    for f in clients.frameworks():
        out.append(f"**{f['label']}**\n\n```{f['language']}\n{f['snippet'].rstrip()}\n```\n")
    out.append("\n</details>\n")
    return "".join(out)


def fmt_int(n: float) -> str:
    return f"{int(round(n)):,}"


def bench_block(img_prefix: str = "docs/assets") -> str:
    parts: list[str] = []
    dp_path = RESULTS / "data_plane.json"
    if dp_path.exists():
        dp = json.loads(dp_path.read_text(encoding="utf-8"))
        for name in ("tokens", "time", "requests", "accuracy"):
            path = ROOT / "docs" / "assets" / f"bench-{name}.svg"
            if path.exists():
                parts.append(f'<img src="{img_prefix}/bench-{name}.svg" alt="Benchmark: {name}" width="49%">')
        if parts:
            parts = ['<div align="center">\n' + "\n".join(parts) + "\n</div>\n"]
        rows = ["| Task | Raw route | iran-bourse-mcp | Tokens saved |", "|---|---|---|---|"]
        for t in dp["tasks"]:
            raw, mcp = t["raw"], t["mcp"]
            rows.append(
                f"| {t['title']} | {raw['requests']:.0f} req · {raw['seconds']:.1f}s · {fmt_int(raw['tokens'])} tok | "
                f"1 call · {mcp['seconds']:.1f}s · {fmt_int(mcp['tokens'])} tok | **{t['token_reduction']:,.0f}x** |"
            )
        parts.append("\n".join(rows) + "\n")
        parts.append(
            f"_Data-plane benchmark, {dp['generated']}. Tokens are a tiktoken `o200k_base` proxy; the ratios matter more than the absolute numbers. "
            "A single-endpoint task takes about as long either way; the server wins where the raw route needs many sequential requests, and on tokens everywhere._\n"
        )
        traps = ["**Traps in the raw data** (each found on the live endpoints and handled by the server):\n", "| Trap | Naive reading | Correct |", "|---|---|---|"]
        for t in dp["traps"]:
            traps.append(f"| {t['what']} | `{json.dumps(t['naive_reading'], ensure_ascii=False)}` | `{json.dumps(t['correct'], ensure_ascii=False)}` |")
        parts.append("\n".join(traps) + "\n")
    ag_path = RESULTS / "agents.json"
    if ag_path.exists():
        ag = json.loads(ag_path.read_text(encoding="utf-8"))
        rows = ["| Agent | Accuracy | Net tokens (mean/task) | Time (mean/task) | Tool calls | Answered |", "|---|---|---|---|---|---|"]
        for arm in ag["arms"].values():
            runs = list(arm["runs"].values())
            n = len(runs)

            def mean(key: str, runs: list = runs, n: int = n) -> float:
                return sum(r.get(key) or 0 for r in runs) / n

            rows.append(
                f"| {arm['label_en']} | {mean('score') * 100:.0f}% | {fmt_int(mean('net_tokens'))} | {mean('seconds'):.0f}s | "
                f"{mean('tool_uses'):.1f} | {sum(1 for r in runs if r.get('answered'))}/{n} |"
            )
        parts.append(f"**Agent trials** ({ag.get('model', 'one model')}, {ag.get('date', '')}; {len(ag.get('tasks', []))} tasks, graded against independent ground truth):\n\n" + "\n".join(rows) + "\n")
        if ag.get("note"):
            parts.append(f"_{ag['note']}_\n")
    return "\n".join(parts) if parts else "_Benchmarks have not been generated yet: run `uv run python benchmarks/data_plane.py`._\n"


def replace(text: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"README.md has no {name} markers")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main() -> None:
    text = README.read_text(encoding="utf-8")
    text = replace(text, "INSTALL", install_block())
    text = replace(text, "BENCH", bench_block())
    README.write_text(text, encoding="utf-8")
    bench_readme = ROOT / "benchmarks" / "README.md"
    bench_readme.write_text(replace(bench_readme.read_text(encoding="utf-8"), "BENCH", bench_block("../docs/assets")), encoding="utf-8")
    print("README.md and benchmarks/README.md updated")


if __name__ == "__main__":
    main()
