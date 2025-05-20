from fastapi import FastAPI
from .routers import users

app = FastAPI(title="server")

app.include_router(users.user_router)


@app.get("/")
async def root():
    return {"message": "Hello Darthman!"}