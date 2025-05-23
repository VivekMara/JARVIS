import grpc
import ai_agent_pb2_grpc
import ai_agent_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ai_agent_pb2_grpc.AgentStub(channel=channel)
        print("--- Calling QueryDeepseek ---")
        response = stub.QueryDeepseek(ai_agent_pb2.Input(query="list all my tasks"))
        print(f"Deepseek says: {response.response}")

    
if __name__ == "__main__":
    run()