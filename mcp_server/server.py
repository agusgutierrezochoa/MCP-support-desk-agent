import asyncio
import os
from typing import Any, Dict, List

import asyncpg
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Support Desk MCP (Postgres)", json_response=True)
DB_DSN = os.getenv("DB_DSN")


async def ensure_seeded() -> None:
    import seed
    await seed.main()


@mcp.tool()
async def search_kb(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    conn = await asyncpg.connect(DB_DSN)
    q = f"%{query.lower()}%"

    rows = await conn.fetch(
        """
        SELECT id, title, description
        FROM kb_articles
        WHERE lower(title) LIKE $1 OR lower(description) LIKE $1
        ORDER BY id
        LIMIT $2;
        """,
        q, limit
    )

    return [{"id": r["id"], "title": r["title"], "description": r["description"][:180]} for r in rows]


if __name__ == "__main__":
    asyncio.run(ensure_seeded())
