from fastapi import APIRouter, HTTPException
from uuid import uuid4

from database import users_collection
from GLH.models import UserRegistration, UserLogin, UserResponse
from security import hash_password, verify_password

GLH_router = APIRouter(prefix="/api")


@GLH_router.post("/register", response_model=UserResponse)
def register_user(user: UserRegistration):
    # Check if user already exists
    existing_user = users_collection.find_one({"emailAddress": user.emailAddress})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password before storing
    hashed_password = hash_password(user.password)

    # Create user document
    new_user = {
        "userID": str(uuid4()),
        "fullName": user.fullName,
        "emailAddress": user.emailAddress,
        "password": hashed_password,
        "userRole": user.userRole,
        "companyName": user.companyName,
        "companyCategory": user.companyCategory,
        "location": user.location,
    }

    result = users_collection.insert_one(new_user)
    print("Inserted ID:", result.inserted_id)

    return {
        "userID": new_user["userID"],
        "fullName": new_user["fullName"],
        "emailAddress": new_user["emailAddress"],
        "userRole": new_user["userRole"],
        "companyName": new_user["companyName"],
        "companyCategory": new_user["companyCategory"],
        "location": new_user["location"],
    }


@GLH_router.post("/login")
def login_user(credentials: UserLogin):
    # Find user by email
    existing_user = users_collection.find_one(
        {"emailAddress": credentials.emailAddress}
    )

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify hashed password
    if not verify_password(credentials.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "userID": existing_user["userID"],
        "fullName": existing_user["fullName"],
        "emailAddress": existing_user["emailAddress"],
        "userRole": existing_user["userRole"],
        "location": existing_user["location"],
        "companyName": existing_user.get("companyName"),
        "companyCategory": existing_user.get("companyCategory"),
    }


@GLH_router.get("/users")
def get_users():
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))
    return users