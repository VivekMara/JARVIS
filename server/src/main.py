from fastapi import FastAPI

app = FastAPI(title="server")

@app.get("/")
async def root():
    return {"message": "Hello Darthman!"}