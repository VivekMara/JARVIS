import httpx
from tools import add_memory, tool_calling, get_current_weather, ollama_chat_post_req, ollama_generate_post_req




client = httpx.Client()




while True:
    inp = input("USER: ")
    if inp == "q":
        print("GOOD BYE")
        break
    data_list = tool_calling(inp)
    if data_list[2] == None:
        add_memory(user_input=inp, ollama_client=client)
    if data_list[1] == "get_current_weather":
        resp = get_current_weather(data_list[2])
        payload_data_with_weather = {
                "model" : "llama3.2:3b",
                "prompt" : f"You are an AI agent who has already used the tools to get the weather details at the place {inp} which has the weather forecast of {resp} celsius, your task is to tell this data to the user casually.",
                "stream" : False
            }
        llm_resp = ollama_generate_post_req(ollama_client=client, payload=payload_data_with_weather)
        print(llm_resp["response"])