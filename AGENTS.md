# Instructions for AI coding agents working on this repository

This file follows the AGENTS.md convention and is read by Codex, Claude Code, Cursor, Gemini CLI, Copilot and others.

## What this project is

`iran-bourse-mcp` is a **read-only** MCP server for Tehran Stock Exchange (TSETMC) and Codal data. Correctness of numbers is the product.

## Commands

```bash
uv sync
uv run pytest                      # offline, ~5 s, must stay green
uv run ruff check .                # must stay clean
uv run python scripts/smoke_live.py     # live check of every tool (needs access to TSETMC)
uv run python scripts/gen_tools_doc.py  # regenerate docs/TOOLS.md after changing tools
uv run python scripts/gen_site_data.py && uv run python scripts/gen_assets.py   # website data and artwork
```

Use `UV_PROJECT_ENVIRONMENT` to keep the virtualenv outside synced folders (for example OneDrive).

## Architecture in one paragraph

`server.py` registers tools -> `service.py` orchestrates upstream calls and defaults -> `shape.py` holds **pure** transformation logic (all the maths) -> `api.py`/`client.py` do HTTP with caching and retries. See `docs/ARCHITECTURE.md` and `docs/DATA_SOURCES.md` (known upstream quirks).

## Rules

1. Put logic in `shape.py` with a test; use recorded fixtures in `tests/fixtures`.
2. Anything the exchange does not publish must be named `estimate`/`estimated` and explained.
3. Prices and values are Rial; say so.
4. **Never** add order placement, login or credential handling.
5. Be gentle with the upstream servers: reuse the cache, never loop over the whole market per symbol.
6. Keep both MCP SDK generations working (`server.py` imports `MCPServer` or `FastMCP`); CI tests both.
7. Commit messages: plain, imperative, no attribution trailers.

## Installing the server for a user

If a user asks you to set this server up, follow [docs/llms-install.md](docs/llms-install.md).
