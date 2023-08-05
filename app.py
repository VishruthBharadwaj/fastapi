import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from postgresql import connect
from pymongo import MongoClient

from user_management import register, get_user

app = FastAPI()

@app.post("/register")
async def register(user: User):
    return await register(user)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await get_user(user_id)

if name == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
