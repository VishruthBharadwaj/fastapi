import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from postgresql import connect
from pymongo import MongoClient


class User(BaseModel):
    fullname: str
    email: str
    password: str
    phone: str
    profile_picture: str


def check_email_exists(email):
    connection = connect(user="postgres", password="postgres", database="fastapi")
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return True
    else:
        return False


def register(user: User):
    if check_email_exists(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Save user details in PostgreSQL
    connection = connect(user="postgres", password="postgres", database="fastapi")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (fullname, email, password, phone) VALUES (%s, %s, %s, %s)", (user.fullname, user.email, user.password, user.phone))
    connection.commit()

    # Save user profile picture in MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["fastapi"]
    collection = db["users"]
    collection.insert_one({"email": user.email, "profile_picture": user.profile_picture})

    return {"message": "User registered successfully"}


def get_user(user_id: int):
    # Get user details from PostgreSQL
    connection = connect(user="postgres", password="postgres", database="fastapi")
    cursor = connection.cursor()
    cursor.execute("SELECT fullname, email, phone FROM users WHERE id = %s", (user_id,))
    user_details = cursor.fetchone()

    # Get user profile picture from MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["fastapi"]
    collection = db["users"]
    document = collection.find_one({"id": user_id})

    user = {
        "fullname": user_details[0],
        "email": user_details[1],
        "phone": user_details[2],
        "profile_picture": document["profile_picture"] if document else None,
    }

    return user

