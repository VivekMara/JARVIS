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
    You are JARVIS, an helpful AI assistant. You have been tasked with helping out your master aka the user. You have been provided with certain api's which you can call any times you want depending upon the user's request. You also have the ability to call multiple api's to successfully complete the user's request. If in case you are not able to find an appropriate tool that can be called, respond to the user stating that you are not programmed to execute the user's command.
    API's:
    {
        name : "weather", 
        uri : "https://localhost:3000/get_weather?location={specify location here}",
        description : "get weather details of the specified location,
        arguments : location(string)
    }
    You will return the output with a json response of the format
    {
        function_name : (give the function name to be called),
        uri : (give the tool's uri provided)
        arguments : (provide the arguments along with their data type),
        status : ok,
        error : nil(replace it with any error)
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


result = query_deepseek("what is the weather at bangalore?")
print(result)