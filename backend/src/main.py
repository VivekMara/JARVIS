from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import httpx

load_dotenv()
apiKey = os.getenv("deepseek_api_key")

client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")
