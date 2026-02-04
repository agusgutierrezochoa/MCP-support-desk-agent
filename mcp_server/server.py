import asyncio


async def ensure_seeded() -> None:
    import seed
    await seed.main()


if __name__ == "__main__":
    asyncio.run(ensure_seeded())
