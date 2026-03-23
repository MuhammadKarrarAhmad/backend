from fastapi import APIRouter, HTTPException

from database import db
from GLH.models import UserAccount, UserLogin, UserResponse

GLH_router = APIRouter(prefix="/api")

user_collection = db["users"]


@GLH_router.post("/register", response_model=UserResponse)
def register(user: UserAccount):
    existing_user = user_collection.find_one({"email": str(user.email)})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.password != user.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    task_dict = {
        "fullName": user.fullName,
        "email": str(user.email),
        "password": user.password,        "role": user.role
    }

    result = user_collection.insert_one(task_dict)

    return UserResponse(
        id=str(result.inserted_id),
        fullName=user.fullName,
        email=user.email,
        role=user.role
    )


@GLH_router.post("/login")
def login(user: UserLogin):
    existing_user = user_collection.find_one({"email": str(user.email)})

    if not existing_user or existing_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "id": str(existing_user["_id"]),
        "fullName": existing_user["fullName"],
        "email": existing_user["email"],
        "role": existing_user["role"]
    }