import json
from typing import List





def ollama_chat_post_req(ollama_client, payload):
    response = ollama_client.post("http://localhost:11434/api/chat", json=payload)
    return response.json()

def ollama_generate_post_req(ollama_client, payload):
    response = ollama_client.post("http://localhost:11434/api/generate", json=payload)
    return response.json()


def add_memory(user_input : str, ollama_client : object) -> str:
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
        response = ollama_chat_post_req(ollama_client=ollama_client, payload=loaded_data)
        new_chat = response["message"]
    

    with open("data.json", "r") as file:
        new_data = json.load(file)
        new_data["messages"].append(new_chat)
    with open("data.json", "w") as file:
        json.dump(new_data, file, indent=4)

    return new_chat

def tool_calling(user_input : str, ollama_client : object) -> List: 
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
    response = ollama_chat_post_req(ollama_client=ollama_client, payload=payload_data)
    msg = response["message"]
    fn_name = msg["tool_calls"][0]["function"]["name"]
    args = msg["tool_calls"][0]["function"]["arguments"]["location"]
    return [response, fn_name, args]

def get_current_weather(city):
    if city == "Bengaluru":
        return "10°"
    if city == "Mysore":
        return "20°"
    else:
        return None