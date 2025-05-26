from fastapi import FastAPI
from .mcp_client import MCPClient
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def hello():
    return {"message":"Hello darthman"}


class Query(BaseModel):
    query: str

@app.post("/query")
async def query(query: Query):
    client = MCPClient()
    await client.connect_to_server("./mcp_servers/TaskManager.py")
    resp = await client.process_query(query.query, 5)
    await client.cleanup()
    return {"message":resp}