# Changelog

## 0.2.0 (2026-11-04)

- **Fix:** `top_movers` queue and real-money rankings returned nothing during the session (today's end-of-day table is empty until the close). The instrument index now falls back to the newest published day.
- **Fix:** gateway failures (HTTP 502/503) are retried more patiently and reported as an overloaded exchange, not as an IP problem.
- New CLI: `tools`, `call` (every tool from the shell, for agents without MCP), `config <client>` and `install <client>` (safe merge into the client's JSON config, with backup).
- Install recipes, one-click deep links (Cursor, VS Code, Goose) and framework snippets for 17 agents and IDEs, generated from one table.
- Website (GitHub Pages) with a promo video, animated README artwork, benchmark harness (`benchmarks/`) with independent ground truth, real example outputs (`docs/EXAMPLES.md`).
- Container image, AGENTS.md, llms.txt and an install guide written for AI agents, code of conduct, citation file, dependabot.
- Tests: 142 offline tests, 89% line coverage (service layer 96%).

## 0.1.0 (2026-11-04)

First public release.

- 28 read-only tools covering market state, indices, whole-market screens, quotes, order book (live and rebuilt history with queue episodes), tick-by-tick trades with aggregation and a coverage check, real/legal flow, shareholders, corporate actions, adjusted price history, fund NAV, Codal filings and supervisor notices.
- 3 prompts and a glossary resource.
- Persian/Arabic text normalisation, Jalali/Gregorian date handling.
- Works with MCP Python SDK 1.x and 2.x.
- `iran-bourse-mcp doctor` connectivity check; `serve` for stdio / streamable-http / sse.
