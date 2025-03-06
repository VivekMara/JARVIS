import httpx
import json


client = httpx.Client()


def chat_with_memory(user_input : str):
    """ Let's you chat with llama with memory of your previous chats"""
    data = {
        "role" : "user",
        "content" : f"{user_input}"
    }

    with open("data.json", "r") as file:
        json_data = json.load(file)
        print("loaded initially")
    
    json_data["messages"].append(data)

    with open("data.json", "w") as file:
        json.dump(json_data, file, indent=4)
        print("json dumped")
        

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
          

while True:
    inp = input("USER: ")
    if inp == "q":
        print("Good Bye")
        break
    chat_with_memory(inp)



