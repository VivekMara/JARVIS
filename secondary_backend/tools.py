import json
from typing import List
import uuid

def ollama_chat_post_req(ollama_client, payload):
    response = ollama_client.post("http://localhost:11434/api/chat", json=payload)
    return response.json()

def ollama_generate_post_req(ollama_client, payload):
    response = ollama_client.post("http://localhost:11434/api/generate", json=payload)
    return response.json()


def add_memory_for_chat(user_input: str, ollama_client: object) -> str:
    file_path = "data.json"

    with open(file_path, "r") as file:
        json_data = json.load(file)

    json_data["messages"].append({"role": "user", "content": user_input})

    response = ollama_chat_post_req(ollama_client=ollama_client, payload=json_data)
    new_chat = response["message"]

    json_data["messages"].append(new_chat)

    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)

    return new_chat

def weather_tool_calling(user_input : str, ollama_client : object) -> List: 
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
                    "description" : "Get the current weather for a given location only if the user explicitly specifies that he or she wants to know the weather of a certain location otherwise please reply according to the user's request.",
                    "parameters" : {
                        "type" : "object",
                        "properties" : {
                            "location" : {
                                "type" : "string",
                                "description" : "The location to get the weather for, e.g. Bengaluru or Mysore"
                            },
                            "format" : {
                                "type" : "string",
                                "description" : "The format to return the weather is, e.g. 'celsius' or 'fahrenheit",
                                "enum" : ["celsius", "fahrenheit1q"]
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
        return "-1°"
    if city == "Mysore":
        return "20°"
    else:
        return None

import json

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def create_task(title, description):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

def read_tasks():
    return load_tasks()

def read_task(user_inp, ollama_client):
    tasks = load_tasks()
    payload_data = {
        "model" : "llama3.2:3b",
        "prompt" : f"You have been tasked with a list of tasks : {tasks}. Your job is to compare the list of tasks with the given input task : {user_inp} and tell me the most relevant task from the list of tasks. Do not give me the code to find the relevant task. I want you to compare and tell me that particular task id alone. I do not want you to reply with anything else",
        "stream" : False
    }
    resp = ollama_generate_post_req(ollama_client=ollama_client, payload=payload_data)
    print(resp["response"])


def update_task(task_id, title=None, description=None, completed=None):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if completed is not None:
                task["completed"] = completed
            save_tasks(tasks)
            return task
    return None

def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.pop(task)
    save_tasks(tasks)
    return True

def task_tool_calling(user_input : str, ollama_client : object) -> List:
    payload_data = {
    "model": "llama3.2:3b",
    "messages": [
        {
            "role": "user",
            "content": f"{user_input}"
        }
    ],
    "stream": False,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task with a title and description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task."
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the task."
                        }
                    },
                    "required": ["title", "description"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_tasks",
                "description": "Retrieve all tasks.",
                "parameters": {}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task by ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to update."
                        },
                        "title": {
                            "type": "string",
                            "description": "The new title of the task."
                        },
                        "description": {
                            "type": "string",
                            "description": "The new description of the task."
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Mark the task as completed or not."
                        }
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task by ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to delete."
                        }
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]
}
    resp = ollama_chat_post_req(ollama_client=ollama_client, payload=payload_data)
    msg = resp["message"]
    fn_name = msg["tool_calls"][0]["function"]["name"]
    args = msg["tool_calls"][0]["function"]["arguments"]
    return [msg, fn_name, args]
