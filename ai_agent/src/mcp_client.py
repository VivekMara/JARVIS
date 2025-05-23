from contextlib import AsyncExitStack
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()
apiKey = os.getenv("deepseek-api-key")

class MCPClient:
    def __init__(self):
        self.deepseek = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.mcp_servers_path = "./mcp_servers"
           
    async def connect_to_server(self, server_path:str):
        server_params = StdioServerParameters(command="python", args=[server_path], env=None)

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        return tools
    
    async def process_query(self, query: str, max_iterations: int):
            current_iteration = 0
            msgs = [
                {
                "role": "system",
                "content": "You are JARVIS, a personal AI assistant.You run in a loop of Thought, Action, PAUSE, Observation. At the end of the loop you output an Answer.Use Thought to describe your thoughts about the question or command you have been given.Use Action to run one of the available actions - then return PAUSE.Observation will be the result of running those actions."
            },
            {
                "role": "user",
                "content": query
            }
            ]
            final_text = []
            response = await self.session.list_tools()

            available_tools = []
            for tool in response.tools:
                tool_desc = {
                    "type":"function",
                    "function":{
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                available_tools.append(tool_desc)

            while current_iteration < max_iterations:
                current_iteration += 1
                resp = self.deepseek.chat.completions.create(
                    model="deepseek-chat",
                    max_tokens=1000,
                    messages=msgs,
                    tools=available_tools
                )
                message = resp.choices[0].message
                if message.tool_calls is None:
                    final_text.append(message.content)
                    msgs.append({
                        "role": "assistant",
                        "content": str(message.content)
                    })
                    return final_text
                else:
                    for tool_call in message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        result = await self.session.call_tool(tool_name, tool_args)
                        self.console.print(f"[Calling tool {tool_name} with args {tool_args}]")
                        msgs.append({
                            "role": "assistant",
                            "content": f"Action: {tool_name}({tool_args})\nPAUSE"
                        })
                        msgs.append({
                            "role": "user",
                            "content": f"Observation: {result.content}"
                        })
            return final_text

    async def cleanup(self):
        await self.exit_stack.aclose()
