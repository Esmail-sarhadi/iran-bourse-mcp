import pytest

from iran_bourse_mcp import shape


def tick(n, t, p, v, canceled=0):
    return {"nTran": n, "hEven": t, "pTran": p, "qTitTran": v, "canceled": canceled}


TICKS = [
    tick(1, 90000, 100, 1000),
    tick(2, 90030, 101, 500),
    tick(3, 90400, 101, 2000),
    tick(4, 90700, 99, 1500),
    tick(5, 90800, 99, 100, canceled=1),
]


def test_cancelled_ticks_are_excluded_and_counted():
    out = shape.aggregate_ticks(TICKS, interval_minutes=5)
    assert out["summary"]["ticks"] == 4 and out["summary"]["cancelled_ticks"] == 1
    assert out["summary"]["volume"] == 5000


def test_vwap_value_and_ohlc():
    s = shape.aggregate_ticks(TICKS)["summary"]
    expected_value = 100 * 1000 + 101 * 500 + 101 * 2000 + 99 * 1500
    assert s["value"] == expected_value
    assert s["vwap"] == pytest.approx(expected_value / 5000, abs=0.01)
    assert (s["open"], s["high"], s["low"], s["close"]) == (100, 101, 99, 99)
    assert (s["first_trade"], s["last_trade"]) == ("09:00:00", "09:07:00")


def test_bars_bucket_by_interval():
    bars = shape.aggregate_ticks(TICKS, interval_minutes=5)["bars"]
    assert [b["from"] for b in bars] == ["09:00", "09:05"]
    assert bars[0]["volume"] == 3500 and bars[0]["trades"] == 3 and bars[0]["close"] == 101
    assert bars[1]["volume"] == 1500 and bars[1]["open"] == 99


def test_completeness_against_official_totals():
    out = shape.aggregate_ticks(TICKS, official_volume=5000, official_count=4)
    assert out["completeness"]["volume_coverage_pct"] == 100.0
    assert out["completeness"]["count_coverage_pct"] == 100.0
    partial = shape.aggregate_ticks(TICKS, official_volume=10_000, official_count=8)
    assert partial["completeness"]["volume_coverage_pct"] == 50.0


def test_tick_rule_pressure_sums_to_100():
    p = shape.aggregate_ticks(TICKS)["pressure_estimate"]
    total = p["uptick_volume_pct"] + p["downtick_volume_pct"] + p["neutral_volume_pct"]
    assert total == pytest.approx(100, abs=0.05)
    assert p["uptick_volume_pct"] > 0 and p["downtick_volume_pct"] > 0


def test_biggest_trades_and_price_levels():
    out = shape.aggregate_ticks(TICKS, top_trades=1)
    assert out["biggest_trades"][0]["volume"] == 2000
    assert out["point_of_control"] == 101  # 2500 shares at 101 beats 1500 at 99 and 1000 at 100


def test_empty_input():
    assert shape.aggregate_ticks([])["ticks"] == 0


def test_shape_ticks_sorted_with_value():
    ticks = shape.shape_ticks(list(reversed(TICKS)))
    assert [t["n"] for t in ticks] == [1, 2, 3, 4]
    assert ticks[0] == {"n": 1, "time": "09:00:00", "price": 100.0, "volume": 1000, "value": 100000}


def test_real_fixture_ticks(fx):
    raw = fx("trades_head")
    out = shape.aggregate_ticks(raw)
    assert out["summary"]["ticks"] == len([r for r in raw if not r["canceled"]])
