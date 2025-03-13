import httpx
from tools import add_memory_for_chat, weather_tool_calling, get_current_weather, ollama_chat_post_req, ollama_generate_post_req, task_tool_calling, create_task, read_tasks, delete_task, read_task




client = httpx.Client(timeout=200.0)



#for demonstrating weather tool calling
# while True:
#     inp = input("USER: ")
#     if inp == "q":
#         print("GOOD BYE")
#         break
#     data_list = weather_tool_calling(user_input=inp, ollama_client=client)
#     print(data_list)
#     print(data_list[2])
#     resp = get_current_weather(data_list[2])
#     print(resp)
#     payload_data_with_weather = {
#                 "model" : "llama3.2:3b",
#                 "prompt" : f"You are an AI weather reporter who has access to the weather at {data_list[2]} place which has the temperature of {resp} Celsius. Your job is to report this data to the user professionally. If by chance you get the temperature as None, then please report that there is some problem with the server currently and tell them that you are sorry for the inconvenience caused.",
#                 "stream" : False
#             }
#     llm_resp = ollama_generate_post_req(ollama_client=client, payload=payload_data_with_weather)
#     print(llm_resp["response"])

#for demonstrating chatting with memory
# while True:
#     inp = input("USER: ")
#     if inp == "q":
#         print("GOOD BYE")
#         break
#     resp = add_memory_for_chat(user_input=inp, ollama_client=client)
#     print(resp["content"])

#for demonstrating task tool calling
while True:
    inp = input("USER: ")
    if inp == "q":
        print("GOOD BYE")
        break
    data_list = task_tool_calling(user_input=inp, ollama_client=client)
    msg = data_list[0]
    fn_name = data_list[1]
    args = data_list[2]
    match fn_name:
        case "create_task":
            create_task(title=args["title"], description=args["description"])
            print(args["title"] + " task added successfully")
        case "read_tasks":
            tasks = read_tasks()
            for i in tasks:
                print(f"{i["title"]} : {i["description"]}")
    # resp = get_current_weather(data_list[2])
    # print(resp)
    # payload_data_with_weather = {
    #             "model" : "llama3.2:3b",
    #             "prompt" : f"You are an AI weather reporter who has access to the weather at {data_list[2]} place which has the temperature of {resp} Celsius. Your job is to report this data to the user professionally. If by chance you get the temperature as None, then please report that there is some problem with the server currently and tell them that you are sorry for the inconvenience caused.",
    #             "stream" : False
    #         }
    # llm_resp = ollama_generate_post_req(ollama_client=client, payload=payload_data_with_weather)
    # print(llm_resp["response"])