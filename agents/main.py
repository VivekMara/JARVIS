import httpx
from tools import add_memory_for_chat, tool_calling, get_current_weather, ollama_chat_post_req, ollama_generate_post_req




client = httpx.Client()



#for demonstrating tool calling
while True:
    inp = input("USER: ")
    if inp == "q":
        print("GOOD BYE")
        break
    data_list = tool_calling(user_input=inp, ollama_client=client)
    resp = get_current_weather(data_list[2])
    payload_data_with_weather = {
                "model" : "llama3.2:3b",
                "prompt" : f"You are an AI agent who has already used the tools to get the weather details at the place {data_list[2]} which has the weather forecast of {resp} celsius, your task is to tell this data to the user casually.",
                "stream" : False
            }
    llm_resp = ollama_generate_post_req(ollama_client=client, payload=payload_data_with_weather)
    print(llm_resp["response"])

#for demonstrating chatting with memory
# while True:
#     inp = input("USER: ")
#     if inp == "q":
#         print("GOOD BYE")
#         break
#     resp = add_memory_for_chat(user_input=inp, ollama_client=client)
#     print(resp["content"])