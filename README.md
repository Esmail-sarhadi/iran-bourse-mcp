# iran-bourse-mcp

**Give your AI agent the whole Tehran Stock Exchange.** An open-source [Model Context Protocol](https://modelcontextprotocol.io) server for TSETMC (بورس تهران و فرابورس) and Codal: quotes, order book, tick-by-tick trades, real-vs-legal money flow, major shareholders, filings and more. Clean, unit-explicit and analysis-ready.

[فارسی](README.fa.md) · [Tool reference](docs/TOOLS.md) · [Data notes](docs/DATA_SOURCES.md)

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.10%2B-blue) ![mcp](https://img.shields.io/badge/MCP-SDK%201.x%20%26%202.x-8A2BE2) ![tools](https://img.shields.io/badge/tools-28%20read--only-green)

> Unofficial. Not affiliated with TSETMC, the Tehran Stock Exchange, Fara Bourse or Codal. Information only, **not investment advice**.

## Why this exists

An AI agent with a web browser cannot really read the Iranian market:

- `tsetmc.com` is a JavaScript shell. Fetching a symbol page returns an empty title (we tested it). Codal's report list comes back as unrendered `{{template}}` placeholders.
- The hidden JSON endpoints that do hold the data use cryptic names (`qTotTran5J`, `pMeDem`, `zOrdMeOf`) and have traps. For example the exchange's own `priceChange` field was `0.0` for a stock that rose 120 rial, the order-book history is a *delta feed* that must be reassembled, and shareholder rows are returned twice.
- A single day of ticks is 3 MB of JSON. Nobody should paste that into a context window.

`iran-bourse-mcp` finds the data, fixes the traps, reassembles what is fragmented, summarises what is huge and labels everything it infers.

## What you can ask

> «وضعیت فولاد رو کامل بررسی کن: صف، ورود پول حقیقی، سهامداران عمده و آخرین اطلاعیه‌های کدال»
> «امروز کدوم سهم‌ها صف خرید قوی دارن و پول حقیقی وارد شده؟»
> «ریز معاملات فولاد دیروز از ۱۰ تا ۱۱ رو خلاصه کن و بزرگ‌ترین معامله‌ها رو نشون بده»
> «سهامدار عمده شستا چه سهم‌های دیگه‌ای داره؟»
> «تاریخچه قیمت تعدیل‌شده خودرو در یک سال اخیر»

## Coverage

| Data | Tools |
|---|---|
| Market state, indices, industry indices | `market_status` `market_overview` `indices` `industry_summary` `index_contributors` |
| Whole-market screens (filter/sort ~590 instruments) | `market_watch` `top_movers` (gainers, losers, buy/sell queues, real-money inflow/outflow, buyer power) `market_snapshot` |
| One-call symbol dossier | `symbol_overview` |
| Price, limits, VWAP, P/E, market cap | `quote` `price_history` (optionally **back-adjusted**) `symbol_statistics` `corporate_actions` |
| Order book and queues (صف خرید/فروش) | `order_book` `order_book_history` (rebuilt from every event, with queue episodes) |
| Tick-by-tick trades (ریز معاملات) | `trades` (filterable) `trade_summary` (bars, VWAP, biggest trades, price levels, pressure estimate, **coverage check**) |
| Real vs legal investors (حقیقی/حقوقی) | `real_legal_flow` (per-capita, buyer power, net flow, daily history) |
| Shareholders (سهامداران عمده) | `shareholders` `shareholder_history` `shareholder_portfolio` `market_holder_moves` |
| Funds | `etf_nav` (premium/discount to issue and redemption NAV) |
| Codal | `codal_filings` (links to page, PDF, Excel) `codal_company` |
| Supervisor notices | `supervisor_messages` |
| Vocabulary | `glossary` (Persian ↔ English market terms) |

Also ships three prompts (`analyze_symbol`, `daily_market_report`, `smart_money_scan`) and a glossary resource.

### Verified, not assumed

Run against the live servers on 2026-11-03/04:

- **Ticks are complete.** For فولاد the 6,819 ticks of 3 Nov and the 15,643 ticks of 2 Nov matched the exchange's own daily totals at **100.0% of volume and trade count**. `trade_summary` reports this coverage on every call so you do not have to trust us. (A community reference claimed a 36-38% shortfall; we could not reproduce that.)
- **Price limits and queues** come from the day's actual allowed price range, not a guess.
- **Derived numbers are labelled.** Anything the exchange does not publish (tick-rule pressure, value of real flow outside history, adjusted prices) sits under an `estimate`/`estimated` key.
- 94 offline tests (recorded real fixtures) pass on both MCP SDK 1.x and 2.x, plus a live smoke test of every tool and an end-to-end stdio test: `scripts/smoke_live.py`, `scripts/e2e_stdio.py`.

## Install

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/). **Run it from a machine in Iran** (see below).

```bash
# check that TSETMC / Codal are reachable from here
uvx --from git+https://github.com/msmahdinejad/iran-bourse-mcp iran-bourse-mcp doctor
```

### Claude Code

```bash
claude mcp add iran-bourse -- uvx --from git+https://github.com/msmahdinejad/iran-bourse-mcp iran-bourse-mcp
```

### Claude Desktop / Cursor / any MCP client

```json
{
  "mcpServers": {
    "iran-bourse": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/msmahdinejad/iran-bourse-mcp", "iran-bourse-mcp"]
    }
  }
}
```

### From a clone

```bash
git clone https://github.com/msmahdinejad/iran-bourse-mcp && cd iran-bourse-mcp
uv sync
uv run iran-bourse-mcp doctor
uv run iran-bourse-mcp            # stdio server
```

## The Iranian IP requirement

TSETMC and Codal are built for Iranian users. Their servers often reject foreign or VPN addresses. So:

- Run the server on a machine in Iran, not behind a foreign VPN, **or**
- point it at an in-Iran proxy: `IRAN_BOURSE_PROXY=http://host:port`, **or**
- run it on an Iranian server and connect remotely over HTTP (use an SSH tunnel or a reverse proxy with authentication; the server has no auth of its own):

```bash
iran-bourse-mcp serve --transport streamable-http --host 127.0.0.1 --port 8000
```

`iran-bourse-mcp doctor` tells you which sources are reachable.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `IRAN_BOURSE_PROXY` | HTTP(S) proxy for all requests | none (system proxy variables are honoured) |
| `IRAN_BOURSE_TIMEOUT` | Request timeout, seconds | `45` |
| `IRAN_BOURSE_CDN_URL` | Override the TSETMC API base | `https://cdn.tsetmc.com/api` |
| `IRAN_BOURSE_WEBGW_URL` | Override the TSE gateway base | `https://webgw.tse.ir` |
| `IRAN_BOURSE_CODAL_URL` | Override the Codal search API | `https://search.codal.ir/api/search/v2/q` |

## Good to know

- Prices and values are in **Rial** (1 Toman = 10 Rial). Dates accept Gregorian (`2026-11-03`) or Jalali (`1405/08/12`, Persian digits fine).
- Persian/Arabic letter variants are interchangeable on input (`کگل` = `كگل`) and normalised on output.
- The market trades Saturday-Wednesday 09:00-12:30 Tehran time. Public holidays are not modelled. Outside the session you get the last session's data.
- **Order-book history for the current trading day may be partial.** TSETMC publishes the full intraday book history only after the day ends. `order_book_history` tells you when it is cut short (`events_span`, `warning`). Use `order_book` for the live book.
- The unofficial endpoints can change without notice. The test-suite uses recorded fixtures, and `scripts/smoke_live.py` re-checks every tool against the real servers.
- Requests are cached briefly (seconds for live data, hours for history) and limited to 6 in flight. Please be gentle: this is somebody else's server.

## Safety

All tools are read-only (`readOnlyHint`). There is deliberately **no order placement**, no login and no credential handling.

## Development

```bash
uv sync
uv run pytest                      # offline, ~3 s
uv run ruff check .
uv run python scripts/smoke_live.py     # needs access to TSETMC
uv run python scripts/e2e_stdio.py      # real MCP handshake against the live data
uv run python scripts/gen_tools_doc.py  # regenerate docs/TOOLS.md
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Roadmap

- Options chain and Greeks (derivatives board), IME commodity and energy bourse data
- Persian holidays calendar
- Portfolio and watchlist helpers
- Published PyPI release (`uvx iran-bourse-mcp`)

## License

[MIT](LICENSE). Market data belongs to its respective owners; check the exchange's terms before redistributing it.
