"""Independent ground truth for the agent benchmark.

Deliberately does NOT import anything from iran_bourse_mcp: it recomputes every answer from the raw
upstream JSON with the simplest possible code, so the MCP server is graded against something it did
not produce.

    uv run python benchmarks/ground_truth.py     (run after the 12:30 Tehran close so data is stable)
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

CDN = "https://cdn.tsetmc.com/api"
WEBGW = "https://webgw.tse.ir"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
OUT = Path(__file__).parent / "results" / "truth.json"


def get(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def norm(text: str) -> str:
    return text.replace("ي", "ی").replace("ك", "ک").strip()


def main() -> None:
    rows = get(f"{CDN}/Instrument/GetInstrumentSearch/{urllib.parse.quote('فولاد')}")["instrumentSearch"]
    ins = next(r["insCode"] for r in rows if norm(r["lVal18AFC"]) == "فولاد")
    truth: dict = {"generated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), "ins_code": ins}

    # T1 quote
    c = get(f"{CDN}/ClosingPrice/GetClosingPriceInfo/{ins}")["closingPriceInfo"]
    truth["T1"] = {
        "date": c["dEven"],
        "last": c["pDrCotVal"],
        "close": c["pClosing"],
        "change_pct": round((c["pDrCotVal"] - c["priceYesterday"]) / c["priceYesterday"] * 100, 2),
        "volume": int(c["qTotTran5J"]),
        "value_rial": int(c["qTotCap"]),
    }

    # trading days
    daily = get(f"{CDN}/ClosingPrice/GetClosingPriceDailyList/{ins}/0")["closingPriceDaily"]
    days = sorted((r["dEven"] for r in daily if (r["zTotTran"] or 0) > 0), reverse=True)

    # T2 ticks of 2026-11-02
    ticks = [t for t in get(f"{CDN}/Trade/GetTradeHistory/{ins}/20261102/false")["tradeHistory"] if not t["canceled"]]
    volume = sum(t["qTitTran"] for t in ticks)
    biggest = max(t["qTitTran"] for t in ticks)
    truth["T2"] = {
        "date": 20261102,
        "vwap": round(sum(t["pTran"] * t["qTitTran"] for t in ticks) / volume, 2),
        "trades": len(ticks),
        "largest_trade_volume": int(biggest),
        "largest_trade_times": sorted({f"{t['hEven']:06d}"[:2] + ":" + f"{t['hEven']:06d}"[2:4] + ":" + f"{t['hEven']:06d}"[4:] for t in ticks if t["qTitTran"] == biggest}),
    }

    # T3 real net flow, last 3 trading days
    per_day = {}
    for d in days[:3]:
        h = get(f"{CDN}/ClientType/GetClientTypeHistory/{ins}/{d}")["clientType"]
        per_day[str(d)] = int(h["buy_I_Value"] - h["sell_I_Value"])
    truth["T3"] = {"days": per_day, "total_net_real_value_rial": sum(per_day.values())}

    # T4 genuine buy queues among ordinary shares
    watch = get(f"{WEBGW}/InstrumentProvider/api/v1/MarketWatch/MarketWatchCash/fa")["Items"]
    import datetime as dt

    d0 = get(f"{CDN}/MarketData/GetMarketOverview/1")["marketOverview"]["marketActivityDEven"]
    today = dt.date(d0 // 10000, d0 // 100 % 100, d0 % 100)
    ids: dict = {}
    for back in range(8):
        listing = get(f"{CDN}/ClosingPrice/GetInstrmentsHistoryInDay/{(today - dt.timedelta(days=back)):%Y%m%d}")["closingPriceDailyHistoryWithInstDetails"]
        if listing:
            ids = {r["instrumentID"]: r["insCode"] for r in listing}
            break
    securities = sorted({norm(w.get("securitiesname") or "") for w in watch})
    queues = []
    for w in watch:
        kind = norm(w.get("securitiesname") or "")
        if kind != "سهام عادی" or w["instrumentId"] not in ids:
            continue
        upper, last = w["maxValue"] or 0, w["lastPrice"]["value"] or 0
        if not upper or last < upper:
            continue
        book = get(f"{CDN}/BestLimits/{ids[w['instrumentId']]}")["bestLimits"]
        if sum(b["qTitMeOf"] for b in book) == 0 and book and book[0]["qTitMeDem"] > 0:
            top = book[0]
            queues.append({"symbol": norm(w["instrumentName"]), "queue_volume": int(top["qTitMeDem"]), "price": top["pMeDem"],
                           "queue_value": int(top["qTitMeDem"] * top["pMeDem"])})
    queues.sort(key=lambda q: q["queue_value"], reverse=True)
    truth["T4"] = {"security_kinds_seen": securities, "total_buy_queues": len(queues), "top10": queues[:10]}

    # T5 Codal
    letters = get(
        "https://search.codal.ir/api/search/v2/q?Symbol=" + urllib.parse.quote("فولاد")
        + "&PageNumber=1&Length=-1&Audited=true&NotAudited=true&Consolidatable=true&NotConsolidatable=true"
        "&Childs=true&Mains=true&Publisher=false&CompanyState=-1&Category=-1&CompanyType=-1&LetterType=-1"
    )["Letters"][:3]
    truth["T5"] = {"filings": [{"tracing_no": x["TracingNo"], "title": norm(x["Title"]), "published": x["PublishDateTime"]} for x in letters]}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(truth, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(truth, ensure_ascii=False, indent=2)[:3500])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
