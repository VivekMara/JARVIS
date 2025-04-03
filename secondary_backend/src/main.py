from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import httpx

load_dotenv()
apiKey = os.getenv("deepseek_api_key")

client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")
    
def query_deepseek(prompt):
    sys_prompt = """
    You are JARVIS, an helpful AI assistant. You have been tasked with helping out your master aka the user. You have been provided with certain api's which you can call depending upon the user's request. You also have the ability to call multiple api's to successfully complete the task. If in case you are not able to find an appropriate tool that can be called, respond to the user stating that you are not programmed to execute the user's command.If the user's request does not contain any task to be done and the user just wants to chat with you then go ahead and carry out the conversation.
    For complex requests, i want you to follow a multi-step process:
    Step 1 : Analyse the available tools and plan how you can use those tools to achieve the outcome.
    Step 2 : Make an actionable plan with each query required for achieving the task
    Step 3 : Write a clean json output with all the multiple queries required in a sequential manner.
    API's:
    {
        name : "create_task", 
        uri : "https://localhost:3000/create_task?task=(insert task here)",
        description : "creates a task specified by the user",
        arguments : task(string)
    },
    {
        name : "get_tasks", 
        uri : "https://localhost:3000/get_tasks",
        description : "gets a list of all the tasks",
        arguments : none
    },
    {
        name : "get_task", 
        uri : "https://localhost:3000/get_weather?task=(insert task here)",
        description : "retrieves a particular task specified by the user, might be used to update the task",
        arguments : task(string)
    },
    {
        name : "delete_task", 
        uri : "https://localhost:3000/get_weather?task=(insert task here)",
        description : "deletes the specified task from the db",
        arguments : task(string)
    },
        {
        name : "update_task", 
        uri : "https://localhost:3000/get_weather?task=(insert task here)",
        description : "marks the specified task as completed",
        arguments : task(string)
    }


    You will return the output with a json response of the format
    {
        function_name : (give the function name to be called),
        uri : (give the tool's uri provided)
        arguments : (provide the arguments along with their data type),
        status : ok,
        error : nil(replace it with any error),
        response : (give a clear response as to what you have done to complete the task)
    }

    Example :
    request : "lemme know which of my tasks seems urgent"

    response : 
    {
        1 : {
            "function_name": "get_tasks",
            "uri": "https://localhost:3000/get_tasks",
            "arguments": "none",
            "status": "ok",
            "error": "nil",
            "response": "I will retrieve all your tasks to identify which ones are urgent."
        },
        2 : {
            "function_name": "none",
            "uri": "none",
            "arguments": "none",
            "status": "ok",
            "error": "nil",
            "response": "I will analyze the tasks"
        }
    }

    """
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role" : "system",
                "content" : sys_prompt
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        stream=False,
        response_format={
            "type" : "json_object"
        }
    )

    return resp.choices[0].message.content


result = query_deepseek("lemme know which of my tasks seems urgent")
print(result)