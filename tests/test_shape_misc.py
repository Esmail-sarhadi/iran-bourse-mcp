import pytest

from iran_bourse_mcp import shape


# ----------------------------------------------------------------------- real / legal
def test_client_type_current_naming(fx):
    ct = fx("client_type")  # buy_CountI style keys
    out = shape.shape_client_type(ct, vwap=4208.49)
    assert out["real"]["buy"]["count"] == ct["buy_CountI"]
    assert out["real"]["buy"]["volume"] + out["legal"]["buy"]["volume"] == int(ct["buy_I_Volume"] + ct["buy_N_Volume"])
    assert out["real"]["buy"]["value_estimated"] is True
    assert out["real"]["net_volume"] == -out["legal"]["net_volume"]  # closed system between two groups


def test_client_type_history_naming_has_real_values(fx):
    ct = fx("client_type_history")  # buy_I_Count style keys + exact values
    out = shape.shape_client_type(ct)
    assert out["real"]["buy"]["count"] == int(ct["buy_I_Count"])
    assert out["real"]["buy"]["value"] == int(ct["buy_I_Value"])
    assert out["real"]["buy"]["value_estimated"] is False
    assert out["real"]["net_value"] == int(ct["buy_I_Value"] - ct["sell_I_Value"])
    assert out["real_buyer_power"] is not None


def test_buyer_power_is_ratio_of_per_capita_amounts():
    ct = {
        "buy_I_Volume": 1000, "buy_CountI": 10, "sell_I_Volume": 2000, "sell_CountI": 100,
        "buy_N_Volume": 0, "buy_CountN": 0, "sell_N_Volume": 0, "sell_CountN": 0,
    }
    out = shape.shape_client_type(ct)
    assert out["real_buyer_power"] == pytest.approx((1000 / 10) / (2000 / 100))


def test_client_type_series_sorted_by_date(fx):
    rows = [dict(fx("client_type_history"), recDate=20261103), dict(fx("client_type_history"), recDate=20261101)]
    series = shape.shape_client_type_history(rows)
    assert [s["date"] for s in series] == ["2026-11-01", "2026-11-03"]


# ----------------------------------------------------------------------- price history
def test_capital_increase_adjustment_is_continuous(fx):
    rows = fx("daily_prices_capital_increase")
    raw, _ = shape.shape_daily_prices(rows, adjusted=False)
    adj, events = shape.shape_daily_prices(rows, adjusted=True)
    assert len(raw) == len(adj) > 3
    assert len(events) == 1
    # 1500bn -> 1935bn shares is a 29% bonus/right issue: factor = 1500/1935
    assert events[0]["factor"] == pytest.approx(1500 / 1935, abs=0.002)
    jump = next(i for i in range(1, len(adj)) if adj[i]["close"] != raw[i]["close"] or adj[i - 1]["close"] != raw[i - 1]["close"])
    # adjusted series has no artificial gap on the ex-date
    ex_index = next(i for i in range(1, len(raw)) if raw[i]["date"] == events[0]["date"])
    assert abs(adj[ex_index]["close"] / adj[ex_index - 1]["close"] - 1) < 0.15
    assert abs(raw[ex_index]["close"] / raw[ex_index - 1]["close"] - 1) > 0.15
    assert jump >= 0
    # the most recent row is never altered
    assert adj[-1]["close"] == raw[-1]["close"]


def test_adjustment_synthetic_split():
    def day(d, close, yesterday):
        return {"dEven": d, "pClosing": close, "pDrCotVal": close, "priceYesterday": yesterday, "priceFirst": close,
                "priceMax": close, "priceMin": close, "qTotTran5J": 10, "qTotCap": 1000, "zTotTran": 3}

    rows = [day(20260101, 100, 100), day(20260102, 102, 100), day(20260103, 51, 51), day(20260104, 52, 51)]
    adj, events = shape.shape_daily_prices(rows, adjusted=True)
    assert [e["factor"] for e in events] == [0.5]
    assert [r["close"] for r in adj] == [50.0, 51.0, 51.0, 52.0]
    plain, no_events = shape.shape_daily_prices(rows, adjusted=False)
    assert no_events == [] and [r["close"] for r in plain] == [100, 102, 51, 52]


def test_tiny_rounding_differences_are_not_events():
    def day(d, close, yesterday):
        return {"dEven": d, "pClosing": close, "pDrCotVal": close, "priceYesterday": yesterday, "priceFirst": close,
                "priceMax": close, "priceMin": close, "qTotTran5J": 10, "qTotCap": 1000, "zTotTran": 3}

    rows = [day(20260101, 10000, 10000), day(20260102, 10005, 10000), day(20260103, 10010, 10004)]
    assert shape.shape_daily_prices(rows, adjusted=True)[1] == []


# ----------------------------------------------------------------------- holders
def test_holders_sorted_and_normalised(fx):
    holders = shape.shape_holders(fx("shareholders_last"))
    assert holders == sorted(holders, key=lambda h: -h["percent"])
    assert all("ي" not in h["name"] and "ك" not in h["name"] for h in holders)
    assert holders[0]["holder_id"] is not None


def test_holder_snapshots_compute_differences():
    def r(name, shares, pct, d):
        return {"shareHolderName": name, "numberOfShares": shares, "perOfShares": pct, "dEven": d}

    rows = [
        r("الف", 100, 10, 20260101), r("ب", 50, 5, 20260101),
        r("الف", 120, 12, 20260102), r("ج", 30, 3, 20260102),
    ]
    snaps = shape.shape_holder_snapshots(rows)
    assert [s["date"] for s in snaps] == ["2026-01-01", "2026-01-02"]
    second = {h["name"]: h for h in snaps[1]["holders"]}
    assert second["الف"]["shares_change"] == 20
    assert second["ج"]["new_in_list"] is True
    assert snaps[1]["dropped_from_list"] == ["ب"]


# ----------------------------------------------------------------------- market watch / codal
def test_watch_row_flattens_and_flags(fx):
    rows = [shape.shape_watch_row(r) for r in fx("market_watch_sample")]
    assert rows
    for row in rows:
        assert isinstance(row["last"], (float, type(None)))
        assert row["symbol"] and row["instrument_id"].startswith("IR")
        assert row["price_limits"]["upper"] is None or row["price_limits"]["upper"] >= row["price_limits"]["lower"]


def test_watch_row_queue_flags():
    base = {
        "instrumentName": "تست", "instrumentId": "IRO1TEST0001", "maxValue": 110, "minValue": 90,
        "lastPrice": {"value": 110}, "sellQuantity": {"value": None}, "buyQuantity": {"value": 500},
        "tradeVolume": {"value": 10}, "tradeValue": {"value": 1100},
    }
    row = shape.shape_watch_row(base)
    assert row["at_upper_limit"] and row["buy_queue_probable"] and not row["sell_queue_probable"]
    base["lastPrice"] = {"value": 90}
    base["buyQuantity"] = {"value": None}
    base["sellQuantity"] = {"value": 700}
    row = shape.shape_watch_row(base)
    assert row["at_lower_limit"] and row["sell_queue_probable"]


def test_codal_letter_links_are_absolute(fx):
    letter = shape.shape_codal_letter(fx("codal_letters")["Letters"][0])
    assert letter["links"]["page"].startswith("https://codal.ir/Reports/Decision.aspx?LetterSerial=")
    if letter["has"]["pdf"]:
        assert letter["links"]["pdf"].startswith("https://codal.ir/DownloadFile.aspx?hs=")
    assert letter["published"][:2] == "14"  # Jalali, ASCII digits
    assert "ي" not in letter["title"]


def test_index_row_splits_code_and_name():
    row = shape.shape_index_row({"lVal30": "01-زراعت", "insCode": 1, "xDrNivJIdx004": 100.0, "xVarIdxJRfV": 1.5, "indexChange": 1.5})
    assert (row["code"], row["name"]) == ("01", "زراعت")
    headline = shape.shape_index_row({"lVal30": "شاخص كل", "insCode": 2})
    assert headline["code"] is None and headline["name"] == "شاخص کل"
