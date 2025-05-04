from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    print(response.choices[0].message.content)
    return response.choices[0].message

client = OpenAI(
    api_key="sk-4e104f54eaef4827b95e51be64b8e27c",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

# messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
# message = send_messages(messages)
# print(f"User>\t {messages[0]['content']}")

# tool = message.tool_calls[0]
# messages.append(message)

# messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
# message = send_messages(messages)
# print(f"Model>\t {message.content}")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "hello deepseek"}],
    tools=tools
)
print(response.choices[0])
