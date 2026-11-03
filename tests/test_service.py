"""Service-level tests with a fake API backed by recorded fixtures (no network)."""

from __future__ import annotations

import pytest
from conftest import load

from iran_bourse_mcp.service import Bourse, InputError


class FakeApi:
    def __init__(self) -> None:
        self.info = load("info")
        self.closing = load("closing_info")
        self.trades = load("trades_head")
        day = int(self.closing["dEven"])
        volume = sum(t["qTitTran"] for t in self.trades if not t["canceled"])
        value = sum(t["qTitTran"] * t["pTran"] for t in self.trades if not t["canceled"])
        # an "official" daily row that exactly matches the 60 recorded ticks
        self.daily = [{"dEven": day, "zTotTran": len(self.trades), "qTotTran5J": volume, "qTotCap": value}]

    async def search(self, query):
        return load("search_folad")

    async def instrument_info(self, ins):
        return self.info

    async def closing_info(self, ins):
        return self.closing

    async def best_limits(self, ins):
        return load("best_limits")

    async def best_limits_history(self, ins, deven, ttl=0):
        return load("best_limits_history_head")

    async def thresholds(self, ins, deven):
        return []

    async def trades_latest(self, ins):
        return self.trades

    async def trades_history(self, ins, deven, ttl=0):
        return self.trades

    async def daily_prices(self, ins):
        return self.daily

    async def client_type(self, ins):
        return load("client_type")

    async def shareholders_last(self, ins):
        return load("shareholders_last")


@pytest.fixture()
def bourse():
    b = Bourse()
    fake = FakeApi()
    b.api = fake
    b.resolver._api = fake
    return b


async def test_quote_pipeline(bourse):
    out = await bourse.quote("فولاد")
    assert out["instrument"]["symbol"] == "فولاد"
    assert out["last"]["change_pct"] is not None
    assert out["jdate"].startswith("14")


async def test_order_book_has_queue_field(bourse):
    out = await bourse.order_book("فولاد")
    assert set(out["queue"]) == {"state", "queue_volume", "queue_orders", "queue_value"}
    assert out["as_of"]["date"] == out["as_of"]["date"][:10]


async def test_trades_filters_by_volume_and_time_and_limit(bourse):
    everything = await bourse.trades("فولاد", limit=1000)
    assert everything["matched"] == 60 and not everything["truncated"]
    big = await bourse.trades("فولاد", min_volume=100_000, limit=1000)
    assert 0 < big["matched"] < 60 and all(t["volume"] >= 100_000 for t in big["trades"])
    first = everything["trades"][0]["time"]
    windowed = await bourse.trades("فولاد", from_time=first, to_time=first, limit=1000)
    assert windowed["matched"] >= 1 and all(t["time"] == first for t in windowed["trades"])
    capped = await bourse.trades("فولاد", limit=5)
    assert capped["returned"] == 5 and capped["truncated"]
    newest = await bourse.trades("فولاد", limit=1, newest_first=True)
    assert newest["trades"][0]["n"] == everything["trades"][-1]["n"]


async def test_trade_summary_reports_full_coverage(bourse):
    out = await bourse.trade_summary("فولاد", interval_minutes=1)
    assert out["completeness"]["volume_coverage_pct"] == 100.0
    assert out["completeness"]["count_coverage_pct"] == 100.0
    assert out["bars"]


async def test_order_book_history_flags_partial_day(bourse):
    out = await bourse.order_book_history("فولاد", date="2026-11-02", from_time="00:00", to_time="23:59")
    assert out["events_span"]["covers_full_session"] is False  # fixture holds only the first events
    assert out["warning"]


async def test_real_legal_flow_latest_only(bourse):
    out = await bourse.real_legal_flow("فولاد", days=0)
    assert "history" not in out and out["latest_session"]["real"]["buy"]["count"] > 0


async def test_shareholders_summary(bourse):
    out = await bourse.shareholders("فولاد")
    assert out["listed_holders"] == len(out["holders"])
    assert 0 < out["top5_percent"] <= out["listed_percent_total"] <= 100


async def test_input_validation(bourse):
    with pytest.raises(InputError):
        await bourse.market_overview("nasdaq")
    with pytest.raises(InputError):
        await bourse.top_movers("moon")
    with pytest.raises(InputError):
        await bourse.trades("فولاد", date="not-a-date")
    with pytest.raises(InputError):
        await bourse.trades("فولاد", from_time="25:99")
