from fastapi import FastAPI
from src.helpers.mcp_client import MCPClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

class Request(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query(request: Request):
    query = request.query
    apiKey = os.getenv("deepseek-api-key")
    client = MCPClient(apiKey)
    try:
        await client.connect_to_server(
            "/home/darthman/code/JARVIS/src/mcp_servers/TaskManager.py"
        )
        resp = await client.process_query(query, 5)
    finally:
        await client.cleanup()
    return {
        "data": resp
    }
