# Data sources and known quirks

Three public, **unofficial** sources are used. None has documented stability guarantees. Every item below was observed on the live servers (2 to 4 November 2026) while building this project.

| Source | Base URL | Key for an instrument | Used for |
|---|---|---|---|
| TSETMC API | `https://cdn.tsetmc.com/api` | `insCode` (numeric string) | quotes, history, order book, ticks, real/legal, shareholders, messages, Codal attachments |
| TSE gateway | `https://webgw.tse.ir` | `instrumentId` (e.g. `IRO1FOLD0001`) | whole-market watch (590 rows incl. P/E, EPS, industry, board, limits), market open flags |
| Codal search | `https://search.codal.ir/api/search/v2/q` | `Symbol` | filings with page/PDF/Excel/attachment links |

`instrumentId` (gateway) and `insCode` (TSETMC) are joined through `GetInstrmentsHistoryInDay`, which carries both.

All requests need a browser-like `User-Agent`; without one TSETMC answers 403.

## Endpoint map

| Tool | Endpoints |
|---|---|
| `quote`, `symbol_overview` | `Instrument/GetInstrumentInfo`, `ClosingPrice/GetClosingPriceInfo` |
| `order_book` | `BestLimits/{ins}`, thresholds from `GetInstrumentInfo` |
| `order_book_history` | `BestLimits/{ins}/{date}`, `MarketData/GetStaticThreshold/{ins}/{date}` |
| `trades`, `trade_summary` | `Trade/GetTrade/{ins}` (latest day), `Trade/GetTradeHistory/{ins}/{date}/false`, totals from `ClosingPrice/GetClosingPriceDailyList` |
| `price_history` | `ClosingPrice/GetClosingPriceDailyList/{ins}/0` |
| `real_legal_flow` | `ClientType/GetClientType/{ins}/1/0`, `ClientType/GetClientTypeHistory/{ins}/{date}` |
| `top_movers` (real_*) | `ClientType/GetClientTypeAll`, `ClosingPrice/GetInstrmentsHistoryInDay/{date}`, gateway market watch |
| queues in `top_movers` | gateway market watch to find limit-locked symbols, then `BestLimits/{ins}` for the true queue size |
| `shareholders` | `Shareholder/GetInstrumentShareHolderLast/{ins}` |
| `shareholder_history` | `Shareholder/{ins}/{date}` |
| `shareholder_portfolio` | `Shareholder/GetShareHolderCompanyList/{holderId}` |
| `market_holder_moves` | `Shareholder/GetShareHolderChanges/false` |
| `corporate_actions` | `ClosingPrice/GetPriceAdjustList/{ins}`, `Instrument/GetInstrumentShareChange/{ins}` |
| `symbol_statistics` | `MarketData/GetInstrumentStatistic/{ins}` |
| `etf_nav` | `Fund/GetETFByInsCode/{ins}` |
| `indices`, `market_overview` | `Index/GetIndexB1LastAll/All/{flow}`, `MarketData/GetMarketOverview/{flow}` (`flow` 1 = bourse, 2 = Fara Bourse) |
| `supervisor_messages` | `Msg/GetMsgByInsCode/{ins}`, `Msg/GetMsgByFlow/{flow}/{top}` |
| `codal_filings` | Codal search API |
| `codal_company` | `Codal/GetCodalPublisherBySymbol/{symbol}` |

## Quirks we found, and what we do about them

1. **`closingPriceInfo.priceChange` is unreliable.** It was `0.0` for a stock that closed 120 rial above yesterday. We recompute change from `pDrCotVal` (last trade) / `pClosing` (closing price) and `priceYesterday`.
2. **Two prices.** `pClosing` is the exchange's closing (weighted) price, `pDrCotVal` is the last trade. Both are returned (`last`, `close`).
3. **Order-book history is a delta feed.** Each `refID` lists only the levels that changed (1 to 5 rows). We rebuild full 5-level snapshots by carrying unchanged levels forward. Events are not limited to the session: orders entered before the open (from about 06:00) and after the close (until about 14:30) are recorded too, so `order_book_history` defaults to 08:30-12:35.
4. **Order-book history for the current day is partial.** On the day we measured, the endpoint stopped at about 09:02 for the current trading day but covered the full session for the previous day. We expose `events_span` and a `warning` instead of pretending.
5. **Tick data is complete.** `Trade/GetTradeHistory` and `GetTrade` matched the exchange's own totals exactly (6,819 and 15,643 trades, 100% of volume) for فولاد on two days. `trade_summary.completeness` repeats this check on every call.
6. **Field names differ between endpoints.** Counts are `buy_CountI` in `GetClientType` but `buy_I_Count` in `GetClientTypeHistory`; only the history variant carries Rial values. We accept both. Current-day values in `real_legal_flow.latest_session` are therefore *estimated* (volume x VWAP) and flagged `value_estimated`.
7. **`Shareholder/{ins}/{date}` returns each holder under two dates** (a current and a neighbouring snapshot). `shareholders` uses `GetInstrumentShareHolderLast` (clean, 1%+ holders); `shareholder_history` groups the dated rows and computes differences.
8. **ETF endpoint is stock-hostile.** `GetETFByInsCode` returns HTTP 500 for non-fund instruments. `etf_nav` converts that to a clear "not a fund" answer.
9. **Search is fuzzy.** `GetInstrumentSearch` returns about 41 hits for any query. We pick the exact normalised symbol match (Arabic ي/ك and Persian ی/ک are equal), preferring the lowest `flow` id when a symbol exists on several boards, and otherwise fail with suggestions.
10. **Gateway top-of-book is empty outside the session.** Queue detection from market-watch alone would call every limit-up stock a queue. `top_movers(kind="buy_queue")` therefore confirms candidates against the real order book.
11. **Adjusted prices are inferred.** TSETMC's `GetPriceAdjustList` covers dividend adjustments but omits many capital increases (e.g. فولاد 2026-03-30, 1500bn to 1935bn shares, factor 0.775). We infer adjustment events from the series itself: on an ex-date `priceYesterday` no longer equals the previous `pClosing`. Differences under 0.1% are treated as tick rounding. Very old rows (before about 2014) sometimes lack this continuity.
12. **Dates.** `dEven` is a Gregorian `YYYYMMDD` integer, `hEven` is `HHMMSS` (no leading zero, so `90013` is 09:00:13). `GetChartData` uses a nonstandard timestamp, so we do not use it.
13. **Text.** TSETMC stores Arabic letters (ي ك). We normalise returned text to Persian letters.
14. **Payload sizes.** A day of ticks is about 3 MB, order-book history 3 MB, supervisor messages for one symbol 3.5 MB, full daily price history 1.5 MB. Responses are cached for a short time and summarised before they reach the model.

## Not covered (yet)

Options chains and Greeks, IME commodity and energy bourse, index constituents' weights, intraday index series, Persian holiday calendar.
