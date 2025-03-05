from ollama import ChatResponse, chat
from tools import read_tasks, insert_task, create_db_and_table, add_two_numbers, subtract_two_numbers


messages = [{'role': 'user', 'content': 'let me know what tasks i have lined up'}]
print('Prompt:', messages[0]['content'])

available_functions = {
  'add_two_numbers': add_two_numbers,
  'subtract_two_numbers': subtract_two_numbers,
  'read_tasks' : read_tasks,
  'insert_task' : insert_task,
  'create_db_and_table' : create_db_and_table
}

response: ChatResponse = chat(
  'llama3.2:3b',
  messages=messages,
  tools=[add_two_numbers, subtract_two_numbers, read_tasks, insert_task, create_db_and_table],
)

if response.message.tool_calls:
  # There may be multiple tool calls in the response
  for tool in response.message.tool_calls:
    # Ensure the function is available, and then call it
    if function_to_call := available_functions.get(tool.function.name):
      print('Calling function:', tool.function.name)
      print('Arguments:', tool.function.arguments)
      output = function_to_call(**tool.function.arguments)
      print(type(output))
      print('Function output:', output)
    else:
      print('Function', tool.function.name, 'not found')

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
  # Add the function response to messages for the model to use
  messages.append(response.message)
  messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

  # Get final response from model with function outputs
  final_response = chat('llama3.2:3b', messages=messages)
  print('Final response:', final_response.message.content)

else:
  print('No tool calls returned from model')