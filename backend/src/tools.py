import httpx
import sqlite3


def wikipedia(q):
    response =  httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()
    hits = response["query"]["searchinfo"]["totalhits"]
    if hits == 0:
        return "No results found"
    else:
        result = response["query"]["search"][0]["snippet"]
        return result

def calculate(what):
    return eval(what)


def initDB():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    # Create todos table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    return conn, cursor

# CREATE
def create_todo(title):
    conn, cursor = initDB()
    cursor.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

# READ
def read_todos():
    conn, cursor = initDB()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return todos

# UPDATE
def update_todo(todo_id, new_title=None, completed=None):
    conn, cursor = initDB()
    if new_title is not None:
        cursor.execute("UPDATE todos SET title = ? WHERE id = ?", (new_title, todo_id))
    if completed is not None:
        cursor.execute("UPDATE todos SET completed = ? WHERE id = ?", (int(completed), todo_id))
    conn.commit()
    conn.close()

# DELETE
def delete_todo(todo_id):
    conn, cursor = initDB()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
