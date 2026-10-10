import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.server"]
    )

    async with stdio_client(server_params) as (
        read,
        write
    ):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable tools:\n")

            for tool in tools.tools:
                print("-", tool.name)

            print("\n" + "=" * 40 + "\n")

            result = await session.call_tool(
                "get_progress",
                {}
            )
            print("PROGRESS")
            print(result)

            result = await session.call_tool(
                "get_topic_progress",
                {}
            )
            print("\nTOPICS")
            print(result)

            result = await session.call_tool(
                "get_weak_topics",
                {}
            )
            print("\nWEAK TOPICS")
            print(result)

            result = await session.call_tool(
                "get_due_revisions",
                {}
            )
            print("\nREVISIONS")
            print(result)

            result = await session.call_tool(
                "recommend_problems",
                {}
            )
            print("\nRECOMMENDATIONS")
            print(result)

            result = await session.call_tool(
                "get_today_plan",
                {}
            )
            print("\nTODAY PLAN")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
