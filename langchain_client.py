import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["C:\\Users\\46760\\mcp-crash-course\\servers\\math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    # result = await agent.ainvoke({"messages": "What is 123456*78910?"})
    result = await agent.ainvoke({"messages": "What is the weather in San Francisco?"})

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
