"""Start the server as a subprocess and talk MCP to it, exactly like Claude Desktop would.

    uv run python scripts/e2e_stdio.py
"""

from __future__ import annotations

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def is_error(result) -> bool:  # SDK 1.x: isError, SDK 2.x: is_error
    return bool(getattr(result, "isError", getattr(result, "is_error", False)))


async def main() -> int:
    params = StdioServerParameters(command=sys.executable, args=["-m", "iran_bourse_mcp"])
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        print(f"{len(tools.tools)} tools:", ", ".join(t.name for t in tools.tools))
        for name, args in [
            ("market_status", {}),
            ("quote", {"symbol": "فولاد"}),
            ("top_movers", {"kind": "real_inflow", "limit": 3}),
        ]:
            result = await session.call_tool(name, args)
            text = result.content[0].text if result.content else ""
            print(f"\n{name}: error={is_error(result)} {len(text)} chars\n{text[:300]}")
            if is_error(result):
                return 1
        bad = await session.call_tool("quote", {"symbol": "نماد-نادرست"})
        print("\nunknown symbol ->", is_error(bad), json.dumps((bad.content[0].text if bad.content else ""), ensure_ascii=False)[:200])
        prompts = await session.list_prompts()
        print("prompts:", [p.name for p in prompts.prompts])
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
