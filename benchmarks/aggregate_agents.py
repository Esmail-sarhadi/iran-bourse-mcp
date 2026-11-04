"""Grade recorded agent runs and write benchmarks/results/agents.json (what the site and README read).

    uv run python benchmarks/aggregate_agents.py

Input : benchmarks/results/agent_runs.json (raw tokens/seconds/tool calls and the final JSON answer of each run)
Output: benchmarks/results/agents.json with per-run score, net tokens (minus the harness's fixed per-agent
        overhead, measured with a do-nothing agent) and the arms' labels.
"""

from __future__ import annotations

import json
from pathlib import Path

import grade

HERE = Path(__file__).parent
RESULTS = HERE / "results"


def main() -> None:
    runs = json.loads((RESULTS / "agent_runs.json").read_text(encoding="utf-8"))
    tasks_def = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]
    base = runs["base_tokens"]
    out_arms = {}
    for arm, spec in runs["arms"].items():
        arm_runs = {}
        for task_id, entry in spec["runs"].items():
            repeats = entry if isinstance(entry, list) else [entry]  # one run, or several repeats of the same task
            graded = []
            for run in repeats:
                fields = grade.GRADERS[task_id](run["answer"], grade.TRUTH[task_id])
                graded.append({
                    "score": sum(fields.values()) / len(fields),
                    "tokens": run["tokens"],
                    "net_tokens": max(run["tokens"] - base[arm], 0),
                    "seconds": run["seconds"],
                    "tool_uses": run["tool_uses"],
                    "answered": any(v is not None for v in run["answer"].values()),
                    "fields": fields,
                })
            mean = lambda key, g=graded: sum(r[key] for r in g) / len(g)  # noqa: E731
            arm_runs[task_id] = {
                "n_runs": len(graded),
                "score": round(mean("score"), 3),
                "scores": [round(r["score"], 3) for r in graded],
                "tokens": round(mean("tokens")),
                "net_tokens": round(mean("net_tokens")),
                "seconds": round(mean("seconds"), 1),
                "tool_uses": round(mean("tool_uses"), 1),
                "answered": all(r["answered"] for r in graded),
                "fields": graded[0]["fields"],
            }
        out_arms[arm] = {"label_en": spec["label_en"], "label_fa": spec["label_fa"], "runs": arm_runs}
    titles_fa = {
        "T1": "قیمت لحظه‌ای", "T2": "ریز معاملات یک روز", "T3": "پول حقیقی ۳ روز", "T4": "صف خرید کل بازار", "T5": "اطلاعیه‌های کدال", "T6": "بازده تعدیل‌شده یک‌ساله",
    }
    out = {
        "model": runs["model"],
        "date": runs["date"],
        "base_tokens": base,
        "tasks": [{"id": t["id"], "title_en": t["title"], "title_fa": titles_fa.get(t["id"], t["title"])} for t in tasks_def if any(t["id"] in a["runs"] for a in out_arms.values())],
        "arms": out_arms,
        "note": runs.get("note", ""),
    }
    (RESULTS / "agents.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    for spec in out_arms.values():
        rs = list(spec["runs"].values())
        print(f"{spec['label_en']:42} acc {sum(r['score'] for r in rs) / len(rs):.0%}  net tok {sum(r['net_tokens'] for r in rs) / len(rs):>8,.0f}  "
              f"time {sum(r['seconds'] for r in rs) / len(rs):>5.0f}s  calls {sum(r['tool_uses'] for r in rs) / len(rs):.1f}")


if __name__ == "__main__":
    main()
