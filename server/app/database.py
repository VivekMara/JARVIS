from sqlmodel import create_engine, Field, SQLModel, Session
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
db_name = os.getenv("DB_NAME")
db_pass = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    password: str


engine = create_engine(f"postgresql://{db_user}:{db_pass}@localhost/{db_name}", echo=True)

SQLModel.metadata.create_all(engine)