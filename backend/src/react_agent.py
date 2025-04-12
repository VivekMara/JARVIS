from openai import OpenAI
import re
import httpx
from dotenv import load_dotenv
import os
import json
import datetime
from backend.src.tools import *

load_dotenv()
apiKey = os.getenv("deepseek_api_key")
client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")

class Agent:
    def __init__(self, system_prompt="", conversation_file=None, username = None):
        self.system_prompt = system_prompt
        self.username = username
        self.data_dir = f"{os.getcwd()}/data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Generate timestamped filename if none provided
        if conversation_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H")
            conversation_file = f"{self.username}_{timestamp}.json"
        
        self.conversation_file = f"{self.data_dir}/{conversation_file}"
        print(self.conversation_file)
        # Initialize conversation file if it doesn't exist
        if not os.path.exists(self.conversation_file):
            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            self._write_messages(messages)
    
    def _read_messages(self):
        with open(self.conversation_file, 'r') as f:
            return json.load(f)
    
    def _write_messages(self, messages):
        with open(self.conversation_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def __call__(self, message):
        # Read current messages
        messages = self._read_messages()
        
        # Add user message
        messages.append({"role": "user", "content": message})
        self._write_messages(messages)
        
        # Get response
        result = self.execute()
        
        # Add assistant response
        messages = self._read_messages()  # Re-read in case file was modified
        messages.append({"role": "assistant", "content": result})
        self._write_messages(messages)
        
        return result
    
    def execute(self):
        messages = self._read_messages()
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        
        return resp.choices[0].message.content

prompt = """
You are JARVIS, a personal AI assistant.
You run in a loop of Thought, Action, PAUSE, Observation. At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate: e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia: e.g. wikipedia: Django
Returns a summary from searching Wikipedia

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()

action_re = re.compile(r"^Action: (\w+): (.*)$")

def query(question, max_turns=5, conversation_file=None, user_name = None):
    i = 0
    bot = Agent(prompt, conversation_file, user_name)
    next_prompt = question
    
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            # Save final state to the conversation file
            return


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
}

while True:
    inp = input("Hello sir, what can i do?\n : ")
    if inp == "q":
        print("have a good day sir!")
        break
    else:
        query(question=inp, user_name="darthman")
