"""Command line entry point.

    iran-bourse-mcp                      run the MCP server on stdio (what MCP clients launch)
    iran-bourse-mcp serve --transport streamable-http --port 8000
    iran-bourse-mcp doctor               check TSETMC / Codal reachability
    iran-bourse-mcp tools                list every tool
    iran-bourse-mcp call quote symbol=فولاد       call a tool from the shell (for agents without MCP)
    iran-bourse-mcp config cursor        print setup text for a client
    iran-bourse-mcp install cursor       add the server to that client's config file
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from typing import Any

from . import __version__


async def _doctor() -> int:
    from .api import CDN, CODAL_SEARCH, WEBGW
    from .service import Bourse

    bourse = Bourse()
    checks = [
        ("TSETMC search       ", f"{CDN}/Instrument/GetInstrumentSearch/...", lambda: bourse.api.search("فولاد")),
        ("TSETMC market data  ", f"{CDN}/MarketData/GetMarketOverview/1", lambda: bourse.api.market_overview(1)),
        ("TSE gateway watch   ", f"{WEBGW}/.../MarketWatchCash", lambda: bourse.api.market_watch()),
        ("Codal search        ", CODAL_SEARCH, lambda: bourse.api.codal_search(Symbol="فولاد")),
    ]
    failed = 0
    print(f"iran-bourse-mcp {__version__} doctor\n")
    for label, target, call in checks:
        started = time.perf_counter()
        try:
            data = await call()
            size = len(data) if hasattr(data, "__len__") else "ok"
            print(f"  OK    {label} {time.perf_counter() - started:5.1f}s  ({size} records)")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  FAIL  {label} {target}\n        {exc}")
    await bourse.aclose()
    if failed:
        print(
            "\nSome sources are unreachable. TSETMC/Codal mostly serve Iranian IPs: run on a machine in Iran "
            "(no foreign VPN) or set IRAN_BOURSE_PROXY=http://host:port to an in-Iran proxy."
        )
        return 1
    print("\nAll sources reachable.")
    return 0


def _schema(tool: Any) -> dict:
    return getattr(tool, "inputSchema", None) or tool.input_schema


async def _tools(as_json: bool) -> int:
    from .server import mcp

    tools = await mcp.list_tools()
    if as_json:
        print(json.dumps(
            [{"name": t.name, "description": t.description, "parameters": _schema(t).get("properties", {}), "required": _schema(t).get("required", [])} for t in tools],
            ensure_ascii=False, indent=2,
        ))
        return 0
    for t in tools:
        first = (t.description or "").strip().splitlines()[0]
        params = ", ".join(f"{k}{'*' if k in _schema(t).get('required', []) else ''}" for k in _schema(t).get("properties", {}))
        print(f"{t.name:22} {first}\n{'':22} ({params})")
    return 0


def _parse_value(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _result_text(result: Any) -> str:
    """Normalise MCP SDK 1.x / 2.x ``call_tool`` return values to text."""
    if isinstance(result, tuple):
        result = result[0]
    if isinstance(result, dict):
        return json.dumps(result, ensure_ascii=False)
    content = getattr(result, "content", result)
    parts = [getattr(block, "text", None) for block in (content if isinstance(content, (list, tuple)) else [content])]
    return "\n".join(p for p in parts if p) or str(result)


async def _call(tool: str, pairs: list[str], raw_json: str | None, compact: bool) -> int:
    from .server import mcp

    arguments: dict[str, Any] = json.loads(raw_json) if raw_json else {}
    for pair in pairs:
        if "=" not in pair:
            print(f"Arguments must be key=value (got {pair!r}). Strings with spaces need quotes.", file=sys.stderr)
            return 2
        key, _, value = pair.partition("=")
        arguments[key] = _parse_value(value)
    try:
        text = _result_text(await mcp.call_tool(tool, arguments))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    try:
        data = json.loads(text)
        text = json.dumps(data, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(data, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        pass
    print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iran-bourse-mcp", description="MCP server for Tehran Stock Exchange (TSETMC) and Codal data.")
    parser.add_argument("--version", action="version", version=f"iran-bourse-mcp {__version__}")
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="run the MCP server (default)")
    serve.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], default="stdio")
    serve.add_argument("--host", default="127.0.0.1", help="bind address for HTTP transports")
    serve.add_argument("--port", type=int, default=8000, help="port for HTTP transports")

    sub.add_parser("doctor", help="check that TSETMC / Codal are reachable from this machine")

    tools = sub.add_parser("tools", help="list the available tools")
    tools.add_argument("--json", action="store_true", help="machine-readable output")

    call = sub.add_parser("call", help="call one tool from the shell and print JSON (for agents without MCP support)")
    call.add_argument("tool")
    call.add_argument("args", nargs="*", metavar="key=value", help="tool arguments; values are parsed as JSON when possible")
    call.add_argument("--json", dest="raw_json", help="all arguments as one JSON object")
    call.add_argument("--compact", action="store_true", help="single-line JSON (fewer tokens)")

    config = sub.add_parser("config", help="print setup instructions for an agent / IDE")
    config.add_argument("client", nargs="?", help="client id; omit to list them")

    install = sub.add_parser("install", help="add this server to a client's JSON config file (with backup)")
    install.add_argument("client")
    install.add_argument("--dry-run", action="store_true", help="show what would change")
    install.add_argument("--source", help="package source for uvx (default: GitHub; use 'pypi' once published)")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if args.command == "doctor":
        sys.exit(asyncio.run(_doctor()))
    if args.command == "tools":
        sys.exit(asyncio.run(_tools(args.json)))
    if args.command == "call":
        sys.exit(asyncio.run(_call(args.tool, args.args, args.raw_json, args.compact)))
    if args.command in ("config", "install"):
        from . import clients

        if args.command == "config":
            if not args.client:
                for c in clients.all_clients():
                    print(f"{c.id:16} {c.label}")
                return
            try:
                print(clients.snippet(args.client))
            except KeyError as exc:
                print(exc.args[0], file=sys.stderr)
                sys.exit(2)
            return
        try:
            print(clients.install(args.client, src=args.source, dry_run=args.dry_run))
        except (KeyError, clients.InstallError) as exc:
            print(exc.args[0] if exc.args else exc, file=sys.stderr)
            sys.exit(1)
        return

    from .server import mcp

    transport = getattr(args, "transport", "stdio")
    if transport == "stdio":
        mcp.run(transport="stdio")
        return
    try:  # SDK 1.x configures HTTP transports through settings
        mcp.settings.host = args.host
        mcp.settings.port = args.port
    except (AttributeError, ValueError):  # SDK 2.x takes them as run() arguments
        mcp.run(transport=transport, host=args.host, port=args.port)
    else:
        mcp.run(transport=transport)


if __name__ == "__main__":  # pragma: no cover
    main()
