"""Grade agent answers against benchmarks/results/truth.json.

    uv run python benchmarks/grade.py benchmarks/results/answers.json

answers.json: {"<arm>": {"T1": {...answer...}, "T2": {...}, ...}, ...}  (null for a failed run)
Prints per-field correctness and writes benchmarks/results/graded.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
TRUTH = json.loads((HERE / "results" / "truth.json").read_text(encoding="utf-8"))


def num(x):
    try:
        return float(str(x).replace(",", "").replace("٬", "").strip())
    except (TypeError, ValueError):
        return None


def close(a, b, rel=0.0, abs_=0.0):
    a, b = num(a), num(b)
    return a is not None and b is not None and abs(a - b) <= max(abs_, abs(b) * rel)


def norm(text):
    return str(text or "").replace("ي", "ی").replace("ك", "ک").replace(" ", "").replace("‌", "")


def grade_t1(ans, t):
    return {
        "last": close(ans.get("last"), t["last"]),
        "close": close(ans.get("close"), t["close"]),
        "change_pct": close(ans.get("change_pct"), t["change_pct"], abs_=0.02),
        "volume": close(ans.get("volume"), t["volume"]),
        "value_rial": close(ans.get("value_rial"), t["value_rial"], rel=0.001),
    }


def grade_t2(ans, t):
    return {
        "vwap": close(ans.get("vwap"), t["vwap"], abs_=0.05),
        "trades": close(ans.get("trades"), t["trades"]),
        "largest_trade_volume": close(ans.get("largest_trade_volume"), t["largest_trade_volume"]),
        "largest_trade_time": str(ans.get("largest_trade_time")) in t["largest_trade_times"],
    }


def grade_t3(ans, t):
    days = {str(k).replace("-", ""): v for k, v in (ans.get("days") or {}).items()}
    out = {"total": close(ans.get("total_net_real_value_rial"), t["total_net_real_value_rial"], rel=0.005)}
    for day, value in t["days"].items():
        out[f"day_{day}"] = close(days.get(day), value, rel=0.005)
    return out


def grade_t4(ans, t):
    expected = [q["symbol"] for q in t["top10"][:5]]
    got = [norm(x.get("symbol")) for x in (ans.get("top5") or [])][:5]
    exp_n = [norm(s) for s in expected]
    out = {"symbol_overlap_5": sum(1 for s in got if s in exp_n) == 5, "order_exact": got == exp_n}
    volumes = {norm(q["symbol"]): q["queue_volume"] for q in t["top10"]}
    out["volumes_ok"] = all(close(x.get("queue_volume"), volumes.get(norm(x.get("symbol"))), rel=0.02) for x in (ans.get("top5") or [])[:5]) and bool(got)
    return out


def grade_t5(ans, t):
    expected = [f["tracing_no"] for f in t["filings"]]
    got = [int(num(f.get("tracing_no")) or 0) for f in (ans.get("filings") or [])][:3]
    return {"tracing_numbers": got == expected, "titles": all(norm(g.get("title")) == norm(e["title"]) for g, e in zip(ans.get("filings") or [], t["filings"], strict=False)) and len(ans.get("filings") or []) >= 3}


GRADERS = {"T1": grade_t1, "T2": grade_t2, "T3": grade_t3, "T4": grade_t4, "T5": grade_t5}


def main(path: str) -> None:
    answers = json.loads(Path(path).read_text(encoding="utf-8"))
    graded: dict = {}
    for arm, tasks in answers.items():
        graded[arm] = {}
        for task_id, ans in tasks.items():
            if not isinstance(ans, dict):
                graded[arm][task_id] = {"fields": {}, "score": 0.0, "answered": False}
                continue
            fields = GRADERS[task_id](ans, TRUTH[task_id])
            graded[arm][task_id] = {"fields": fields, "score": round(sum(fields.values()) / len(fields), 3), "answered": True}
    Path(HERE / "results" / "graded.json").write_text(json.dumps(graded, ensure_ascii=False, indent=2), encoding="utf-8")
    for arm, tasks in graded.items():
        scores = [t["score"] for t in tasks.values()]
        print(f"{arm:12} mean accuracy {sum(scores) / len(scores):.0%}  " + "  ".join(f"{k}={v['score']:.0%}" for k, v in tasks.items()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(HERE / "results" / "answers.json"))
