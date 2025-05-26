from datetime import datetime
from mcp.server.fastmcp import FastMCP
from sqlmodel import Field, create_engine, SQLModel, Session, select
import uuid
from dotenv import load_dotenv
import os

mcp = FastMCP("TaskManager")

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

class Task(SQLModel, table=True):
    user_id: uuid.UUID = Field(nullable=False)
    task_id: uuid.UUID = Field(nullable=False, default_factory=uuid.uuid4, primary_key=True)
    task_name: str = Field(nullable=False)
    task_desc: str = Field(nullable=False)
    status: bool = Field(default=False)
    created_at: str = Field(nullable=False, default_factory=datetime.now)
    updated_at: str = Field(nullable=False, default_factory=datetime.now)

pg_url = f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}"
engine = create_engine(pg_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

@mcp.tool()
def create_task(title: str, desc: str) -> str:
    """
    Add a new task to the database.

    Args:
        title (str): The title of the task.
        desc (str): The description of the task.

    Returns:
        str: Confirmation message or error.
    """
    task = Task(user_id=uuid.uuid4(), task_name=title, task_desc=desc)
    try:
        with Session(engine) as session:
            session.add(task)
            session.commit()
        return f"Task '{title}' created successfully"
    except Exception as e:
        return f"Error creating task with the error: {e}"

@mcp.tool()
def read_tasks() -> list[dict]:
    """
    Fetch all tasks from the database.

    Returns:
        list[dict]: List of tasks (each task is a dictionary with keys like 'id', 'title', etc.).
    """
    try:
        with Session(engine) as session:
            statement = select(Task)
            result = session.exec(statement=statement)
            return [dict(row) for row in result]
    except Exception as e:
        return f"Error reading tasks with the error: {e}"

@mcp.tool()
def mark_task_completed_by_id(task_id: uuid.UUID) -> str:
    """
    Mark a specific task as 'completed' based on its task ID.
    If status is False, then the task is not completed yet.

    Args:
        task_id (uuid.UUID): ID of the task to update.

    Returns:
        str: Status message (e.g., "Task 5 marked as completed").
    """
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if task == None:
                return f"No task with the task id: {task_id}"
            else:
                task.status = True
                task.updated_at = datetime.now()
                session.add(task)
                session.commit()
                session.refresh(task)
                return f"Updated task: {task}"
    except Exception as e:
        return f"Error updating the task with the error: {e}"


@mcp.tool()
def delete_task_by_id(task_id: uuid.UUID) -> str:
    """
    Delete a task based on its ID.

    Args:
        task_id (uuid.UUID): The ID of the task to delete.

    Returns:
        str: Status message (e.g., "Deleted task 5").
    """
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            session.delete(task)
            session.commit()
            return f"Deleted the task: {task}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    init_db()
    mcp.run(transport='stdio')
