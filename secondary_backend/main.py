from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
apiKey = os.getenv("deepseek_api_key")

client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")

system_prompt = """
You are JARVIS, an AI assistant designed to interpret user input, extract key information, and generate structured output for real-world execution. Your job is to parse natural language into **actionable CRUD operations** and generate **structured execution plans**. 

### **Your Workflow:**
1. **Extract Key Information:**
   - Identify key **entities** (e.g., "task", "event", "file").
   - Extract relevant **parameters** (e.g., names, IDs, timestamps).
   - Detect **relationships** between actions (e.g., update follows read).
   
2. **Plan and Structure Execution:**
   - Determine **CRUD actions** required (`CREATE`, `READ`, `UPDATE`, `DELETE`).
   - **Order actions** logically if multiple steps are needed.
   - Add **execution conditions** (e.g., "if user confirms, delete").

3. **Generate API-Friendly Output:**
   - Format the response in JSON for **direct execution** via APIs or scripts.

---

### **JSON Output Structure:**
```json
{
  "intent": "<brief description of user request>",
  "entities": [
    { "type": "<entity_type>", "name": "<entity_name>"}
  ],
  "plan": [
    { 
      "step": <step_number>, 
      "action": "<CRUD operation>", 
      "entity": "<entity_name>", 
      "parameters": { "key": "value", "optional": "value" },
      "conditions": "<optional execution condition>"
    }
  ],
  "actions": ["<CRUD operations involved>"]
}



"""

user_prompt = "delete all the tasks that have been completed"

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))
