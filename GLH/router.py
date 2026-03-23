from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4

from database import users_collection
from GLH.models import UserRegistration, UserLogin, UserResponse
from security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)

GLH_router = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


@GLH_router.post("/register", response_model=UserResponse)
def register_user(user: UserRegistration):
    existing_user = users_collection.find_one({"emailAddress": user.emailAddress})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

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

    users_collection.insert_one(new_user)

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
    existing_user = users_collection.find_one(
        {"emailAddress": credentials.emailAddress}
    )

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(credentials.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={
            "sub": existing_user["emailAddress"],
            "role": existing_user["userRole"],
            "userID": existing_user["userID"],
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "userID": existing_user["userID"],
            "fullName": existing_user["fullName"],
            "emailAddress": existing_user["emailAddress"],
            "userRole": existing_user["userRole"],
            "location": existing_user["location"],
            "companyName": existing_user.get("companyName"),
            "companyCategory": existing_user.get("companyCategory"),
        },
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = users_collection.find_one({"emailAddress": email})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_buyer(current_user: dict = Depends(get_current_user)):
    if current_user["userRole"] != "buyer":
        raise HTTPException(status_code=403, detail="Buyer access only")
    return current_user


def require_producer(current_user: dict = Depends(get_current_user)):
    if current_user["userRole"] != "producer":
        raise HTTPException(status_code=403, detail="Producer access only")
    return current_user


@GLH_router.get("/buyer-dashboard")
def buyer_dashboard(current_user: dict = Depends(require_buyer)):
    return {
        "message": "Welcome to buyer dashboard",
        "userID": current_user["userID"],
        "fullName": current_user["fullName"],
        "emailAddress": current_user["emailAddress"],
        "userRole": current_user["userRole"],
    }


@GLH_router.get("/producer-dashboard")
def producer_dashboard(current_user: dict = Depends(require_producer)):
    return {
        "message": "Welcome to producer dashboard",
        "userID": current_user["userID"],
        "fullName": current_user["fullName"],
        "emailAddress": current_user["emailAddress"],
        "userRole": current_user["userRole"],
        "companyName": current_user.get("companyName"),
        "companyCategory": current_user.get("companyCategory"),
    }