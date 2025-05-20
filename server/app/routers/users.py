from fastapi import APIRouter
from sqlmodel import Session
from ..database import engine, User


user_router = APIRouter()

@user_router.post("/auth/")
async def add_new_user(user: User):
    try:
        with Session(engine) as session:
            session.add(user)
            session.commit()

            return {
                "message": "User created successfully"
            }
    except Exception as e:
        return{
            "message": f"Error {e}"
        }