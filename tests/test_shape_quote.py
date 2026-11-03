from iran_bourse_mcp import shape


def test_quote_recomputes_change_instead_of_trusting_price_change(fx):
    closing, info = fx("closing_info"), fx("info")
    # The exchange's own priceChange field is 0.0 in this payload while the price clearly moved.
    assert closing["priceChange"] == 0.0
    quote = shape.shape_quote(closing, info)
    assert quote["last"]["change"] == closing["pDrCotVal"] - closing["priceYesterday"]
    assert quote["last"]["change_pct"] == round((closing["pDrCotVal"] / closing["priceYesterday"] - 1) * 100, 2)
    assert quote["units"] == "rial"


def test_quote_limits_vwap_and_market_cap(fx):
    closing, info = fx("closing_info"), fx("info")
    quote = shape.shape_quote(closing, info)
    thr = info["staticThreshold"]
    assert quote["price_limits"] == {"upper": thr["psGelStaMax"], "lower": thr["psGelStaMin"]}
    assert quote["vwap"] == round(closing["qTotCap"] / closing["qTotTran5J"], 2)
    assert quote["fundamentals"]["market_cap"] == int(closing["pDrCotVal"] * info["zTitad"])
    assert quote["at_upper_limit"] is (closing["pDrCotVal"] >= thr["psGelStaMax"])
    assert quote["status"]["title"] == "مجاز"


def test_pe_uses_estimated_eps(fx):
    info = fx("info")
    quote = shape.shape_quote(fx("closing_info"), info)
    eps = float(info["eps"]["estimatedEPS"])
    assert quote["fundamentals"]["eps"] == eps
    assert quote["fundamentals"]["pe"] == round(quote["last"]["price"] / eps, 2)


def test_identity_normalises_names_and_kind(fx):
    ident = shape.shape_identity(fx("info"))
    assert ident["symbol"] == "فولاد"
    assert "ك" not in ident["name"] and "ي" not in ident["name"]
    assert ident["instrument_kind"] == "stock"


def test_classify_instrument():
    assert shape.classify_instrument("IRT1AHRM0001", None) == "fund_unit"
    assert shape.classify_instrument("IRO9ZHRM4023", None) == "option_or_derivative"
    assert shape.classify_instrument("IRB4O2190884", None) == "bond_or_sukuk"
    assert shape.classify_instrument(None, None) == "unknown"
