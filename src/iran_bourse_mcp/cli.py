"""Command line entry point: ``iran-bourse-mcp`` (serve) and ``iran-bourse-mcp doctor``."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time

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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="iran-bourse-mcp", description="MCP server for Tehran Stock Exchange data.")
    parser.add_argument("--version", action="version", version=f"iran-bourse-mcp {__version__}")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="run the MCP server (default)")
    serve.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], default="stdio")
    serve.add_argument("--host", default="127.0.0.1", help="bind address for HTTP transports")
    serve.add_argument("--port", type=int, default=8000, help="port for HTTP transports")
    sub.add_parser("doctor", help="check that TSETMC / Codal are reachable from this machine")
    args = parser.parse_args(argv)

    if args.command == "doctor":
        sys.exit(asyncio.run(_doctor()))

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
