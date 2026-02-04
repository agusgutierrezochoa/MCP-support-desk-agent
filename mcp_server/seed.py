import os

import asyncpg

DB_DSN = os.getenv("DB_DSN")

KB_ARTICLES = [
    ("Check sales endpoint", "Check before next black Friday"),
    ("Fix api codes", "For some reason, API is not returning 404 when resource not found"),
]


async def main() -> None:
    conn = await asyncpg.connect(DB_DSN)

    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS kb_articles (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                customer_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL
            );
        """)

        count = await conn.fetchval("SELECT COUNT(*) FROM kb_articles;")

        if count == 0:
            await conn.executemany(
                "INSERT INTO kb_articles(title, description) VALUES($1, $2);",
                KB_ARTICLES
            )
    finally:
        await conn.close()
