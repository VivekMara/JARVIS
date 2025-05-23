from concurrent import futures
import grpc.aio
import ai_agent_pb2_grpc
import ai_agent_pb2
from src.mcp_client import MCPClient
import asyncio
    
class AgentServicer(ai_agent_pb2_grpc.AgentServicer):
    async def QueryDeepseek(self, request, context):
        client = MCPClient()
        try:
            await client.connect_to_server("./src/mcp_servers/TaskManager.py")
            resp = await client.process_query(request.query, 5)
            print(f"Received: {request.query}")
            print(f"Response: {resp}")
            await client.cleanup()
            return ai_agent_pb2.Output(response="".join(resp))
        except Exception as e:
            print(f"Error: {e}")
            return ai_agent_pb2.Output(response=f"Error: {e}")
        

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_agent_pb2_grpc.add_AgentServicer_to_server(AgentServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Python gRPC Server running on port 50051...")

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down server...")
        await server.stop(grace=None)
        await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())