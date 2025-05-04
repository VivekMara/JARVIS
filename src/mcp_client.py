import os
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from typing import Optional
from contextlib import AsyncExitStack
import asyncio

load_dotenv()
apiKey = os.getenv("deepseek_api_key")
baseURL = os.getenv("base_url")

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.deepseek = OpenAI(api_key=apiKey, base_url=baseURL)

    async def connect_to_server(self, server_path:str):
        server_params = StdioServerParameters(command="python", args=[server_path], env=None)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        resp = await self.session.list_tools()
        tools = resp.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query:str) -> str:
        msgs = [{
            "role" : "user",
            "content" : query
        }]

        # resp = await self.session.list_tools()
        # available_tools = [{
        #         "name": tool.name,
        #         "description": tool.description,
        #         "input_schema": tool.inputSchema
        #     } for tool in resp.tools]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather of an location, the user shoud supply a location first",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            }
                        },
                        "required": ["location"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "evaluate",
                    "description": "Mathematical evaluation of any two numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "int",
                                "description": "The first number to be evaluated",
                            },
                            "b": {
                                "type": "int",
                                "description": "The second number to be evaluated",
                            }
                        },
                        "required": ["a","b"]
                    },
                }
            },
        ]
        resp = self.deepseek.chat.completions.create(
            model = "deepseek-chat",
            messages=msgs,
            stream=False,
            tools=tools
        )
        choice = resp.choices[0].message

        final_text = []
        assistant_message_content = []
        tool = {}

        if choice.tool_calls == None:
            final_text.append(choice.message.content)
            assistant_message_content.append(choice.message.content)
        else:
            for i in choice.tool_calls:
                tool["name"] = i.function.name
                tool["args"] = i.function.arguments
        print(choice)

        print(tool)



async def main():
    client = MCPClient()
    try:
        await client.process_query("How's the weather in Hangzhou? and what is the sum of 2 and 4")
    finally:
        print("GOODBYE")


asyncio.run(main())
