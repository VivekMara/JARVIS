from src.helpers.mcp_client import MCPClient

async def deepseek_client(server: str, query: str):
    client = MCPClient()
    if server == "TaskManager":
        try:
            await client.connect_to_server("/home/darthman/code/JARVIS/src/mcp_servers/TaskManager.py")
            resp = await client.process_query(query, 5)
        finally:
            await client.cleanup()
        return resp
    else:
        return "invalid path to mcp server"
