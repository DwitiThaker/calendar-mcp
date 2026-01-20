import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool(
            "book_appointment",
            {
                "title": "Holiday Test",
                "start_time": "2026-01-22T10:00:00+05:30",
                "end_time": "2026-01-22T10:30:00+05:30",
                "description": "Logging debug test"
            }
        )
        print(result)

asyncio.run(main())
