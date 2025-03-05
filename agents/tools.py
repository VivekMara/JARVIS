import sqlite3
import uuid

def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a (int): The first number
    b (int): The second number

  Returns:
    int: The sum of the two numbers
  """

  # The cast is necessary as returned tool call arguments don't always conform exactly to schema
  # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
  return int(a) + int(b)


def subtract_two_numbers(a: int, b: int) -> int:
  """
  Subtract two numbers
  """

  # The cast is necessary as returned tool call arguments don't always conform exactly to schema
  return int(a) - int(b)


def generate_uuid():
    """
    Generates a random UUID (version 4) and returns it as a string.

    Returns:
        str: A randomly generated UUID.
    """
    return str(uuid.uuid4())  # Convert UUID to string for SQLite

def create_db_and_table() -> str:
    """
    Creates a SQLite database and a 'tasks' table if it does not exist.
    The table contains three columns: UUID (TEXT), task description (TEXT),
    and completion status (INTEGER, where 0 = incomplete and 1 = complete).

    Returns:
        str: A confirmation message indicating that the database and table were created.
    """
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (uuid TEXT PRIMARY KEY, task TEXT, completion INTEGER)")
    connection.commit()
    connection.close()
    return "DB and table created!"

def read_tasks() -> list:
    """
    Fetches all tasks from the 'tasks' table.

    Returns:
        list: A list of tuples, where each tuple represents a task (uuid, task, completion).
              If no tasks are found, returns an empty list.
    """
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()  # Fetch all rows
    
    connection.close()
    
    return tasks if tasks else "No tasks found!"  # Return tasks or a message

def insert_task(task:str) -> str:
    """
    Inserts a new task into the 'tasks' table with a unique UUID.
    You have to use this when the user intends to store some reminder or some task which he wants to store in the db

    Args:
        task (str): The description of the task.

    Returns:
        str: A confirmation message indicating that the task was added.
    """
    connection = sqlite3.connect("tasks.db")
    cursor = connection.cursor()
    id = generate_uuid()  # Generate a unique UUID for the task
    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?)", (id, task, 0))  # 0 = Incomplete task
    connection.commit()
    
    # Check total number of tasks after insertion
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    connection.close()
    return f"Task '{task}' added successfully! Total tasks: {count}"


# response = read_tasks()
# print(response)

# resp = insert_task('second')
# print(resp)