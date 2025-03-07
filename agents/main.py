import httpx
import json
from typing import List

client = httpx.Client()


def chat_with_memory(user_input : str):
    """ Let's you chat with llama with memory of your previous chats"""
    data = {
        "role" : "user",
        "content" : f"{user_input}"
    }

    with open("data.json", "r") as file:
        json_data = json.load(file)
    
    json_data["messages"].append(data)

    with open("data.json", "w") as file:
        json.dump(json_data, file, indent=4)
        

    with open("data.json", "r") as file:
        loaded_data = json.load(file)
        response = client.post("http://localhost:11434/api/chat", json=loaded_data)

    new_chat = response.json()
    print(new_chat['message'])

    with open("data.json", "r") as file:
        new_data = json.load(file)
    
    new_data["messages"].append(new_chat["message"])

    with open("data.json", "w") as file:
        json.dump(new_data, file, indent=4)
          
# To chat with the model with memory
# while True:
#     inp = input("USER: ")
#     if inp == "q":
#         print("Good Bye")
#         break
#     chat_with_memory(inp)

def tool_calling(user_input : str) -> List : 
    payload_data = {
        "model" : "llama3.2:3b",
        "messages" : [
            {
                "role" : "user",
                "content" : f"{user_input}"
            }
        ],
        "stream" : False,
        "tools" : [
            {
                "type" : "function",
                "function" : {
                    "name" : "get_current_weather",
                    "description" : "Get the current weather for a given location only if the user explicitly specifies that he wants to know the weather of a certain location otherwise please carry a normal conversation with the user",
                    "parameters" : {
                        "type" : "object",
                        "parameters" : {
                            "location" : {
                                "type" : "string",
                                "description" : "The location to get the weather for, e.g. Bengaluru"
                            },
                            "format" : {
                                "type" : "string",
                                "description" : "The format to return the weather is, e.g. 'celsius'"
                            }
                        },
                        "required" : ["location", "format"]
                    }
                }
            }
        ]
    }
    response = client.post("http://localhost:11434/api/chat", json=payload_data)
    msg = response.json()["message"]
    fn_name = msg["tool_calls"][0]["function"]["name"]
    args = msg["tool_calls"][0]["function"]["arguments"]["location"]
    return [fn_name, args]
    
def get_current_weather(city):
    if city == "Bengaluru":
        return "10°"
    if city == "Mysore":
        return "20°"
    

def get_weather():
    while True:
        inp = input("USER: ")
        if inp == "q":
            print("GOOD BYE")
            break
        data_list = tool_calling(inp)
        if data_list[0] == "get_current_weather":
            resp = get_current_weather(data_list[1])
            print(resp)
        



get_weather()