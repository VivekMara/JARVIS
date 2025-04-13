from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import httpx
from react_agent import query

while True:
    inp = input("Hello sir, what can i do?\n : ")
    if inp == "q":
        print("have a good day sir!")
        break
    else:
        query(question=inp, user_name="darthman")
